import mlflow
# import sys
# print(sys.path)

print("MLFLOW TYPE", type(mlflow))
print("MLFLOW FILE", mlflow.__file__)
print("MLflow imported:", dir(mlflow))

# from mlflow.tracking import MlflowClient

from pandas import DataFrame
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression


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

    # client = MlflowClient()
    # client.set_tracking_uri(uri="http://mlflow:5000")
    # client.set_experiment("train_model_thru_mage")
    # client.sklearn.autolog()

    # with client.start_run():

    # mlflow.set_tracking_uri(uri="http://mlflow:5000")
    mlflow.set_experiment("train_model_thru_mage")
    mlflow.sklearn.autolog()

    with mlflow.start_run():
        y_train = df['fail'].values
        df_train = df[~df['fail']]
        
        train_dicts = df_train.to_dict(orient='records')

        dv = DictVectorizer()
        X_train = dv.fit_transform(train_dicts)

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
