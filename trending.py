
import os
import re
import pandas as pd
from tube.transformer import (
    url_to_bs4,
    create_youtube_url_from_video_id,
    get_current_datetime
)

datasets_path = os.path.join(os.getcwd(), 'data')

trending_page_url = url_to_bs4(url='https://www.youtube.com/feed/trending')
trending_videos_filename = 'trending_videos_metadata.csv'
trending_videos_path = os.path.join(datasets_path, trending_videos_filename)

trending_videos_retrieved = re.findall(
    pattern='(?<=watchEndpoint":{)("videoId":".+?(?="))',
    string=str(trending_page_url)
    )

trending_videos_dict = {}

for idx, vid_id in enumerate(trending_videos_retrieved, start=1):
    video_id = vid_id.split(':')[1].strip('"')
    if video_id not in trending_videos_dict.keys():
        trending_videos_dict[video_id] = idx

tv_temp = []

for video_id, trending_position in trending_videos_dict.items():
    video_url = create_youtube_url_from_video_id(video_id)
    datetime = get_current_datetime()
    date = datetime.split(' ')[0]
    tv_temp.append((video_id, video_url, trending_position, date, datetime))

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

trending_df.to_csv(trending_videos_path, index=True)
