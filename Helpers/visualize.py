

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style("dark")


def plot_date_change_for_col(
    input_df: pd.DataFrame, 
    col: str,
    date_col: str,
    video_id: str
) -> None:
    """ Function to plot the daily changes (based on 'Trending_Date') for
    a numeric column ('col').
    """
    plt.figure(figsize=(10, 10))
    cols = [date_col, col]
    video_df = input_df[input_df['video_id'] == video_id][cols]
    sns.lineplot(data=video_df, x=date_col, y=col)
    plt.xticks(rotation=40)
    plt.title(
        'Change of \'{0}\' per day for VideoId: \'{1}\''.format(col, video_id)
    )
    plt.grid(True, alpha=0.3, c='black')
    plt.show()


def plot_change_in_views_and_likes(
    input_df: pd.DataFrame, 
    video_id: str, 
    views_col: str,
    likes_col: str,
    date_col: str
) -> None:
    """ Function to plot the daily changes (based on 'Trending_Date') for
    a numeric column ('col').
    """
    plt.figure(figsize=(10, 10))
    cols = [date_col, likes_col, views_col]
    video_df = input_df[input_df['video_id'] == video_id][cols]
    sns.lineplot(data=video_df, x=date_col, y=likes_col, 
                 label='Likes', c='tab:cyan')
    sns.lineplot(data=video_df, x=date_col, y=views_col,
                 label='Views', c='tab:orange')
    plt.xticks(rotation=40)
    plt.legend(loc='best')
    plt.ylabel('Count')
    plt.title(
        f'Number of Views and Likes for VideoId: \'{video_id}\'',
        fontweight='bold'
    )
    plt.grid(True, alpha=0.1, color='black')
    plt.show()


def visualize_categorical_feature(input_df: pd.DataFrame,
                                  col_name: str,
                                  hue=None,
                                  return_counts=False,
                                  figsize=(10, 8),
                                  rotation=80):
    ''' Plot the number of observations per category for a specified feature 
    defined by 'col'.

    Parameters
    ----------
        input_df: Dataframe that contains the dataset
        col: Column of the dataframe that will be used by the countplot
    Returns
    -------
        Countplot of the specified variable.
    '''
    size = float(input_df.shape[0])

    if return_counts:
        print(input_df[col_name].value_counts())
    
    plt.figure(figsize=figsize)
    if hue:
        ax = sns.countplot(
            x=col_name, 
            hue=hue, 
            data=input_df, 
            palette=["#d63638", "#3582c4"]
            )
    else:
        palette = ["#d63638", "#3582c4"]
        ax = sns.countplot(x=col_name, data=input_df, palette=palette)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation)
    for p in ax.patches:
        height = p.get_height()
        ax.text(
            p.get_x()+p.get_width()/2., 
            height+5, '{:1.2f}%'.format(105 * height/size), 
            ha='center', 
            fontweight='bold'
            )
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)   
    plt.grid(True, alpha=0.2, color='black')
    plt.title(f'Number of observations per \'{col_name}\'', fontweight='bold')
    plt.show()
