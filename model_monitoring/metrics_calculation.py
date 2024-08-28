# pylint: disable=line-too-long,unnecessary-pass,pointless-string-statement,unused-import,line-too-long

"""
In progress
"""

import datetime
import logging
import os
import pickle
import random
import time
from pathlib import Path

import pandas as pd
import psycopg
from evidently import ColumnMapping
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
    DatasetMissingValuesMetric,
)
from evidently.report import Report

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
)
"""


def read_reference_data():
    ref_data_file = Path(
        os.getenv(
            "REF_DATA_FILE", "../../../data/processed/reference_data.parquet"
        )
    )
    reference_data_df = pd.read_parquet(ref_data_file)
    reference_data_df.rename(columns={"fail": "prediction"})
    return reference_data_df


def load_model():
    model_path = Path(os.getenv("MODELS_LOC", "../../../models/lin_reg.bin"))
    try:
        with open(model_path, "rb") as f_in:
            dv, model = pickle.load(f_in)
        print("Successfully read binary model file")
    except Exception as e:
        print(f"Failed to read binary model file: {e}")
    return dv, model


def read_raw_data():
    raw_data = os.getenv("INPUT_DATA_FILE", "../../../data/raw/data.csv")
    raw_data_df = pd.read_parquet(raw_data)
    raw_data_df = raw_data_df.rename(
        columns={
            "tempMode": "temp_mode",
            "AQ": "air_quality",
            "USS": "proximity_sensor",
            "CS": "current_usage",
            "VOC": "voc_level",
            "RP": "revolutions_per_minute",
            "IP": "input_pressure",
            "Temperature": "temperature",
            "Fail": "prediction",
        }
    )
    return raw_data_df


numeric_features = list(raw_data_df.columns)
# numeric_features.remove('prediction')

column_mapping = ColumnMapping(
    prediction="prediction",
    numerical_features=numeric_features,
    categorical_features=None,
    target=None,
)

report = Report(
    metrics=[
        ColumnDriftMetric(column_name="prediction"),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric(),
    ]
)


def prep_db():
    pass
    """
    FIX PYLINT COMPLAINTSLATER
    with psycopg.connect("host=localhost port=5433 user=postgres password=example", autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("create database test;")
        with psycopg.connect(
            "host=localhost port=5433 dbname=test user=postgres password=example"
            ) as conn:
            conn.execute(create_table_statement)
"""


def calculate_metrics_postgresql(curr, i):
    current_data_df = read_raw_data()
    reference_data_df = read_reference_data()
    dv, model = load_model()

    # predict failure for "new" raw data
    current_data_df["prediction"] = model.predict(
        current_data_df[numeric_features].fillna(0)
    )

    report.run(
        reference_data=reference_data_df,
        current_data=current_data,
        column_mapping=column_mapping,
    )

    result = report.as_dict()

    prediction_drift = result["metrics"][0]["result"]["drift_score"]
    num_drifted_columns = result["metrics"][1]["result"][
        "number_of_drifted_columns"
    ]
    share_missing_values = result["metrics"][2]["result"]["current"][
        "share_of_missing_values"
    ]

    curr.execute(
        "insert into dummy_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
        (
            begin + datetime.timedelta(i),
            prediction_drift,
            num_drifted_columns,
            share_missing_values,
        ),
    )


def batch_monitoring_backfill():
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    """
    FIX PYLINT ISSUES LATER
    with psycopg.connect("host=localhost port=5433 dbname=test user=postgres password=example", autocommit=True) as conn:
        for i in range(0, 27):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, i)

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send = last_send + datetime.timedelta(seconds=10)
            logging.info("data sent")
"""


if __name__ == "__main__":
    batch_monitoring_backfill()
