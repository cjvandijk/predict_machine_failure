import os
import pickle
from typing import Dict

from flask import Flask, jsonify, request

"""
Flask application for predicting machine failure based on
readings submitted from machine. README.md contains descriptions
of the machine readings.

Expects a trained LinearRegression model and DictVectorizer to be
available, the filename to appear as environment variable MODELS_LOC.

If MODELS_LOC is not in the environemnt, or if the model cannot be
loaded from its filename, an error will be returned by the service.
"""


def load_model():
    """
    Locates model with MODELS_LOC environment variable, returns either
    the loaded model and dictvectorizer, or an error message indicating
    a problem loading the model.
    """

    model_load_msg = dv = model = None

    MODELS_LOC = os.getenv("MODELS_LOC", "MODELS_LOC env variable not found")

    if MODELS_LOC[:6] == "MODELS":  # variable was not found in environment
        model_load_msg = MODELS_LOC

    else:
        try:
            with open(MODELS_LOC, "rb") as f_in:
                (dv, model) = pickle.load(f_in)
        except Exception as e:
            model_load_msg = e
    return model_load_msg, dv, model


def predict(features: Dict[str, int], model, dv) -> float:
    """
    Given a dictionary of machine readings, returns a number
    predicting whether machine will fail.
    """
    X = dv.transform(features)
    preds = model.predict(X)
    return round(preds[0], 2)


app = Flask("predict-machine-failure")


@app.route("/predict", methods=["POST"])
def predict_endpoint() -> Dict[str, str | int]:
    """
    Accepts input through the request object, sends to the predict() function,
    and returns result which includes
    """

    machine_readings = request.get_json()

    result = {"error_message": None, "failure_likelihood": None}

    required_keys = [
        "footfall",
        "temp_mode",
        "air_quality",
        "proximity_sensor",
        "current_usage",
        "voc_level",
        "revolutions_per_minute",
        "input_pressure",
        "temperature",
    ]

    for k in required_keys:
        if k not in machine_readings:
            result["error_message"] = (
                f"Incorrect data sent to predict service. Expecting {k}."
            )
            return jsonify(result)

    model_load_msg, dv, model = load_model()

    if model_load_msg:  # a message means the model failed to load
        result["error_message"] = f"Model failed to load: {model_load_msg}"
    else:
        print("PROCESSING MACHINE_READINGS")
        pred = predict(machine_readings, model, dv)
        result["failure_likelihood"] = f"{int(pred*100)} %"

    return jsonify(result)


if __name__ == "__main__":

    app.run(debug=True, host="0.0.0.0", port=9696)
