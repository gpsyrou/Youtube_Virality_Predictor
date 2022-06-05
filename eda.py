
from helpers.visualize import (
    plot_date_change_for_col,
    plot_change_in_views_and_likes,
    )
import pandas as pd
import seaborn as sns
sns.set_style('dark')


# Load lines data
data_loc_lines = 'video_lines_metadata.csv'
data_lines = pd.read_csv(data_loc_lines)
data_lines.drop(columns=['Unnamed: 0'], inplace=True)


# Load header data
data_loc_header = 'video_header_metadata.csv'
data_header = pd.read_csv(data_loc_header)
data_header.drop(columns=['Unnamed: 0'], inplace=True)

# Load channels data
data_loc_channels = 'channels_metadata.csv'
data_channels = pd.read_csv(data_loc_channels)
data_channels.drop(columns=['Unnamed: 0'], inplace=True)


# Merge the dataset
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
assert (list(data_header['video_id'].unique()) == list(data_lines['video_id'].unique())) & (list(data['video_id'].unique()) == list(data_lines['video_id'].unique()))


# Drop Date columns from Header
data = data.drop(
    columns=[
        'CreatedDate_header',
        'CreatedDatetime_header',
        'CreatedDate',
        'CreatedDatetime']
    )
del data_lines
del data_header
del data_channels

# Compute the ratio of likes/views per day
data['target'] = data['number_of_likes'] / data['number_of_views']


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


plot_date_change_for_col(
    input_df=data,
    col='number_of_views',
    date_col='CreatedDate_lines',
    video_id='sPA3XIbho_A'
    )

plot_date_change_for_col(
    input_df=data,
    col='number_of_views',
    date_col='CreatedDate_lines',
    video_id='oTw8AECmUNA'
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
    video_id='oTw8AECmUNA'
    )


plot_change_in_views_and_likes(
    input_df=data,
    video_id='3S1jrYq87Zw',
    views_col='number_of_views',
    likes_col='number_of_likes',
    date_col='CreatedDate_lines'
    )
