"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""

import os
import json
from tube.connector import TubeLogger, TubeMultiWritter

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

logger = TubeMultiWritter(video_collection=catalog)
logger.multivideo_meta_push_to_db()
logger.write_dataframes_to_csv(filename='video_metadata.csv')

test1 = TubeLogger(video_url='https://youtu.be/yzTuBuRdAyA')
test2 = TubeLogger(video_url='https://youtu.be/NcXsK_u4ixI')
