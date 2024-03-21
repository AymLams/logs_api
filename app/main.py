import uvicorn
from fastapi import FastAPI, UploadFile
from modules.logs import get_filtered_logs, erase_logs, insert_logs
from app.models.logs import CreateLogs, FilterLogs
from settings import settings

app = FastAPI()


# The GET API using the filter from params
@app.get("/logs/")
async def get_logs(query_params: FilterLogs):
    # We get back the parameters from the query in order to make the filter
    return get_filtered_logs(query_params)


# The creation of some new logs
@app.post("/logs/")
async def create_logs(format_logs: CreateLogs, file: UploadFile):
    return insert_logs(file, )


# The delete API
@app.delete("/logs/")
async def delete_logs():
    return erase_logs()


if __name__ == "__main__":
    conf = settings
    uvicorn.run(app, host="127.0.0.1", port=8000)
