"""
Author: Georgios Spyrou (georgios.spyrou1@gmail.com")

Purpose: Module to perform validation and automatic quality assurance checks
during population/retrieval of the data from YouTube.
"""
import os
import json
import pandas as pd
from typing import List

CONFIGS_PATH = os.path.join(os.getcwd(), 'config')

catalog_path = os.path.join(CONFIGS_PATH, 'video_catalog.json')
params_path = os.path.join(CONFIGS_PATH, 'param.json')

with open(catalog_path) as video_catalog_json:
    catalog = json.load(video_catalog_json)
    video_catalog_json.close()

with open(params_path) as params_json:
    params = json.load(params_json)
    params_json.close()

db_name = params['database_name']
metadata_table_name = params['meta_table_name']
header_table_name = params['header_table_name']
lines_table_name = params['lines_table_name']
header_f = params['header_csv_filename']
lines_f = params['lines_csv_filename']


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
