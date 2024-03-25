import uvicorn
import os
import logging

from fastapi import FastAPI, UploadFile, File, Form, Request

from app.modules.logs import get_filtered_logs, erase_logs, insert_logs
from app.models.logs import FilterLogs
from app.settings import get_settings


# We set our app
app = FastAPI()


# The GET API using the filter from params
@app.get("/logs/")
async def get_logs(request: Request, query_params: FilterLogs):
    # We get back the parameters from the query in order to make the filter
    logging.info("Getting logs from the data folder")
    return get_filtered_logs(query_params)


# The creation of some new logs
@app.post("/logs/")
async def create_logs(log_format: str = Form(...), file: UploadFile = File(...)):
    logging.info("Running POST API to save logs.")
    # We read the content of the file & decode it
    file_content = await file.read()
    file_content = file_content.decode('utf-8')

    # We get back the extension of the filename
    file_extension = os.path.splitext(file.filename)[1]

    return insert_logs(file_content, file_extension)


# The delete API
@app.delete("/logs/")
async def delete_logs():
    logging.info("Deleting Logs in data folder.")
    return erase_logs()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(app, host=settings.api_address, port=settings.api_port)
