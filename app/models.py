from pydantic import BaseModel
from typing import Literal


class Logs(BaseModel):
    uid: str
    ip: str
    size: int
    time: str
    allow: bool
    type: list


class CreateLogs(BaseModel):
    log_format: Literal['JSON', 'YAML']


class DeleteLogs(Logs):
    pass
