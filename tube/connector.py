"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""

import pandas as pd
import json
import sqlite3
from tube.metadata import MetadataCollector
from database.db import insert_into_q


db_name = 'TubeDB.sqlite'
metadata_table_name = 'TubeMetadata'

conn = sqlite3.connect(db_name)
c = conn.cursor()

video_url = 'https://youtu.be/yzTuBuRdAyA'
video_url_2 = 'https://youtu.be/MOMthW49TU0'


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
            self.number_of_views
            )

        c.execute(query)
        print('Finishing Transaction on {0}...'.format(target_tablename))

        conn.commit()
        conn.close()


v1 = TubeLogger(video_url=video_url)
v2 = TubeLogger(video_url=video_url_2)


v1.insert_into_metadata_table()
v2.insert_into_metadata_table()
