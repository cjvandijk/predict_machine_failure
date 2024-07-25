import os
from pathlib import Path
import pickle
import tempfile
from typing import Tuple

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(
    data: Tuple[DictVectorizer, LinearRegression], *args, **kwargs
    ) -> None:
    """
    Logs the dictvectorizer to mlflow artifacts and the linear 
    regression model to mlflow models. Registers the logged model 
    in mlflow.

    Args:
        data: The output from the upstream parent block containing a tuple
        with a dictvectorizer and a linear regression model

    Output:
        No output is returned; model will be registered in mlflow 
        and ready for webservice deployment
    """


    EXPERIMENT_NAME = "train_model_thru_mage"
    MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI', "http://mlflow:5000")

    # register model in mlflow
    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.rmse ASC"]
    )[0]
    
    # Register best model
    mlflow.register_model(model_uri=f"runs:/{best_run.info.run_id}/models", 
                          name="Machine Failure Prediction Model"
                         )
