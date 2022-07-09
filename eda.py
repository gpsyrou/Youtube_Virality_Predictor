
from helpers.visualize import (
    plot_date_change_for_col,
    plot_change_in_views_and_likes,
    )
import pandas as pd
import numpy as np
import seaborn as sns
sns.set_style('dark')


# Load lines data
data_loc_lines = 'data/video_lines_metadata.csv'
data_lines = pd.read_csv(data_loc_lines)
data_lines.drop(columns=['Unnamed: 0'], inplace=True)
data_lines.groupby('video_id').size()  # number of samples per video_id
data_lines = data_lines.sort_values('CreatedDatetime').groupby(['video_id', 'CreatedDate']).tail(1)  ## Take only the last entry per day per video_id


# QC that there is no videos that have duplicate lines for the same day
assert len(np.where(data_lines.groupby(['video_id', 'CreatedDate']).size() != 1)[0]) == 0

# Load header data
data_loc_header = 'data/video_header_metadata.csv'
data_header = pd.read_csv(data_loc_header)
data_header.drop(columns=['Unnamed: 0'], inplace=True)
data_header.groupby('video_id').size()  # number of samples per video_id
data_header = data_header.sort_values('CreatedDatetime').groupby(['video_id']).tail(1)  ## Take only the most recent entry per video_id

assert len(np.where(data_header.groupby(['video_id', 'CreatedDate']).size() != 1)[0]) == 0


# Load channels data
data_loc_channels = 'data/channels_metadata.csv'
data_channels = pd.read_csv(data_loc_channels)
data_channels.drop(columns=['Unnamed: 0'], inplace=True)
data_channels = data_channels.sort_values('CreatedDatetime').groupby(['channel_id']).tail(1)  ## Take only the most recent entry per video_id

assert len(np.where(data_channels.groupby(['channel_id']).size() != 1)[0]) == 0


# Merge the datasets
data = data_header.merge(
    data_lines,
    on=['channel_id', 'video_id'],
    how='left',
    suffixes=("_header", "_lines")
    ).merge(
    data_channels,
    on='channel_id',
    how='left'
    )

# Check if join works properly
assert (sorted(list(data_header['video_id'].unique())) == sorted(list(data_lines['video_id'].unique()))) & (sorted(list(data['video_id'].unique())) == sorted(list(data_lines['video_id'].unique())))


# Drop Date columns from Header
data = data.drop(
    columns=[
        'CreatedDate_header',
        'CreatedDatetime_header',
        'CreatedDate',
        'CreatedDatetime']
    )

del data_lines, data_header, data_channels


# Compute the ratio of likes/views per day
data['target'] = data['number_of_likes'] / data['number_of_views']

# Logarithms
data['log_views'] = np.log(data['number_of_views'])
data['log_likes'] = np.log(data['number_of_likes'])


# Compute the daily change in views and likes
data['likes_diff'] = data.groupby(['video_id'])['number_of_likes'].transform(
    lambda x: x.diff(periods=1)
    )

data['views_diff'] = data.groupby(['video_id'])['number_of_views'].transform(
    lambda x: x.diff(periods=1)
    )


# Computing 7-day rolling average
data['seven_d_avg_likes_change'] = data['likes_diff'].rolling(7).mean()
data['seven_d_avg_views_change'] = data['views_diff'].rolling(7).mean()

# Compute z-scores for vies and likes
from scipy.stats import zscore
data['z_norm_views'] = zscore(data['number_of_views'])
data['z_norm_likes'] = zscore(data['number_of_likes'])

#

def get_timeseries_for_video_id(
        input_df: pd.DataFrame,
        video_id: str,
        col: str
) -> pd.Series:
    ts = input_df[input_df['video_id'] == video_id][col]
    return ts


get_timeseries_for_video_id(
    input_df=data,
    video_id='sPA3XIbho_A',
    col='target'
    )


ts = get_timeseries_for_video_id(
    input_df=data,
    video_id='sPA3XIbho_A',
    col='number_of_views'
    )


plot_date_change_for_col(
    input_df=data,
    col='log_views',
    date_col='CreatedDate_lines',
    video_id='sPA3XIbho_A'
    )

plot_date_change_for_col(
    input_df=data,
    col='log_views',
    date_col='CreatedDate_lines',
    video_id='RjrA-slMoZ4'
    )

plot_date_change_for_col(
    input_df=data,
    col='number_of_views',
    date_col='CreatedDate_lines',
    video_id='bNhGDDUnNE8'
    )

plot_date_change_for_col(
    input_df=data,
    col='likes_diff',
    date_col='CreatedDate_lines',
    video_id='oTw8AECmUNA'
    )


plot_date_change_for_col(
    input_df=data,
    col='seven_d_avg_likes_change',
    date_col='CreatedDate_lines',
    video_id='RjrA-slMoZ4'
    )


plot_change_in_views_and_likes(
    input_df=data,
    video_id='RjrA-slMoZ4',
    views_col='log_views',
    likes_col='log_likes',
    date_col='CreatedDate_lines'
    )

plot_change_in_views_and_likes(
    input_df=data,
    video_id='RjrA-slMoZ4',
    views_col='z_norm_views',
    likes_col='z_norm_likes',
    date_col='CreatedDate_lines',
    sharey=False
    )
