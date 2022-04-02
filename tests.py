
import unittest
import numpy as np
from tube.connection import YoutubeMetaDataRetriever

video_url = 'https://youtu.be/iByQSaWTR1g'



class TestHighLevelInfo(unittest.TestCase):
    
    def testVideoURLImport(
            self, 
            err_msg: str = 'Video URL is not imported properly'
    ):
        video = YoutubeMetaDataRetriever(video_url=video_url)
        video_url_check = video.__get_video_url__()
        self.assertEqual(video_url_check, video_url, msg=err_msg)

