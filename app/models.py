"""
数据模型 - 包含所有的Pydantic模型定义
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# 请求模型
class ReplyCommentRequest(BaseModel):
    oid: int
    rpid: int
    message: str
    root: int


class DifyConfigRequest(BaseModel):
    base_url: str
    interval_hours: int = 1


# 响应模型
class CommentInfo(BaseModel):
    rpid: int
    mid: str
    oid: int
    root: int
    parent: int
    content: str
    title: str
    uname: str


class UnrepliedCommentsResponse(BaseModel):
    result: List[CommentInfo]
    count: int


class ReplyResponse(BaseModel):
    success: bool
    message: str
    rpid: Optional[int] = None


class DifyCallResponse(BaseModel):
    success: bool
    message: str
    response_data: Optional[dict] = None
    call_time: datetime


class SchedulerStatusResponse(BaseModel):
    is_running: bool
    last_call_time: Optional[datetime]
    last_call_status: Optional[str]
    call_count: int
    error_count: int
    next_run_time: Optional[datetime] 