from s3_service import S3Storage

if __name__ == "__main__":
    """S3 services"""

    bucket_name = "predict-storage-claudia"
    models_pkl_path = "mlflow_data/mlartifacts/1/aa4f34a7a3cb43858cd9e576fbf57753/artifacts/model/model.pkl"

    s3 = S3Storage()
    try:
        s3.create_s3_bucket(bucket_name)
    except Exception as e:
        print(e)
    predictions_path = "~/Documents/Projects/zoomcamp-homework/mlops/best_practices_hw_6/homework/output/yellow_tripdata_2023-03.parquet"
    s3.upload_to_aws(models_pkl_path, bucket_name, "model/model.pkl")

    print("~~~~ BUCKETS CREATED IN THIS TEST:", s3.list_buckets())
    print(
        f"~~~~ DATA THAT WAS LOADED INTO LOCALSTACK {bucket_name}: {s3.list_data_in_bucket(bucket_name)}"
    )
