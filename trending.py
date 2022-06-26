
import re
from tube.transformer import url_to_bs4

trending_page_url = url_to_bs4(url='https://www.youtube.com/feed/trending')

trending_videos_retrieved = re.findall(
    pattern='(?<=watchEndpoint":{)("videoId":".+?(?="))',
    string=str(trending_page_url)
    )

trending_videos_dict = {}

for idx, vid_id in enumerate(trending_videos_retrieved, start=1):
    video_id = vid_id.split(':')[1].strip('"')
    if video_id not in trending_videos_dict.keys():
        trending_videos_dict[video_id] = idx
