from pydantic import BaseModel
import pandas as pd


class DataFrameField(BaseModel):
    dataframe: pd.DataFrame
