
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from helpers.eda import print_dataset_size

project_path = '/Users/georgiosspyrou/Desktop/GitHub/Projects/Youtube_Likes_Predictor'
data_folder = 'Data'

train_data_filename = 'train.parquet'
test_data_filename = 'train.parquet'

youtube_df_train = pd.read_parquet(
    os.path.join(
        project_path, data_folder, train_data_filename
    )
)

print_dataset_size(input_df=youtube_df_train)

youtube_df_train.head(5)

youtube_df_train.dtypes

youtube_df_train['trending_date'] = pd.to_datetime(youtube_df_train['trending_date'])

# Produce summary statistics for all columns in the dataset
df_stats = youtube_df_train.describe(include='all')

list(youtube_df_train.columns)

youtube_df_train.iloc[0]

num_lines_per_channel_id = youtube_df_train['channelId'].value_counts().reset_index()
num_lines_per_channel_id.rename(columns={'index': 'channelId', 'channelId': 'count'}, inplace=True)

num_lines_per_video_id = youtube_df_train['video_id'].value_counts().reset_index()
num_lines_per_video_id.rename(columns={'index': 'video_id', 'video_id': 'count'}, inplace=True)


youtube_df_train.groupby('video_id').count()
test_case = youtube_df_train[youtube_df_train['video_id'] == 'zzd4ydafGR0']

test_case['likes'].iloc[0] / test_case['view_count'].iloc[0]
test_case['target'].iloc[0]



def plot_trending_date_change_for_col(
    input_df: pd.DataFrame,
    col: str, 
    video_id: str
    ) -> None:
    """ Function to plot the daily changes (based on 'Trending_Date') for
    a numeric column ('col').
    """
    plt.figure(figsize=(10, 10))
    cols=['trending_date', col]
    video_df = input_df[input_df['video_id'] == video_id][cols]
    sns.lineplot(data=video_df, x='trending_date', y=col)
    plt.xticks(rotation=40)
    plt.title(
        'Change of {0} per day for VideoId: \'{1}\''.format(col, video_id)
    )
    plt.show()


plot_trending_date_change_for_col(
    input_df=youtube_df_train, 
    video_id='zzd4ydafGR0', 
    col='target'
    )

