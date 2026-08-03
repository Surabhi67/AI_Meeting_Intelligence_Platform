from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str

class MeetingResponse(BaseModel):
    id: int
    title: str
    audio_path: str
    transcript: str | None = None
    summary: str | None = None
    status: str

    class Config:
        from_attributes = True