import uvicorn
import os
from fastapi import FastAPI, UploadFile, File, Form
from modules.logs import get_filtered_logs, erase_logs, insert_logs
from models.logs import CreateLogs, FilterLogs
from settings import Settings
import logging

app = FastAPI()


# The GET API using the filter from params
@app.get("/logs/")
async def get_logs(query_params: FilterLogs):
    # We get back the parameters from the query in order to make the filter
    return get_filtered_logs(query_params)


# The creation of some new logs
@app.post("/logs/")
async def create_logs(log_format: str = Form(...), file: UploadFile = File(...)):
    logging.info("Running POST API to save logs.")
    file_content = await file.read()
    file_extension = os.path.splitext(file.filename)[1]
    file_content = file_content.decode('utf-8')
    return insert_logs(file_content, file_extension)


# The delete API
@app.delete("/logs/")
async def delete_logs():
    return erase_logs()


if __name__ == "__main__":
    #settings = Settings()
    uvicorn.run(app, host="127.0.0.1", port=8000)
