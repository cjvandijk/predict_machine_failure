# pylint disable=wrong-import-position, import-error

"""
Run prediction for given input
"""

import os
import sys
from typing import Dict

# from sklearn.feature_extraction import DictVectorizer

project_root = os.getenv("USER_CODE_PATH", "/home/src/predict_machine_failure")
sys.path.insert(0, project_root)
from predict_service_context.predict import load_model, predict

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom

DEFAULT_INPUTS = {
    "footfall": 15,
    "temp_mode": 3,
    "air_quality": 7,
    "proximity_sensor": 1,
    "current_usage": 6,
    "voc_level": 5,
    "revolutions_per_minute": 45,
    "input_pressure": 6,
    "temperature": 22,
}


@custom
def mage_predict(**kwargs) -> Dict[str, float]:
    inputs: Dict[str, int] = kwargs.get("inputs", DEFAULT_INPUTS)

    model_load_msg, vectorizer, model = load_model()

    predictions = predict(inputs, model, vectorizer)

    return model_load_msg, predictions
