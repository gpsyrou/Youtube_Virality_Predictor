
import pandas as pd
import urllib
import time
import re
from dateutil.parser import isoparse
from datetime import datetime
from typing import List, Mapping
from bs4 import (BeautifulSoup,
                 element)



class YoutubeAnalyzer:
    def __init__(self, video_url: str):
        self.video_url = video_url
        self.video_bsoup = self.url_to_bs4(video_url=video_url)
 
    def url_to_bs4(self, video_url: str) -> BeautifulSoup:
        """
        Given a website link (URL), retrieve the corresponding website in an html
        format.
        Parameters
        ----------
        video_url : str
            URL of the webpage that will be transformed to a BeautifulSoup object.
        """
        #print('Attempting to retrieve HTML object for {0}'.format(video_url))
        request = urllib.request.urlopen(video_url)
        if request.getcode() != 200:
            raise Exception('Can not communicate with the client')        
        else:
            response = request.read()
            response_html = BeautifulSoup(response, 'html.parser')
            return response_html

       
    def _get_video_url(self) -> str:
        return self.video_url
    
    def get_current_number_of_views(self, views_map={'itemprop': 'interactionCount'}) -> int:
        number_of_views = self.video_bsoup.find_all('meta', attrs=views_map)[0].get('content')
        return number_of_views




t
pryda_loving_you = YoutubeAnalyzer(video_url='https://youtu.be/iByQSaWTR1g')

pryda_loving_you._get_video_url()