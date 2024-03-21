import os
import json
import yaml
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
from app.filters.logs import *
from app.models.logs import FilterLogs, Logs

data_path = ''

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

    return {"message": "Hello World"}


def filter_logs(df, params: FilterLogs):
    """
    Method to filter the dataframe of logs depending on the parameters we get back from the query

    """
    # We go through all the parameters we get in the query
    for param, value in params.items():
        # We check if the param is in the key list of FILTERS
        if param in FILTERS:
            # We filter the dataframe using the function developed for the
            df = FILTERS[param](df, value)
    return df


def insert_logs(file: UploadFile):

    # We get back the extension of the file
    extension = os.path.splitext(file.filename)[1]

    # Depending on the extension we get, we read the content with different methods
    if extension in ('json', 'yml'):
        data = read_log_json(file)
    elif extension == "yml":
        data = read_log_yml(file)
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
    new_df = pd.DataFrame(data)

    # We make the concatenation of the both dataframes
    df_concat = pd.concat([df, new_df], ignore_index=True)

    if len(df_concat) > 500:
        return JSONResponse(status_code=404, content={"message": "Too many logs saved"})

    # We save it to a csv file
    df_concat.to_csv(data_path, index=False)


def read_log_json(file: UploadFile) -> List[Logs]:
    """
    """
    # We get back the content of the file
    file_content = await file.read()
    data = json.loads(file_content)
    return data


def read_log_yml(file: UploadFile) -> List[Logs]:
    """
    """
    # We get back the content of the file
    file_content = await file.read()
    data = yaml.safe_load(file_content)
    return data


def erase_logs():
    """
    Function to delete the file of data.
    """
    # We read the csv file to get the count of lines
    try:
        with open(data_path) as f:
            count = sum(1 for line in f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail='No data available for this delete')

    # We remove the file from the system
    # Another possibility was to delete all rows from the file, here we just delete it
    os.remove(data_path)

    return {"message": f"{count} lines removed from the data folder."}
