"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Purpose: A collection of classes/methods to efficiently connect to youtube
videos and retrieve metadata information, such as number of views, channel_id,
upload date and more.
"""


import re
import numpy as np
from typing import Dict, Any
from bs4 import element
from tube.transformer import transform_pt_format, remove_chars, url_to_bs4


class TubeVideoMetaDataRetriever:
    """ Class to retrieve and analyzer information of Youtube videos.
    """
    def __init__(self, video_url: str):
        self.video_url = video_url
        self.video_bsoup = url_to_bs4(video_url=video_url)

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
        self.title = remove_chars(self.title)

        return self.title

    def get_video_description(
            self,
            descr_map={'property': 'og:description'}) -> str:
        self.description = self.video_bsoup.find('meta', attrs=descr_map)
        self.description = self.description.get('content')
        self.description = remove_chars(self.description)

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

    def get_duration_in_pt(self, duration_map={'itemprop': 'duration'}) -> str:
        self.pt_format = self.video_bsoup.find('meta', attrs=duration_map)
        self.pt_format = self.pt_format.get('content')
        return self.pt_format

    def get_video_duration(
            self,
            duration_map={'itemprop': 'duration'},
            target_format: str = 'minutes'
    ) -> float:
        self.pt_format = self.get_duration_in_pt(duration_map=duration_map)
        video_duration = transform_pt_format(
            pt=self.pt_format,
            target_format=target_format
            )
        self.video_duration = np.round(video_duration, 4)

        return self.video_duration

    def get_published_date(
            self, publishdt_map={'itemprop': 'datePublished'}
    ) -> str:
        self.published_date = self.video_bsoup.find(
            'meta',
            attrs=publishdt_map
            )
        self.published_date = self.published_date.get('content')

        return self.published_date

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
    ) -> str:
        self.regions_allowed = self.video_bsoup.find('meta', attrs=regions_map)
        self.regions_allowed = self.regions_allowed.get('content')

        return str(self.regions_allowed)

    def get_current_number_of_likes(self):
        breaker = str(self.video_bsoup).find('likes')
        likes_text = str(self.video_bsoup)[breaker-20:breaker+5]
        number_of_likes = re.findall(r'[\d,]+.', likes_text)[0].strip()
        self.number_of_likes = int(number_of_likes.replace(',', ''))
        return self.number_of_likes


class VideoMetadataCollector(TubeVideoMetaDataRetriever):
    def __init__(self, video_url: str):
        TubeVideoMetaDataRetriever.__init__(self, video_url=video_url)

    def collect_variable_metadata(self) -> Dict[str, int]:
        """ Returns a collection of video information that is variable in time.

        Returns:
        -------
            number_of_views
        """
        number_of_views = self.get_current_number_of_views()
        number_of_likes = self.get_current_number_of_likes()

        variable_dict = {'number_of_views': number_of_views, 
                         'number_of_likes': number_of_likes}

        return variable_dict

    def collect_id_metadata(self) -> Dict[str, str]:
        """ Returns a collection of video information around identification
        parameters.

        Returns:
        -------
            channel_id, video_id
        """
        channel_id = self.get_channel_id()
        video_id = self.get_video_id()
        video_url = self.__get_video_url__()

        id_dict = {
            'channel_id': channel_id,
            'video_id': video_id,
            'video_url': video_url
            }

        return id_dict

    def collect_description_metadata(
        self
    ) -> Dict[str, Any]:
        """ Returns a collection of parameters that correspond to video's
        description.

        Returns:
        -------
            title, description, thumb, duration, genre, regions
        """
        title = self.get_video_title()
        description = self.get_video_description()
        thumb = self.get_thumbnail_link()
        duration = self.get_video_duration()
        genre = self.get_video_genre()
        regions = self.get_regions_allowed()

        desc_dict = {'title': title, 'description': description,
                     'thumbnail': thumb, 'duration': duration,
                     'genre': genre, 'regions': regions}

        return desc_dict

    def collect_date_metadata(self) -> Dict[str, str]:
        """ Returns a collection parameters related to date information about
        the video.

        Returns:
        -------
            date_dict: {published_date, upload_date}
        """
        publ_date = self.get_published_date()
        upload_date = self.get_upload_date()

        date_dict = {'published_date': publ_date, 'upload_date': upload_date}

        return date_dict

    def merge_video_meta_info(self) -> Dict[str, Any]:
        dates = self.collect_date_metadata()
        ids = self.collect_id_metadata()
        descr = self.collect_description_metadata()
        var = self.collect_variable_metadata()

        return {**ids, **descr, **dates, **var}


class TubeChannelMetaDataRetriever:
    """ Class to retrieve and analyzer information of Youtube channels.
    """
    def __init__(self, channel_url: str):
        self.channel_url = channel_url
        self.channel_bsoup = url_to_bs4(url=channel_url)

    def __meta_content_tags__(self) -> element.ResultSet:
        return self.channel_bsoup.find_all('meta')

    def __get_channel_url__(self) -> str:
        pass
