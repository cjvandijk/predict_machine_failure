# pylint disable=import-error

"""
Trigger the training pipeline
"""

from mage_ai.orchestration.triggers.api import trigger_pipeline

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def retrain():
    """
    Retrains the model, triggering the training pipeline
    """

    # models = [
    #     "linear_model.Lasso",
    #     "linear_model.LinearRegression",
    #     "svm.LinearSVR",
    #     "ensemble.ExtraTreesRegressor",
    #     "ensemble.GradientBoostingRegressor",
    #     "ensemble.RandomForestRegressor",
    # ]

    trigger_pipeline(
        "predict_machine_failure",
        check_status=True,
        error_on_failure=True,
        schedule_name="Automatic retraining for sklearn models",
        verbose=True,
    )
