# app/schemas/url.py
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    target_url: HttpUrl

class URLCreate(URLBase):
    custom_code: Optional[str] = None
    expires_at: Optional[datetime] = None

class URL(URLBase):
    short_code: str
    clicks: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True