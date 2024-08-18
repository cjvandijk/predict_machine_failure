# pylint disable=undefined-variable

"""
Used by mage for pipeline dashboard
"""


@data_source
def d(df):
    return df[df["status"] == "completed"]
