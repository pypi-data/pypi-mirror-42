from tmg_etl_library.components.databases.database import Database
from tmg_etl_library.components.buckets.gs import GSClient

from google.api_core.exceptions import NotFound
from google.cloud.bigquery.table import TimePartitioning, TimePartitioningType
from google.cloud.bigquery.job import ExtractJobConfig, CopyJobConfig, QueryJobConfig, QueryJob
from google.cloud import bigquery
from google.cloud import storage

from jsonschema import validate, ValidationError

import re
import os
import datetime as dt
import time
import csv


class BQClient(Database):
    def __init__(self, log, project):
        super().__init__(log)
        self.project = project
        self.google_client = bigquery.Client(project=project)

    def list_tables(self, dataset, table_regex=''):
        '''
        :param project: String Project
        :param dataset: String Dataset
        :param table_regex: Option Regex to Filter the Tables Returned
        :return: List of BQTable Objects
        '''

        project = self.project
        google_bq_dataset = self._get_dataset(project, dataset)
        google_bq_table_items = self.google_client.list_tables(google_bq_dataset)

        table_names = [table.table_id for table in google_bq_table_items]

        if table_regex:
            table_names = [table_name for table_name in table_names if re.match(table_regex, table_name)]

        bqTables = [BQTable(project=project, dataset=dataset, name=table) for table in table_names]

        return bqTables

    def _create_gbq_schema(self, BQTable_schema):
        """
        :param BQTable_schema:
        :return: [SchemaField]
        """
        return [bigquery.SchemaField(name=column['name'], field_type=column['type'], mode=column.get('mode', 'NULLABLE'))
                for column in BQTable_schema]

    def run_query(self, query=None, query_file_name=None, destination=None, write_disposition=None, use_legacy_sql=False, async_query=False, query_params={}):
        """
        :param query: String Query to be Performed
        :param destination: BQTable, where the results of the query should be written to
        :param write_disposition: If the table exists, WRITE_TRUNCATE or WRITE_APPEND, Default: WRITE_EMPTY
        :param use_legacy_sql: Defaults to False - uses Standard SQL
        :return:
        """
        if not (query or query_file_name):
            raise Exception("query or query_file_name should be provided.")

        if query_file_name:
            with open(query_file_name, mode="r") as query_file:
                query = query_file.read()

        query = query.format(**query_params)

        job_config = bigquery.QueryJobConfig()
        job_config.use_legacy_sql = use_legacy_sql

        if destination:
            self.logger.info('Query Destination: %s' % str(destination))
            if destination.partitioned_field:
                job_config.time_partitioning = TimePartitioning(type_=TimePartitioningType.DAY, field=destination.partitioned_field)
            google_bq_table = self._get_table_ref(destination)
            job_config.destination = google_bq_table

        if write_disposition:
            job_config.write_disposition = write_disposition

        self.logger.info('Running Query')
        query_job = self.google_client.query(query, job_config=job_config)  # API request - starts the query asynchronously

        if async_query:
            return query_job

        while True:
            query_job.reload()  # Refreshes the state via a GET request.
            if query_job.state == 'DONE':
                if query_job.error_result:
                    raise RuntimeError(query_job.errors)
                break
            time.sleep(1)

        iterator = query_job.result()

        headers = [col.name for col in iterator.schema]

        data = []
        for row in iterator:
            result_row = []
            for point in row:
                result_row.append(point)
            data.append(result_row)

        return data, headers

    def wait_for_queries(self, query_jobs):
        """
        :param QueryJobs: List of QueryJob type
        :return:
        """
        if not isinstance(query_jobs, list):
            raise TypeError('queries must be of type list')
        else:
            for query_job in query_jobs:
                if not isinstance(query_job, QueryJob):
                    raise TypeError('Values in list must be of type QueryJob')

        for query_job in query_jobs:
            while True:
                query_job.reload()  # Refreshes the state via a GET request.
                if query_job.state == 'DONE':
                    if query_job.error_result:
                        raise RuntimeError(query_job.errors)
                    self.logger.info('Query Job with id "%s" has completed' % query_job.job_id)
                    break
                time.sleep(1)

        return True

    def _get_table_ref(self, table):
        """
        Retrieves table reference
        :param table: BQTable object
        :return:
        """

        dataset = self._get_dataset(table.project, table.dataset)
        if not dataset:
            return None
        return dataset.table(table_id=table.name)

    def _get_dataset(self, project, dataset_id, location='EU', force_dataset_creation=False):
        """
        Create or get the dataset in GC
        :param project: project name
        :param dataset_name: dataset name
        :param location: dataset location name: EU or US
        :param force_dataset_creation: If True creates a dataset if doesn't exists
        :return: dataset
        """

        dataset_ref = bigquery.DatasetReference(dataset_id=dataset_id, project=project)
        try:
            dataset = self.google_client.get_dataset(dataset_ref=dataset_ref)
            self.logger.info('Dataset {0} is reached.'.format(dataset_id))
            return dataset
        except NotFound:
            if force_dataset_creation:
                dataset = bigquery.Dataset(dataset_ref=dataset_ref)
                dataset.location = location
                self.google_client.create_dataset(dataset)
                self.logger.info('Dataset {0} is created.'.format(dataset_id))
                return dataset
            else:
                return None


    def delete_from_storage(self, project, bucket_name, filename):
        #TODO: potentially move to storage object
        """
        Delete a file from storage

        :param project: Project name
        :param bucket_name: Bucket name
        :param src_filename: file in the bucket
        :return:
        """

        client = storage.Client(project=project)
        bucket = client.get_bucket(bucket_name)

        blob = bucket.blob(filename.name)

        blob.delete(client)

        self.logger.info("Deleting {filename} from bucket gs://{bucket}".format(
            filename=filename,
            bucket=bucket_name,
        ))

    def get_schema_from_bq(self, table):
        """
        :param table: BQTable
        :return:
        """
        #TODO: Code this functionality
        google_bq_current_table_ref = self.get_table_ref(table)
        google_bq_current_table = self.client.get_table(google_bq_current_table_ref)
        current_field_names = [field.name for field in google_bq_current_table.schema]

        new_schema_field_names = [field['name'] for field in table.schema]

