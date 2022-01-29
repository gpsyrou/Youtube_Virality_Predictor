
import os
import pandas as pd
from Helpers.eda_helpers import print_dataset_size

project_path = '/Users/georgiosspyrou/Desktop/GitHub/Projects/Youtube_Likes_Predictor'
data_folder = 'Data'

train_data_filename = 'train.parquet'
test_data_filename = 'train.parquet'

youtube_df = pd.read_parquet(os.path.join(project_path, data_folder, train_data_filename))

print_dataset_size(input_df=youtube_df)




youtube_df.head(5)
df_stats = youtube_df.describe()
list(youtube_df.columns)
youtube_df.dtypes
youtube_df.iloc[0]



