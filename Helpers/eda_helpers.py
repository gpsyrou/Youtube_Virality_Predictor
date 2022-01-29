import pandas as pd

def print_dataset_size(input_df: pd.DataFrame) -> None:
    df_num_rows, df_num_columns = input_df.shape[0], input_df.shape[1]
    print(
        'There are {0} rows and {1} columns in the dataset'.format(
            df_num_rows, df_num_columns
        )
    )
