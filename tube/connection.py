
import pandas as pd
import urllib.request
import time
import re
from dateutil.parser import isoparse
from datetime import datetime
from typing import List, Mapping
from bs4 import (BeautifulSoup,
                 element)



class YoutubeAnalyzer:
    """ Class to retrieve and analyzer information of Youtube videos.
    """
    def __init__(self, video_url: str):
        self.video_url = video_url
        self.video_bsoup = self.url_to_bs4(video_url=video_url)


    def url_to_bs4(self, video_url: str) -> BeautifulSoup:
        """
        Given a website link (URL), retrieve the corresponding website in an 
        html format.
        Parameters
        ----------
        video_url : str
            URL of the webpage that will be transformed to a BeautifulSoup obj.
        """
        #print('Attempting to retrieve HTML object for {0}'.format(video_url))
        request = urllib.request.urlopen(video_url)
        if request.getcode() != 200:
            raise Exception('Can not communicate with the client')        
        else:
            response = request.read()
            response_html = BeautifulSoup(response, 'html.parser')
            return response_html


    def __meta_content_tags__(self) -> element.ResultSet:
        return self.video_bsoup.find_all('meta')

      
    def _get_video_url(self) -> str:
        return self.video_url

  
    def get_current_number_of_views(
            self, 
            views_map={'itemprop': 'interactionCount'}) -> int:
        views_tags = self.video_bsoup.find_all('meta', attrs=views_map)
        self.number_of_views = int(views_tags[0].get('content'))
        return self.number_of_views


    def get_video_title(self, title_map={'name': 'title'}) -> str:
        title_tags = self.video_bsoup.find_all('meta', attrs=title_map)
        self.title = title_tags[0].get('content')
        return self.title

    def get_video_description(
            self, 
            descr_map={'property': 'og:description'}) -> str:
        self.description = self.video_bsoup.find('meta', attrs=descr_map)
        self.description = self.description.get('content')
        return self.description 

    def get_thumbnail_link(self, thumbn_map={'property': 'og:image'}) -> str:
        self.thumbnail = self.video_bsoup.find('meta', attrs=thumbn_map)
        self.thumbnail = self.thumbnail.get('content')
        return self.thumbnail 

    
    def get_channel_id(self, channel_map={'itemprop': 'channelId'}) -> str:
        self.channel_id = self.video_bsoup.find('meta', attrs=channel_map)
        self.channel_id = self.channel_id.get('content')
        return self.channel_id
    
    def get_video_id(self, video_id_map={'itemprop': 'videoId'}) -> str:
        self.video_id = self.video_bsoup.find('meta', attrs=video_id_map)
        self.video_id = self.video_id.get('content')
        return self.video_id
    
    
    def get_video_duration(self):
        pass
    
    
    def get_published_date(self):
        pass
    
    def get_upload_date(self):
        pass
    
    def get_video_genre(self):
        pass

    
pryda_loving_you = YoutubeAnalyzer(video_url='https://youtu.be/iByQSaWTR1g')

pryda_loving_you._get_video_url()
pryda_loving_you.__meta_content_tags__()
pryda_loving_you.get_current_number_of_views()
pryda_loving_you.get_video_title()
pryda_loving_you.get_video_description()
pryda_loving_you.get_thumbnail_link()