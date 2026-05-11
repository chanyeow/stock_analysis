from datetime import datetime
from typing import List

from pydantic import BaseModel


class LogFileInfo(BaseModel):
    name: str
    size: int
    modified_at: datetime


class LogListResponse(BaseModel):
    files: List[LogFileInfo]


class LogContentResponse(BaseModel):
    name: str
    lines: List[str]
    read_lines: int
