"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""
import os
import pandas as pd
import json
import sqlite3
from tube.metadata import MetadataCollector
from database.db import insert_into_q


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


class TubeLogger(MetadataCollector):
    def __init__(self, video_url: str):
        MetadataCollector.__init__(self, video_url=video_url)
        self.data = self.merge_video_meta_info()

    def create_dataframe_for_video(self) -> pd.DataFrame:
        meta_info_dict = self.merge_video_meta_info()
        df = pd.DataFrame.from_records([meta_info_dict])

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


class MultiTubeWritter():
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
            video = TubeLogger(video_url=video_url)
            video.insert_into_metadata_table(
                target_tablename=metadata_table_name
                )


# test = TubeLogger(video_url='https://youtu.be/yzTuBuRdAyA')
# test.create_insert_into_query()

logger = MultiTubeWritter(video_collection=catalog)
logger.multivideo_meta_push_to_db()
