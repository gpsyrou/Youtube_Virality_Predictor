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
from database.db import (
    insert_into_q,
    insert_into_video_lines_q,
    insert_into_video_header_q,
    get_distinct_video_ids_from_db_table
    )
from tube.transformer import get_current_datetime
from tube.validation import transform_json_urls_to_video_ids
from pandas.errors import EmptyDataError

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
header_table_name = params['header_table_name']
lines_table_name = params['lines_table_name']

catalog = transform_json_urls_to_video_ids(catalog)

try:
    video_ids_exist_in_header_ls = get_distinct_video_ids_from_db_table(
        table_name=header_table_name
        )
except sqlite3.OperationalError:
    video_ids_exist_in_header_ls = []


class TubeVideoLogger(VideoMetadataCollector):
    def __init__(self, video_url: str):
        VideoMetadataCollector.__init__(self, video_url=video_url)
        self.data = self.merge_video_meta_info()
        # self.variable_metadata = self.collect_variable_metadata()

    def create_dataframe_for_video(self, kind: str = 'all') -> pd.DataFrame:
        if kind == 'all':
            meta_info_dict = self.merge_video_meta_info()
        elif kind == 'header':
            meta_info_dict = self.merge_video_constant_metadata()
        elif kind == 'lines':
            meta_info_dict = self.merge_video_variable_metadata()
        else:
            raise ValueError('The specified type does not exist')

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

    def create_insert_into_header_query(
        self,
        q: str = insert_into_video_header_q,
        target_tablename: str = header_table_name
    ) -> str:
        self.insert_query_header = q.format(
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
            self.video_url
            )
        return self.insert_query_header

    def create_insert_into_lines_query(
        self,
        q: str = insert_into_video_lines_q,
        target_tablename: str = lines_table_name
    ) -> str:
        self.insert_query_lines = q.format(
            target_tablename,
            self.channel_id,
            self.video_id,
            self.number_of_views,
            self.number_of_likes
            )
        return self.insert_query_lines

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

    def insert_into_header_table(
        self,
        target_tablename: str = header_table_name
    ) -> None:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        print('Populating: {0} for video_id: \'{1}\''.format(
            target_tablename, self.video_id)
            )
        query = self.create_insert_into_header_query(
            target_tablename=target_tablename
            )

        c.execute(query)
        print('Finishing Transaction on: {0} for video_id: \'{1}\'\n'.format(
            target_tablename, self.video_id)
            )

        conn.commit()
        conn.close()

    def insert_into_lines_table(
        self,
        target_tablename: str = lines_table_name
    ) -> None:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        print('Populating: {0} for video_id: \'{1}\''.format(
            target_tablename, self.video_id)
            )
        query = self.create_insert_into_lines_query(
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
        print('Finished pushing to DB...')

    def meta_push_to_db_header(self) -> None:
        for video_url in self.video_url_list:
            video = TubeVideoLogger(video_url=video_url)
            video_id = video.get_video_id()
            if video_id not in video_ids_exist_in_header_ls:
                video.insert_into_header_table(
                    target_tablename=header_table_name
                    )
        print('Finished pushing to DB for Header Table...')

    def meta_push_to_db_lines(self) -> None:
        for video_url in self.video_url_list:
            video = TubeVideoLogger(video_url=video_url)
            video.insert_into_lines_table(
                target_tablename=lines_table_name
                )
        print('Finished pushing to DB for Lines Table...')

    def combine_video_dataframes(self, kind: str = 'all') -> pd.DataFrame:
        all_videos_df = pd.DataFrame()
        for video_url in self.video_url_list:
            video = TubeVideoLogger(video_url=video_url)
            video_df = video.create_dataframe_for_video(kind=kind)
            all_videos_df = all_videos_df.append(video_df)
        return all_videos_df

    def write_dataframes_to_csv(
        self,
        filename: str,
        kind: str = 'all'
    ) -> None:
        if not os.path.isfile(filename):
            pd.DataFrame().to_csv(filename, index=True)
        all_videos_df = self.combine_video_dataframes(kind=kind)
        try:
            df_history = pd.read_csv(filename, index_col=[0])
            df_history = df_history.append(all_videos_df)
            print('\nUpdating metadata file at: {0}\n'.format(filename))
            df_history.to_csv(filename, index=True)
        except EmptyDataError:
            print('\nUpdating metadata file at: {0}\n'.format(filename))
            all_videos_df.to_csv(filename, index=True)
