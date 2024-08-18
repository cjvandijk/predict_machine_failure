"""
This is a Mage block, which runs in the pipeline to
train the model after data was prepared in the block preceeding
this one. It also tracks the training experiment with MLFlow.
"""

import os
import pickle
from pathlib import Path

import mlflow
from pandas import DataFrame
from predict_machine_failure.utils import encode, split_dataset
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression


if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def start_train(df: DataFrame) -> tuple[DictVectorizer, LinearRegression]:
    """
    Trains a linear regression model. Prints the intercept for homework answer.

    Args:
        df: output from the upstream parent block

    Returns:
        dv: the DictVectorizer made from the train_df data
        lr: the linear regression model
    """

    mlflow.set_tracking_uri(uri="http://mlflow:5000")
    mlflow.set_experiment("train_model_thru_mage")
    mlflow.sklearn.autolog(log_datasets=False)

    with mlflow.start_run():
        df_train, df_val, y_train, y_val = split_dataset.split_df(df)
        X_train, X_val, dv = encode.vectorize_features(df_train, df_val)

        lr = LinearRegression()

        lr.fit(X_train, y_train)

        model_path = Path(os.getenv("MODELS_LOC", "../models.lin_reg.bin"))

        try:
            with open(model_path, "wb") as f_out:
                pickle.dump((dv, lr), f_out)
            print("Successfully wrote binary file")
        except Exception as e:
            print(f"Failed to write binary file: {e}")

    return dv, lr


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
