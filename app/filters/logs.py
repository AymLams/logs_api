#from models.utils import DataFrameField
from datetime import datetime
from typing import List
import ipaddress

import pandas as pd
from pandas import DataFrame


def is_private_ip(ip: str) -> bool:
    """
    Method to detect is an address IP is private or not
    """
    # We get back an ip obj and we detect if it's a private one or not
    ip_obj = ipaddress.ip_address(ip)
    return ip_obj.is_private


def filter_ip(df: DataFrame, value: str):
    """
    Function to filter the IP depending on the value selected
    """
    # The private IP are the one starting by 10. or 172. or 192., the public are the other one
    if value == "private":
        return df[df['ip'].apply(is_private_ip)]
    else:
        return df[~df['ip'].apply(is_private_ip)]


def filter_before_time(df: DataFrame, value: datetime):
    """

    """
    df['time'] = pd.to_datetime(df['time'])
    print(df.dtypes)
    print(type(value))
    return df[df['time'] < value]


def filter_after_time(df: DataFrame, value: datetime):
    """

    """

    df['time'] = pd.to_datetime(df['time'])
    print(df.dtypes)
    print(type(value))
    return df[df['time'] > value]


def filter_type(df: DataFrame, value: List[str]):
    """
    """
    # We apply a lambda to check if at least one of the value we want to filter in is part of the list
    return df[df['type'].apply(lambda x: any(item in x for item in value))]

