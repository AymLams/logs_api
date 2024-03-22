import json
import logging
import os
import yaml
from datetime import datetime

import pandas as pd
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from filters.logs import *
from models.logs import FilterLogs, Logs

data_folder = '/Users/lams/Documents/Dev/logs_api/data_folder'
DATA_FILENAME = "data.csv"
data_path = os.path.join(data_folder, DATA_FILENAME)

# We set a dict of filters in order to launch them depending on the parameters we have
FILTERS = {
    "ip": filter_ip,
    'before_time': filter_before_time,
    'after_time': filter_after_time,
    'type': filter_type
}


def get_filtered_logs(params: FilterLogs):
    """
    Method to get the content of the data from our data
    """

    # We get back the pandas dataframe from our csv file
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Data not available")

    # We filter our dataframe with the parameters
    df_filter = filter_logs(df, params)

    print(df_filter)
    #formated_data, format_type = format_data(params["log_format"], df_filter)

    return {"message": "Hello World"}


def format_data(log_format: str, df):
    """
    Function to format our data depending on the type of output they want
    """
    if log_format == "CSV":
        return False, False
    elif log_format == "JSON":
        return False, False
    else:
        return False, False


def filter_logs(df, params: FilterLogs):
    """
    Method to filter the dataframe of logs depending on the parameters we get back from the query

    """
    print(params)
    # We go through all the parameters we get in the query
    for param, value in params.__dict__.items():
        # We check if the param is in the key list of FILTERS
        if value and param in FILTERS:
            # We filter the dataframe using the function developed for the
            df = FILTERS[param](df, value)
    return df


def insert_logs(file_content: str, file_extension: str):
    """

    """
    # Depending on the extension we get, we read the content with different methods
    if file_extension == ".json":
        data = read_log_json(file_content)
    elif file_extension == ".yml":
        data = read_log_yml(file_content)
    else:
        return JSONResponse(status_code=400, content={"message": "Invalid file format."})

    # We update our output data depending on the content of the file
    update_data_output(data)

    return {"message": "File treated"}


def update_data_output(data: List[Logs]):
    """
    """
    # We check if the data file already exists or not
    if os.path.isfile(data_path):
        df = pd.read_csv(data_path)
    else:
        df = pd.DataFrame()

    # We create our new Pandas dataframe
    new_df = pd.json_normalize(data)

    # We make the concatenation of the both dataframes
    df_concat = pd.concat([df, new_df], ignore_index=True)

    if len(df_concat) > 500:
        return JSONResponse(status_code=404, content={"message": "Too many logs saved"})

    # We save it to a csv file
    df_concat.to_csv(data_path, index=False)


def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            pass
    return json_dict


def read_log_json(file_content: str) -> List[Logs]:
    """
    """
    # We initialize our output data
    data = []

    # We transform the string content in order to make in easier for the next step
    file_content = file_content.replace("\n", "")
    file_content = file_content.replace("}{", "}\n{")

    # We split the jsons in a list of jsons
    split_content = file_content.split("\n")

    # We try to transform each different Json in order to add them to our Data Base
    try:
        # We go through all splitted content and we add them to our data
        for content in split_content:
            data.append(json.loads(content, object_hook=date_hook))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail='Wrong format of data.')

    return data


def read_log_yml(file_content: str) -> List[Logs]:
    """
    """
    # We initialize our output data
    data = []

    # We split the content of the YAML file
    split_content = file_content.split('---')

    # We try to transform it in order to add content to our data
    try:
        for content in split_content:
            data.append(yaml.safe_load(content))
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail='Wrong format of data.')

    return data


def erase_logs():
    """
    Function to delete the file of data.
    """
    # We read the csv file to get the count of lines
    try:
        with open(data_path) as f:
            # We make the count of row in the CSV minus 1 to deal with the header
            count = sum(1 for line in f) - 1
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='No data available for this delete.')

    # We remove the file from the system
    # Another possibility was to delete all rows from the file, here we just delete it
    os.remove(data_path)

    return {"message": f"{count} lines removed from the data folder."}
