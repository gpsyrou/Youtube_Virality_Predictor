
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')
from helpers.df_func import print_dataset_size
from helpers.visualize import (
    plot_trending_date_change_for_col, 
    plot_change_in_views_and_likes,
    visualize_categorical_feature
    )
from features.feature_preprocess import is_title_full_capital

project_path = '/Users/georgiosspyrou/Desktop/GitHub/Projects/Youtube_Likes_Predictor'
data_folder = 'Data'

train_data_filename = 'train.parquet'
test_data_filename = 'train.parquet'

youtube_df_train = pd.read_parquet(
    os.path.join(project_path, data_folder, train_data_filename)
    )

print_dataset_size(input_df=youtube_df_train)

youtube_df_train.head(5)

youtube_df_train.dtypes

youtube_df_train['trending_date'] = pd.to_datetime(youtube_df_train['trending_date'])

# Produce summary statistics for all columns in the dataset
df_stats = youtube_df_train.describe(include='all')

youtube_df_train['comments_disabled'].value_counts()
youtube_df_train['ratings_disabled'].value_counts()

list(youtube_df_train.columns)

youtube_df_train.iloc[0]

num_lines_per_channel_id = youtube_df_train['channelId'].value_counts().reset_index()

num_lines_per_channel_id.rename(
    columns={'index': 'channelId', 'channelId': 'count'},
    inplace=True
    )

num_lines_per_video_id = youtube_df_train['video_id'].value_counts().reset_index()

num_lines_per_video_id.rename(
    columns={'index': 'video_id', 'video_id': 'count'},
    inplace=True
    )

youtube_df_train.groupby('video_id').count()
test_case = youtube_df_train[youtube_df_train['video_id'] == 'zzd4ydafGR0']

test_case['likes'].iloc[0] / test_case['view_count'].iloc[0]
test_case['target'].iloc[0]

plot_trending_date_change_for_col(
    input_df=youtube_df_train, 
    video_id='zzd4ydafGR0', 
    col='target'
    )

plot_trending_date_change_for_col(
    input_df=youtube_df_train,  
    video_id='zzd4ydafGR0', 
    col='view_count'
    )

plot_change_in_views_and_likes(
    input_df=youtube_df_train, 
    video_id='H1tQhK0n5Qk', 
    overlay_target=True
    )

youtube_df_train['title'][0]

youtube_df_train.groupby('comments_disabled')['target'].mean()
youtube_df_train.groupby('has_thumbnail')['target'].mean()

visualize_categorical_feature(input_df=youtube_df_train, col_name='has_thumbnail', hue=None, return_counts=True)








