from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any, AnyStr, Union
from fastapi import UploadFile
from enum import Enum
from datetime import datetime

class UserSigninPayload(BaseModel):
    user: str
    email: EmailStr
    password: str

class UserLoginPayload(BaseModel):
    user_or_email: str
    password: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LoginResponse(BaseModel):
    valid: bool
    token: Optional[str] = None

class SuccessResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class Status(str, Enum):
    UPLOADED = 'uploaded'
    PROCESSED = 'processed'

class TaskObject(BaseModel):
    task_id: int
    original_file_name: str
    original_file_ext: str
    original_stored_file_name: str
    target_file_ext: str
    target_stored_file_name: str
    uploaded_at: datetime
    converted_at: Union[datetime, None]
    status: Status
    