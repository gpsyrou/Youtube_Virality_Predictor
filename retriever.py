"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""

import os
import json
from tube.connector import TubeVideoMultiWritter, TubeChannelMultiWritter
from tube.validation import is_header_synced_with_catalog


CONFIGS_PATH = os.path.join(os.getcwd(), 'config')

catalog_path = os.path.join(CONFIGS_PATH, 'video_catalog.json')
params_path = os.path.join(CONFIGS_PATH, 'param.json')
channels_path = os.path.join(CONFIGS_PATH, 'channel_catalog.json')
datasets_path = os.path.join(os.getcwd(), 'data')

if __name__ == '__main__':
    with open(catalog_path) as video_catalog_json:
        catalog = json.load(video_catalog_json)
        video_catalog_json.close()

    with open(params_path) as params_json:
        params = json.load(params_json)
        params_json.close()

    with open(channels_path) as channels_json:
        channels_catalog = json.load(channels_json)
        channels_json.close()

    db_name = params['database_name']
    metadata_table_name = params['meta_table_name']
    header_f = params['header_csv_filename']
    lines_f = params['lines_csv_filename']
    channel_f = params['channels_csv_filename']

    videos_logger = TubeVideoMultiWritter(video_collection=catalog)

    channel_logger = TubeChannelMultiWritter(
        channel_collection=channels_catalog
        )

    # Update Videos

    # Check all videos in lines and header match
    data_synced = is_header_synced_with_catalog(
        header_f=os.path.join(datasets_path, header_f),
        catalog=catalog
        )

    if data_synced:
        # DB push
        # videos_logger.meta_push_to_db_lines()

        videos_logger.write_dataframes_to_csv(
            filename=os.path.join(datasets_path, lines_f),
            kind='lines'
            )
    else:
        # DB push
        # videos_logger.meta_push_to_db_header()
        # videos_logger.meta_push_to_db_lines()

        # Flat files push
        videos_logger.write_dataframes_to_csv(
            filename=os.path.join(datasets_path, header_f),
            kind='header'
            )

        videos_logger.write_dataframes_to_csv(
            filename=os.path.join(datasets_path, lines_f),
            kind='lines'
            )
'''
    # Update Channels
    channel_logger.write_channel_dataframes_to_csv(
        filename=os.path.join(datasets_path, channel_f)
        )
'''