from sklearn.model_selection import train_test_split
# Hi

def split_df(df):

    df_train, df_val = train_test_split(df, test_size=0.2, random_state=3)

    df_train.reset_index(drop=True)
    df_val.reset_index(drop=True)

    y_train = df_train.fail.values
    y_val = df_val.fail.values

    del df_train['fail']

    return df_train, df_val, y_train, y_val
    