"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""

import os
import json
from tube.connector import TubeVideoMultiWritter
from tube.validation import is_header_synced_with_catalog

CONFIGS_PATH = os.path.join(os.getcwd(), 'config')

catalog_path = os.path.join(CONFIGS_PATH, 'video_catalog.json')
params_path = os.path.join(CONFIGS_PATH, 'param.json')


with open(catalog_path) as video_catalog_json:
    catalog = json.load(video_catalog_json)
    video_catalog_json.close()

with open(params_path) as params_json:
    params = json.load(params_json)
    params_json.close()

db_name = params['database_name']
metadata_table_name = params['meta_table_name']
header_f = params['header_csv_filename']
lines_f = params['lines_csv_filename']

logger = TubeVideoMultiWritter(video_collection=catalog)

# Check all videos in lines and header match
data_synced = is_header_synced_with_catalog(header_f=header_f, catalog=catalog)

if data_synced:
    # DB push
    logger.meta_push_to_db_lines()

    logger.write_dataframes_to_csv(
        filename=lines_f,
        kind='lines'
        )
else:
    # DB push
    logger.meta_push_to_db_header()
    logger.meta_push_to_db_lines()

    # Flat files push
    logger.write_dataframes_to_csv(
        filename=header_f,
        kind='header'
        )

    logger.write_dataframes_to_csv(
        filename=lines_f,
        kind='lines'
        )
