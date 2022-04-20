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

db_name = 'TubeDB.sqlite'
metadata_table_name = 'TubeMetadata'
config_filepath = os.path.join(os.getcwd(), 'config/video_catalog.json')

with open(config_filepath) as video_catalog:
    catalog = json.load(video_catalog)

video_url = catalog['videos'][0].get('url')
video_url


class TubeLogger(MetadataCollector):
    def __init__(self, video_url: str):
        MetadataCollector.__init__(self, video_url=video_url)
        self.data = self.merge_video_meta_info()

    def create_dataframe_for_video(self) -> pd.DataFrame:
        meta_info_dict = self.merge_video_meta_info()
        df = pd.DataFrame.from_records([meta_info_dict])

        return df

    def create_json_line_for_video(self) -> str:
        jason_line = json.dumps(self.data)
        return jason_line

    def insert_into_metadata_table(
            self,
            q: str = insert_into_q,
            target_tablename: str = metadata_table_name
    ) -> None:

        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        print('Populating {0}...'.format(target_tablename))
        query = q.format(
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

        c.execute(query)
        print('Finishing Transaction on {0}...'.format(target_tablename))

        conn.commit()
        conn.close()


class MultiTubeWritter:
    def __init_(self, video_collection):
        self.video_collection = video_collection

    def multivideo_meta_push_to_db() -> None:
        pass


v1 = TubeLogger(video_url=video_url)
v1.insert_into_metadata_table()
