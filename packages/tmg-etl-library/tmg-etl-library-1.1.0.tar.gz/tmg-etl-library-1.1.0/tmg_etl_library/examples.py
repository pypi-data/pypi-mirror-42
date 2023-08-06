'''
This file is to showcase the goals of this library to simplify creating basic data-transfers between and within technologies.
'''

from tmg_etl_library.components.databases import bq, mysql
from tmg_etl_library.components.locals import csv
from tmg_etl_library.cloud_logger import cloud_logger
from tmg_etl_library.components.config_classes import BQTOBQConfig, BQTOMySQLConfig, CSVTOBQConfig, BQTOCSVConfig
from tmg_etl_library.data_transfers.datatransfers import BQTOBQ, BQTOMySQL, CSVTOBQ, BQTOCSV

'''
Basic CSV insert to BQ
'''


log = cloud_logger.Logger(app_name='examples',
                          logger_name='examples',
                          google_project_id='tmg-plat-dev')

BQ_connection = bq.BQClient(log=log,
                            project='tmg-plat-dev')

source_file = csv.CSVFile(name='example.csv',
                          path='/Users/masond/git/etl_library/tmg-etl-library/tmg_etl_library',
                          delimiter=',')


target_table = bq.BQTable(client=BQ_connection,
                          project='tmg-plat-dev',
                          dataset='examples',
                          name='example_source_table')
target_table.schema = [{'name': 'example_field', 'type': 'string'},
                       {'name': 'example_numbers', 'type': 'integer'}]

config = CSVTOBQConfig()
config.create_disposition = 'REPLACE_IF_EXISTS'
config.allow_jagged_rows = True
config.skip_leading_rows = True

transfer = CSVTOBQ(log=log,
                   CSVFile=source_file,
                   BQTable=target_table,
                   config=config)

transfer.run()

'''
Basic query to table in BQ
'''

log = cloud_logger.Logger(app_name='examples',
                          logger_name='examples',
                          google_project_id='tmg-plat-dev')

BQ_connection = bq.BQClient(log=log,
                            project='tmg-plat-dev')

source_table = bq.BQTable(client=BQ_connection,
                          project='tmg-plat-dev',
                          dataset='examples',
                          name='example_source_table')
source_table.schema = [{'name': 'example_field', 'type': 'string'},
                       {'name': 'example_numbers', 'type': 'integer'}]

target_table = bq.BQTable(client=BQ_connection,
                          project='tmg-plat-dev',
                          dataset='examples',
                          name='example_target_table')
target_table.schema = [{'name': 'result', 'type': 'integer'}]

config = BQTOBQConfig()
config.force_table_creation = True
config.write_disposition = 'WRITE_APPEND'
config.query = 'Select * from `tmg-plat-dev.examples.{table}`'

pipeline = BQTOBQ(log=log,
                  source=source_table,
                  target=target_table,
                  config=config)
pipeline.run()

'''
Basic pull from BQ
'''

log = cloud_logger.Logger(app_name='examples',
                          logger_name='examples',
                          google_project_id='tmg-plat-dev')

BQ_connection = bq.BQClient(log=log,
                            project='tmg-plat-dev')

source_table = bq.BQTable(client=BQ_connection,
                          project='tmg-plat-dev',
                          dataset='examples',
                          name='example_target_table')
source_table.schema = [{'name': 'result', 'type': 'integer'}]

local_runner = csv.CSVClient(log=log)
target_file = csv.CSVFile(name='result.csv',
                          path='/Users/masond/git/etl_library/tmg-etl-library/tmg_etl_library',
                          delimiter=',')
target_file.client = local_runner

config = BQTOCSVConfig()
config.skip_leading_rows = False

pipeline = BQTOCSV(log=log,
                   BQTable=source_table,
                   CSVFile=target_file,
                   config=config)

pipeline.run()


'''
Functions example
'''

log = cloud_logger.Logger(app_name='examples',
                          logger_name='examples',
                          google_project_id='tmg-plat-dev')

BQ_connection = bq.BQClient(log=log,
                            project='tmg-plat-dev')

source_table = bq.BQTable(client=BQ_connection,
                          project='tmg-plat-dev',
                          dataset='examples',
                          name='example_source_table')
source_table.schema = [{'name': 'example_field', 'type': 'string'},
                       {'name': 'example_numbers', 'type': 'integer'}]

print(source_table.exists())
results, _ = BQ_connection.run_query('Select * from `tmg-plat-dev.examples.example_source_table`')
print(results)

'''
Basic BQToMySQL move
'''

# log = cloud_logger.Logger(app_name='examples',
#                           logger_name='examples',
#                           google_project_id='tmg-plat-dev')
#
# BQ_connection = bq.BQClient(log=log,
#                             project='tmg-plat-dev')
#
# MySQL_connection = mysql.MySQLClient(log=log,
#                                      hostname='example',
#                                      username='example',
#                                      password='test',
#                                      dataset='test')
#
# source_table = bq.BQTable(client=BQ_connection,
#                           project='tmg-plat-dev',
#                           dataset='examples',
#                           name='example_source_table')
# source_table.schema = [{'name': 'example_field', 'type': 'string'},
#                        {'name': 'example_numbers', 'type': 'integer'}]
#
# target_table = mysql.MySQLTable(client=MySQL_connection,
#                                 dataset='examples',
#                                 name='example')
# target_table.schema = [{'name': 'example_field', 'type': 'string'},
#                        {'name': 'example_numbers', 'type': 'integer'}]
#
# config = BQTOMySQLConfig()
# config.write_disposition = 'WRITE_APPEND'
#
# pipeline = BQTOMySQL(log=log,
#                      source=source_table,
#                      target=target_table,
#                      config=config)
# pipeline.run()