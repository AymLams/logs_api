import uvicorn
from fastapi import FastAPI, UploadFile
from logs.logs import filter_logs, supp_logs, insert_logs
from models import Logs, CreateLogs

app = FastAPI()


@app.get("/logs/")
async def get_logs():
    return filter_logs()


@app.post("/logs/")
async def create_logs(create_logs: CreateLogs, file: UploadFile):
    return insert_logs()


@app.delete("/logs/")
async def delete_logs():
    return supp_logs()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
