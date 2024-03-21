from app.models.utils import DataFrameField
from datetime import datetime
from typing import List
import ipaddress


def is_private_ip(ip: str) -> bool:
    """
    Method to detect is an address IP is private or not
    """
    # We get back an ip obj and we detect if it's a private one or not
    ip_obj = ipaddress.ip_address(ip)
    return ip_obj.is_private


def filter_ip(df: DataFrameField, value: str):
    """
    Function to filter the IP depending on the value selected
    """
    # The private IP are the one starting by 10. or 172. or 192., the public are the other one
    if value == "private":
        return df[df['ip'].apply(is_private_ip)]
    else:
        return df[~df['ip'].apply(is_private_ip)]


def filter_before_time(df: DataFrameField, value: datetime):
    """

    """
    return df[df['time'] < value]


def filter_after_time(df: DataFrameField, value: datetime):
    """

    """
    return df[df['time'] > value]


def filter_type(df: DataFrameField, value: List[str]):
    """
    """
    return df[df['type'].isin(value)]

