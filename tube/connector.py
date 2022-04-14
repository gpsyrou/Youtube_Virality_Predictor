""" Package to collect metadata for Youtube Videos and apply formatting and
transformations to prepare the data for further analysis.
"""

import tube.metadata as meta

video_url = 'https://youtu.be/yzTuBuRdAyA'


hills = meta.YoutubeMetaDataRetriever(video_url=video_url)

hills.__meta_content_tags__()
hills.get_video_description()
hills.get_video_duration(target_format='minutes')
hills.get_duration_in_pt()

hills = meta.MetadataCollector(video_url=video_url)
hills.collect_date_metadata()
hills.collect_id_metadata()
