import os

import pandas as pd

"""
This is a Mage block, which runs in the pipeline as the first
block. It loads the dataset specified in INPUT_DATA_FILE env
variable and returns it as a pandas DataFrame.
"""


if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_file() -> pd.DataFrame:
    """
    Load data from dataset, path specified in the INPUT_DATA_FILE
    environment variable.
    Return a dataframe containing the raw data.
    """

    input_path = os.getenv("INPUT_DATA_FILE")

    df_raw = pd.read_csv(input_path)

    return df_raw


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
