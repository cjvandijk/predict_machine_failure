"""
Test upload of model file to s3 using localstack
"""

import os
import sys

project_root = os.getenv("USER_CODE_PATH", "/home/src/predict_machine_failure")
sys.path.insert(0, project_root)
# pylint disable=wrong-import-position
from .utils.s3_service import S3Storage


def test_upload_to_s3_service():
    # pylint disable=broad-exception-caught, line-too-long
    """
    Uses the localstack container hosted on port 4566.
    Creates bucket if it does not exist already (it shouldn't, since
    localstack is not configured to persist its data).
    After uploading it uses s3 list_buckets and list_data_in_bucket()
    to validate that the expected bucket and data are present.
    """

    bucket_name = "predict-storage-claudia"
    models_pkl_path = "mlflow_data/mlartifacts/1/aa4f34a7a3cb43858cd9e576fbf57753/artifacts/model/model.pkl"

    s3 = S3Storage()
    try:
        s3.create_s3_bucket(bucket_name)
        s3.upload_to_aws(models_pkl_path, bucket_name, "model/model.pkl")
    except Exception as e:
        print("EXCEPTION RAISED:", e)

    assert s3.list_buckets() == ["predict-storage-claudia"]
    assert s3.list_data_in_bucket(bucket_name) == ["model/model.pkl"]


if __name__ == "__main__":
    test_upload_to_s3_service()
