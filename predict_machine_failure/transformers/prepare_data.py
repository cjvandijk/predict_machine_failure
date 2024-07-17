from pandas import DataFrame
import numpy as np
from scipy import stats

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def eliminate_outliers(named_df: DataFrame) -> DataFrame:
    """
    For each row in dataframe, retain column values that are within
    3 standard deviations from the mean
    """
    
    initial_length = len(named_df)
    df = named_df[(np.abs(stats.zscore(named_df)) < 3).all(axis=1)]
    print(f"Eliminated {initial_length - len(df)} outliers")
    return df


@transformer
def execute_transformer_action(df_raw: DataFrame) -> DataFrame:
    """
    Reformat dataframe column names from acronyms to spelled-out names
    """
    
    # Rename columns
    df_named = df_raw.rename(columns={
        "tempMode":"temp_mode",
        "AQ":"air_quality", 
        "USS":"proximity_sensor", 
        "CS":"current_usage", 
        "VOC":"voc_level", 
        "RP":"revolutions_per_minute", 
        "IP":"input_pressure",
        "Temperature":"temperature"
    })

    return eliminate_outliers(df_named)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
