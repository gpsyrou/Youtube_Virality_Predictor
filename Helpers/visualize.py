
from features.feature_preprocess import get_title_from_video_id
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
    title = get_title_from_video_id(input_df=input_df, video_id=video_id)
    sns.lineplot(data=video_df, x=date_col, y=col, marker='o')
    plt.xticks(rotation=40)
    plt.title(
        'Change of \'{0}\' per day for VideoId: \'{1}\' \n {2}'.format(
            col, video_id, title
            ), fontweight='bold'
            )
    plt.grid(True, alpha=0.3, c='black')
    plt.show()


def plot_change_in_views_and_likes(
    input_df: pd.DataFrame,
    video_id: str,
    views_col: str,
    likes_col: str,
    date_col: str,
    sharey: bool = False
) -> None:
    """ Function to plot the daily changes (based on 'Trending_Date') for
    a numeric column ('col').
    """
    cols = [date_col, likes_col, views_col]
    video_df = input_df[input_df['video_id'] == video_id][cols]

    f, axs = plt.subplots(
        1,
        2,
        figsize=(12, 12),
        sharey=sharey,
        gridspec_kw=dict(width_ratios=[3, 3])
        )

    sns.lineplot(
        data=video_df,
        x=date_col,
        y=likes_col,
        label='Likes',
        c='tab:cyan',
        marker='o',
        ax=axs[0]
        )
    sns.lineplot(
        data=video_df,
        x=date_col,
        y=views_col,
        label='Views',
        c='tab:orange',
        marker='o',
        ax=axs[1]
        )

    plt.setp(axs[0].xaxis.get_majorticklabels(), rotation=45)
    plt.setp(axs[1].xaxis.get_majorticklabels(), rotation=45)
    axs[0].grid(True, alpha=0.2, color='black')
    axs[1].grid(True, alpha=0.2, color='black')
    f.tight_layout()
    plt.suptitle(
        f'Number of Views and Likes for VideoId: \'{video_id}\'',
        fontweight='bold'
    )
    f.subplots_adjust(top=0.95)
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
