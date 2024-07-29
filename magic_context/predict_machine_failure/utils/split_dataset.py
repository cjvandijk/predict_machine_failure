from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

"""
Function for splitting dataset into test and train sets
"""


def split_df(
    df: pd.DataFrame,
) -> Tuple(pd.DataFrame, list[int], pd.DataFrame, list[int]):
    """
    Splits dataframe into train and test dataframes and target values
    """

    df_train, df_val = train_test_split(df, test_size=0.2, random_state=3)

    df_train.reset_index(drop=True)
    df_val.reset_index(drop=True)

    y_train = df_train.fail.values
    y_val = df_val.fail.values

    del df_train["fail"]

    return df_train, df_val, y_train, y_val
