""" 
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Purpose: A collection of classes/methods to efficiently connect to youtube 
videos and retrieve metadata information, such as number of views, channel_id,
upload date and more.
"""


import urllib.request
from typing import List
from bs4 import (BeautifulSoup, element)
from tube.transformer import transform_pt_format


class YoutubeMetaDataRetriever:
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

      
    def __get_video_url__(self) -> str:
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
    
    
    def get_video_duration(
            self, 
            duration_map={'itemprop': 'duration'}, 
            target_format: str = 'minutes'
    ) -> int:
        self.video_duration = self.video_bsoup.find('meta', attrs=duration_map)
        self.video_duration = self.video_duration.get('content')
        self.video_duration = transform_pt_format(
            pt=self.video_duration, 
            target_format=target_format
            )

        return self.video_duration 

  
    def get_published_date(
            self, publishdt_map={'itemprop': 'datePublished'}
    ) -> str:
        self.publised_date = self.video_bsoup.find('meta', attrs=publishdt_map)
        self.publised_date = self.publised_date.get('content')

        return self.publised_date

    
    def get_upload_date(self, uploaddt_map={'itemprop': 'uploadDate'}) -> str:
        self.upload_date = self.video_bsoup.find('meta', attrs=uploaddt_map)
        self.upload_date = self.upload_date.get('content')

        return self.upload_date

    
    def get_video_genre(self, video_genre_map={'itemprop': 'genre'}) -> str:
        self.video_genre = self.video_bsoup.find('meta', attrs=video_genre_map)
        self.video_genre = self.video_genre.get('content')

        return self.video_genre

    
    def get_regions_allowed(
            self,
            regions_map={'itemprop': 'regionsAllowed'}
    ) -> List[str]:
        self.regions_allowed = self.video_bsoup.find('meta', attrs=regions_map)
        self.regions_allowed = self.regions_allowed.get('content')
        self.regions_allowed = list(self.regions_allowed.split(","))

        return self.regions_allowed
