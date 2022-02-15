
import pandas as pd
import seaborn as sns
sns.set_style("dark")
import matplotlib.pyplot as plt


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


def plot_change_in_views_and_likes(
    input_df: pd.DataFrame, video_id: str, overlay_target=True
    ) -> None:
    """ Function to plot the daily changes (based on 'Trending_Date') for
    a numeric column ('col').
    """
    plt.figure(figsize=(10, 10))
    cols=['trending_date', 'target', 'likes', 'view_count']
    video_df = input_df[input_df['video_id'] == video_id][cols]
    sns.lineplot(data=video_df, x='trending_date', y='likes', 
                 label='Likes', c='tab:cyan')
    sns.lineplot(data=video_df, x='trending_date', y='view_count',
                 label='Views', c='tab:orange')
    if overlay_target:
        sns.lineplot(data=video_df, x='trending_date', y='target',
                     label='Target (Likes/Views)', c='tab:red')
    plt.xticks(rotation=40)
    plt.legend(loc='best')
    plt.ylabel('Count')
    plt.title(
        f'Number of Views and Likes for VideoId: \'{video_id}\'',
        fontweight='bold'
    )
    plt.grid(True, alpha=0.1, color='black')
    plt.show()
