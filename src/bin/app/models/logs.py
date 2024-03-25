from pydantic import BaseModel
from typing import Literal, List, Optional
from datetime import datetime


# Class to build the content of a Logs
class Logs(BaseModel):
    uid: str
    ip: str
    size: int
    time: datetime
    allow: bool
    type: List[Literal['phishing', 'malware', 'exploit', 'c2', 'spam']]


# Class for the creation of the logs
class CreateLogs(BaseModel):
    log_format: Literal['JSON', 'YML']


# Class to deal with the logs we will filter
class FilterLogs(BaseModel):
    ip: Optional[Literal['private', 'public']] = None
    before_time: Optional[datetime] = None
    after_time: Optional[datetime] = None
    type: Optional[List[Literal['phishing', 'malware', 'exploit', 'c2', 'spam']]] = None
    log_format: Literal['JSON', 'XML', 'CSV', 'YML']


# Class to delete logs
class DeleteLogs(Logs):
    pass
