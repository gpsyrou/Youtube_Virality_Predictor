""" 
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""

from tube.metadata import MetadataCollector
import pandas as pd
import json

video_url = 'https://youtu.be/yzTuBuRdAyA'
video_url_2 = 'https://youtu.be/MOMthW49TU0'


class TubeConnector(MetadataCollector):
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

v1 = TubeConnector(video_url=video_url)
v2 = TubeConnector(video_url=video_url_2)

v1.data
v2.data


v1.create_dataframe_for_video()
v1.create_json_line_for_video()
