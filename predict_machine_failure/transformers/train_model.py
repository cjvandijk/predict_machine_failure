import mlflow
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression

from predict_machine_failure.utils import split_dataset
from predict_machine_failure.utils import encode


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
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
    mlflow.sklearn.autolog()

    # X_train, X_test, y_train, y_test 

    with mlflow.start_run():
        df_train, df_val, y_train, y_val = split_dataset.split_df(df)
        X_train, X_val, dv = encode.vectorize_features(df_train, df_val)

        lr = LinearRegression()
    
        lr.fit(X_train, y_train)

    print(lr.intercept_)

    return dv, lr


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
