""" Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""

from tube.metadata import YoutubeMetaDataRetriever, MetadataCollector
from tube.transformer import get_current_datetime
import pandas as pd
from typing import Dict, Any

video_url = 'https://youtu.be/yzTuBuRdAyA'

hills = MetadataCollector(video_url=video_url)
hills.collect_date_metadata()
hills.collect_id_metadata()
hills.collect_description_metadata()
hills.collect_variable_metadata()



class TubeConnector(MetadataCollector):
    def __init__(self, video_url: str):
        MetadataCollector.__init__(self, video_url=video_url)
        
    def merge_video_meta_info(self) -> Dict[str, Any]:
        dates = self.collect_date_metadata()
        ids = self.collect_id_metadata()
        descr = self.collect_description_metadata()
        var = self.collect_variable_metadata()
        
        return {**ids, **descr, **dates, **var}
        
    def create_dataframe_for_video(self) -> pd.DataFrame:
        meta_info_dict = self.merge_video_meta_info()        
        df = pd.DataFrame.from_records([meta_info_dict])
        
        return df
    
v = TubeConnector(video_url=video_url)      
v.merge_video_meta_info()
v.create_dataframe_from_meta_info()