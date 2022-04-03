
import unittest
import numpy as np
from tube.connector import YoutubeMetaDataRetriever

video_url = 'https://youtu.be/iByQSaWTR1g'


class TestMainInfo(unittest.TestCase):
    
    def testVideoURLImport(
            self, 
            err_msg: str = 'Video URL is not imported properly'
    ):
        video = YoutubeMetaDataRetriever(video_url=video_url)
        video_url_check = video.__get_video_url__()
        self.assertEqual(video_url_check, video_url, msg=err_msg)


class TestMetaDataRetrievalInfo(unittest.TestCase):
    

    def testDurationTransformationMinutes(
            self,
            err_msg: str = 'Duration has not been transformed properly'
    ):
        video = YoutubeMetaDataRetriever(video_url=video_url)
        duration = video.get_video_duration(target_format='minutes')
        self.assertEqual(8.1333, np.round(duration, 4), msg=err_msg)


    def testDurationTransformationSeconds(
            self,
            err_msg: str = 'Duration has not been transformed properly'
    ):
        video = YoutubeMetaDataRetriever(video_url=video_url)
        duration = video.get_video_duration(target_format='seconds')
        self.assertEqual(488, duration, msg=err_msg)