class BQTable:
    def __init__(self, client, project, dataset, name):
        """
        Class that contains all the information needed to represent a BQ table

        :param project: BQ project name
        :param dataset: BQ dataset name
        :param name: BQ table name
        :param schema: BQ schema (Dictionary)
        """
        self.project = project
        self.dataset = dataset
        self.name = name
        self._schema = None
        self._expiry = None
        self._partitioned_field = None
        if isinstance(client, BQClient):
            self._client = client
        else:
            raise TypeError('Client should be of BQClient type')

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        raise RuntimeError('The client should not updated after creation of the BQTable')

    def __repr__(self):
        return '%s.%s.%s' % (self.project, self.dataset, self.name)

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value):
        valid_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "mode": {"type": "string"},
                    "type": {"type": "string"}
                },
                'required': ["name", "type"],
                "additionalProperties": False,
                'max_items': 3
            }
        }

        try:
            validate(value, valid_schema)
            self._schema = value
        except ValidationError as e:
            raise Exception('Schema given is not in the correct format. Please check documentation.')

    @property
    def expiry(self):
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        """
        :param value: Time in Minutes for when the table should expire (delete itself)
        :return: Nothing
        """
        if not isinstance(value, int):
            raise TypeError('expiry must be an Integer')

        self._expiry = value

    @property
    def partitioned_field(self):
        return self._partitioned_field

    @partitioned_field.setter
    def partitioned_field(self, value):
        """
        :param value: Field (String) to set as the field to partition the table on
        :return: Nothing
        """
        if not isinstance(value, str):
            raise TypeError('Partitioned Field must be a String')

        self._partitioned_field = value

    def exists(self):
        """
        Checks to see if a big query table exists
        :param client: Client object to interact with BQ
        :return: True/False
        """

        google_table_ref = self.client._get_table_ref(self)

        try:
            self.client.google_client.get_table(google_table_ref)
            return True
        except NotFound:
            return False

    def delete(self):
        """
        :param client: Client object to interact with BQ
        :return: Nothing
        """

        google_bq_table = self.client._get_table_ref(self)
        self.client.logger.info('Deleting Table: %s' % str(self))
        self.client.google_client.delete_table(google_bq_table)

    def create(self, force_dataset_creation=True, force_table_creation=True):
        """
        Creates a new empty table in BQ.
        :param table: BQTable
        :param config: BQTableConfig
        :return: BQTable
        """

        if not self.schema:
            raise Exception('No schema is defined.')

        dataset = self.client._get_dataset(self.project, self.dataset, force_dataset_creation=force_dataset_creation)
        if not dataset:
            raise Exception('Dataset {0} not found'.format(self.dataset))

        table_ref = dataset.table(self.name)

        try:
            self.client.google_client.get_table(table_ref)
            self.client.logger.info('Table {0} already exists.'.format(self.name))
            return self
        except NotFound:
            if not force_table_creation:
                raise Exception('Table {0} does not exist and force_table_creation is not set to True.'.format(self.name))
            self.client.logger.info('Table {0} does not exists.'.format(self.name))

        google_schema = self.client._create_gbq_schema(self.schema)
        gbq_table = bigquery.Table(table_ref, schema=google_schema)

        if self.expiry:
            expiry_datetime = dt.datetime.now() + dt.timedelta(minutes=self.expiry)
            gbq_table.expires = expiry_datetime

        if self.partitioned_field:
            gbq_table.time_partitioning = TimePartitioning(type_=TimePartitioningType.DAY, field=self.partitioned_field)

        self.client.google_client.create_table(gbq_table)
        self.client.logger.info('Table {0} is created.'.format(self.name))

    def update_table_schema(self):
        '''
        :param table: BQTable object
        '''

        self.client.logger.info('Updating Schema for Table %s' % str(self))
        google_bq_current_table_ref = self.client._get_table_ref(self)
        google_bq_current_table = self.client.google_client.get_table(google_bq_current_table_ref)
        current_field_names = [field.name for field in google_bq_current_table.schema]

        new_schema_field_names = [field['name'] for field in self.schema]
        columns_removed = [field_name for field_name in current_field_names if field_name not in new_schema_field_names]

        if columns_removed:
            raise Exception('New Schema does not have columns which exist in current table - Please Include')

        updated_schema = [bigquery.SchemaField(name=column['name'], field_type=column['type'], mode=column.get('mode', 'NULLABLE'))
                          for column in self.schema]

        google_bq_current_table.schema = updated_schema

        self.client.google_client.update_table(google_bq_current_table, ['schema'])

