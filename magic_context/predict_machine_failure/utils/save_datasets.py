
"""
Save parquet files to localhost
"""

import os
from datetime import datetime

from pandas import DataFrame


S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL",
                            "http://localhost:4566")
BUCKET = os.getenv("BUCKET", "training-datasets-claudia")
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print("ENDPOINT", S3_ENDPOINT_URL)


def set_options() -> str:
    """
    Configure storage options for localstack
    """

    return {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}


def save_dataset(df: DataFrame, df_name: str) -> None:
    """
    Save dataframe as parquet file to localstack:s3

    Args:
        df: pd.DataFrame
        dfname: string rep of df name for filename

    Returns:
        None
    """

    file_path = f"s3://{BUCKET}/{df_name}_{current_datetime}.parquet"

    print("Saving datasets to localstack")
    df.to_parquet(
        file_path,
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=set_options(),
    )
