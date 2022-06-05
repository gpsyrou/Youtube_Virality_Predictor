"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Purpose: Module to perform validation and automatic quality assurance checks
during population/retrieval of the data from YouTube.
"""
import pandas as pd
from typing import List


def get_id_from_url(url: str) -> str:
    return url.split('/')[-1]


def transform_json_urls_to_video_ids(catalog: dict) -> List[str]:
    urls_ls = [x['url'] for x in catalog['videos']]
    urls_ls = list(set(map(get_id_from_url, urls_ls)))
    return urls_ls


def retrieve_list_of_videos(filename: str, col: str = 'video_id') -> List[str]:
    data = pd.read_csv(filename, usecols=[col])
    vals = list(set(data[col]))
    return vals


def retrieve_list_of_existing_channels(
    filename: str,
    cols: str = ['channel_id', 'channel_name']
) -> tuple:
    data = pd.read_csv(filename, usecols=cols)
    vals_ids = list(set(data[cols[0]]))
    vals_names = list(set(data[cols[1]]))
    return (vals_ids, vals_names)


def is_header_lines_coverage_complete(
    header_f: str,
    lines_f: str,
    col: str = 'video_id'
) -> bool:
    header = retrieve_list_of_videos(filename=header_f, col=col)
    lines = retrieve_list_of_videos(filename=lines_f, col=col)
    intersect_len = len(list(set(header) & set(lines)))

    return intersect_len == len(header) == len(lines)


def is_header_synced_with_catalog(
    header_f: str,
    catalog: dict,
    col: str = 'video_id'
) -> bool:
    header = retrieve_list_of_videos(filename=header_f, col=col)
    catalog = transform_json_urls_to_video_ids(catalog)
    intersect_len = len(list(set(header) & set(catalog)))

    return intersect_len == len(header) == len(catalog)
