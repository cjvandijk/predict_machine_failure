from mage_ai.orchestration.triggers.api import trigger_pipeline

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def retrain(*args, **kwargs):
    """
    Note: code used was shared by Mage AI in their mlops zoomcamp repo.
    Changed the name of the pipeline to trigger.
    """
    
    models = [
        'linear_model.Lasso',
        'linear_model.LinearRegression',
        'svm.LinearSVR',
        'ensemble.ExtraTreesRegressor',
        'ensemble.GradientBoostingRegressor',
        'ensemble.RandomForestRegressor',
    ]

    trigger_pipeline(
        'predict_machine_failure',
        check_status=True,
        error_on_failure=True,
        schedule_name='Automatic retraining for sklearn models',
        verbose=True,
    )


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
