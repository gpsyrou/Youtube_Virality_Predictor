"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""

import os
import pandas as pd
import json
import sqlite3
from tube.metadata import VideoMetadataCollector
from database.db import insert_into_q
from tube.transformer import get_current_datetime

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


class TubeVideoLogger(VideoMetadataCollector):
    def __init__(self, video_url: str):
        VideoMetadataCollector.__init__(self, video_url=video_url)
        self.data = self.merge_video_meta_info()

    def create_dataframe_for_video(self) -> pd.DataFrame:
        meta_info_dict = self.merge_video_meta_info()
        print('Creating metadata df for video_id: \'{0}\''.format(
            self.video_id)
            )
        df = pd.DataFrame.from_records([meta_info_dict])

        curr_time = get_current_datetime()
        df['CreatedDate'] = curr_time.split(' ')[0]
        df['CreatedDatetime'] = curr_time

        return df

    def create_json_line_for_video(self) -> str:
        json_line = json.dumps(self.data)
        return json_line

    def create_insert_into_query(
        self,
        q: str = insert_into_q,
        target_tablename: str = metadata_table_name
    ) -> str:
        self.insert_query = q.format(
            target_tablename,
            self.channel_id,
            self.video_id,
            self.title,
            self.description,
            self.thumbnail,
            self.video_duration,
            self.video_genre,
            self.regions_allowed,
            self.published_date,
            self.upload_date,
            self.number_of_views,
            self.number_of_likes,
            self.video_url
            )
        return self.insert_query

    def insert_into_metadata_table(
        self,
        target_tablename: str = metadata_table_name
    ) -> None:

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        print('Populating: {0} for video_id: \'{1}\''.format(
            target_tablename, self.video_id)
            )

        query = self.create_insert_into_query(
            target_tablename=target_tablename
            )

        c.execute(query)
        print('Finishing Transaction on: {0} for video_id: \'{1}\'\n'.format(
            target_tablename, self.video_id)
            )

        conn.commit()
        conn.close()


class TubeVideoMultiWritter():
    def __init__(self, video_collection: dict):
        self.video_collection = video_collection
        self.video_url_list = self.generate_video_list()

    def generate_video_list(self):
        video_url_list = []
        for video in self.video_collection['videos']:
            if video.get('run'):
                video_url_list.append(video.get('url'))
        return video_url_list

    def multivideo_meta_push_to_db(self) -> None:
        for video_url in self.video_url_list:
            video = TubeVideoLogger(video_url=video_url)
            video.insert_into_metadata_table(
                target_tablename=metadata_table_name
                )

    def combine_video_dataframes(self) -> pd.DataFrame:
        all_videos_df = pd.DataFrame()
        for video_url in self.video_url_list:
            video = TubeVideoLogger(video_url=video_url)
            video_df = video.create_dataframe_for_video()
            all_videos_df = all_videos_df.append(video_df)
        return all_videos_df

    def write_dataframes_to_csv(self, filename: str) -> None:
        if not os.path.isfile(filename):
            pd.DataFrame().to_csv(filename, index=True)
        df_history = pd.read_csv(filename, index_col=[0])
        all_videos_df = self.combine_video_dataframes()

        df_history = df_history.append(all_videos_df)
        print('\nUpdating metadata file at: {0}\n'.format(filename))
        df_history.to_csv(filename, index=True)
