"""
Function for vectorizing features used in training a Linear Regression model.
"""

from pandas import DataFrame
from sklearn.feature_extraction import DictVectorizer


def vectorize_features(training_set: DataFrame, validation_set: DataFrame):
    """
    Accepts training and validation DataFrames, uses DictVectorizer to
    vectorize them for training, returning the X_train sparse matrix, X_val
    array, and the DictVectorizer object.
    """

    dv = DictVectorizer()
    train_dicts = training_set.to_dict(orient="records")
    X_train = dv.fit_transform(train_dicts)

    val_dicts = validation_set[training_set.columns].to_dict(orient="records")
    X_val = dv.transform(val_dicts)

    return X_train, X_val, dv
