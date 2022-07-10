
import os
import re
import pandas as pd
from typing import Dict
from bs4 import BeautifulSoup
from pandas.errors import EmptyDataError

from tube.transformer import (
    url_to_bs4,
    create_youtube_url_from_video_id,
    get_current_datetime
)

datasets_path = os.path.join(os.getcwd(), 'data')

trending_page_url = url_to_bs4(url='https://www.youtube.com/feed/trending')
trending_videos_filename = 'trending_videos_metadata.csv'
trending_videos_path = os.path.join(datasets_path, trending_videos_filename)


def get_current_trending_videos(trending_page_url: BeautifulSoup) -> dict:
    trending_videos_retrieved = re.findall(
        pattern='(?<=watchEndpoint":{)("videoId":".+?(?="))',
        string=str(trending_page_url)
        )

    trending_videos_dict = {}

    for idx, vid_id in enumerate(trending_videos_retrieved, start=1):
        video_id = vid_id.split(':')[1].strip('"')
        if video_id not in trending_videos_dict.keys():
            trending_videos_dict[video_id] = idx

    return trending_videos_dict


def generate_trending_videos_df(
    trending_videos_dict: Dict[str, int]
) -> pd.DataFrame:

    tv_temp = []

    for video_id, trending_position in trending_videos_dict.items():
        video_url = create_youtube_url_from_video_id(video_id)
        datetime = get_current_datetime()
        date = datetime.split(' ')[0]
        tv_temp.append(
            (video_id, video_url, trending_position, date, datetime)
            )
    trending_df = pd.DataFrame(
        tv_temp,
        columns=[
            'video_id',
            'video_url',
            'trending_position',
            'trending_date',
            'trending_datetime'
            ]
        )

    return trending_df


def write_trending_dataframes_to_csv(
    filename: str,
    trending_page_url: str
) -> None:

    trending_videos_dict = get_current_trending_videos(
        trending_page_url=trending_page_url
        )

    if not os.path.isfile(filename):
        pd.DataFrame().to_csv(filename, index=True)
    all_trending_df = generate_trending_videos_df(
        trending_videos_dict=trending_videos_dict
        )
    try:
        df_trending_history = pd.read_csv(filename, index_col=[0])
        df_trending_history = df_trending_history.append(all_trending_df)
        print('\nUpdating metadata file at: {0}\n'.format(filename))
        df_trending_history.to_csv(filename, index=True)
    except EmptyDataError:
        print('\nUpdating metadata file at: {0}\n'.format(filename))
        all_trending_df.to_csv(filename, index=True)


write_trending_dataframes_to_csv(
    filename=trending_videos_path,
    trending_page_url=trending_page_url
    )
