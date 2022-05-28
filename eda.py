
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')
from helpers.df_func import print_dataset_size
from helpers.visualize import (
    plot_date_change_for_col, 
    plot_change_in_views_and_likes,
    visualize_categorical_feature
    )
from features.feature_preprocess import is_title_full_capital, extract_tags, get_tag_size


data_loc_lines = '/Users/georgiosspyrou/Desktop/GitHub/Projects/Youtube_Likes_Predictor/video_lines_metadata.csv'
data = pd.read_csv(data_loc_lines)
data.drop(columns=['Unnamed: 0'], inplace=True)
data.head(10)
data[data['video_id'] == 'sPA3XIbho_A']
data[data['video_id'] == 'sPA3XIbho_A']['number_of_views']

data['Target'] = data['number_of_likes'] / data['number_of_views']

data.video_id.unique()



plot_date_change_for_col(input_df=data, col='number_of_views', date_col='CreatedDate', video_id='sPA3XIbho_A')
plot_date_change_for_col(input_df=data, col='number_of_views', date_col='CreatedDate', video_id='oTw8AECmUNA')


plot_change_in_views_and_likes(
    input_df=data, 
    video_id='sPA3XIbho_A', 
    views_col='number_of_views', 
    likes_col='number_of_likes', 
    date_col='CreatedDate'
    ) # Need to normalize



















