import sys
import argparse

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Logs API"
    data_folder: str
    max_file_size: int
    api_address: str
    api_port: int

    class Config:
        pass


@lru_cache
def get_settings():
    try:
        return get_settings_sys()
    except:
        return get_settings_json("config_test.json")


@lru_cache
def get_settings_sys():
    return Settings.parse_file(parse_sys_config())


@lru_cache
def get_settings_json(path):
    return Settings.parse_file(path)


def parse_sys_config():
    """
    Method to get back the config file from the sys variables
    """
    parser = argparse.ArgumentParser()
    # We set which argument we want to find in the parser
    parser.add_argument("-c", "--config", help="Path to the configuration file.")
    args = parser.parse_args(sys.argv[1:])
    # We get back the config
    config_path = args.config
    return config_path
