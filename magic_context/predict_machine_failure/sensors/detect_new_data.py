# pylint disable=import-error, unspecified-encoding

"""
Emulates checking for new data which would necessitate model
re-training.
"""

import json
import os

import requests
from mage_ai.settings.repo import get_repo_path

if "sensor" not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def check_for_new_data() -> bool:
    """
    Note that the data selected for this project is static and does not change.
    To emulate changing data, a call is made to an endpoint that returns a
    pull_count; when that pull_count increases, the trigger considers a change
    in data and runs the re-training pipeline. However the data used in
    training remains the same and so changes in metrics like RMSE will not
    change.

    Note: code used was shared by Mage AI in their mlops zoomcamp repo.
    """

    path = os.path.join(get_repo_path(), ".cache", "data_tracker")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    data_tracker_prev = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            data_tracker_prev = json.load(f)

    data_tracker = requests.get(
        "https://hub.docker.com/v2/repositories/mageai/mageai", timeout=10
    ).json()
    with open(path, "w") as f:
        f.write(json.dumps(data_tracker))

    count_prev = data_tracker_prev.get("pull_count")
    count = data_tracker.get("pull_count")

    print(f"Previous count: {count_prev}")
    print(f"Current count:  {count}")

    should_train = count_prev is None or count > count_prev
    if should_train:
        print("Retraining models...")
    else:
        print("Not enough new data to retrain models.")

    return should_train
