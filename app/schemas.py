# app/schemas/url.py
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class URLBase(BaseModel):
    target_url: HttpUrl
    
    def get_target_url_str(self) -> str:
        return str(self.target_url)

class URLCreate(URLBase):
    custom_code: Optional[str] = None
    expires_at: Optional[datetime] = None
    password: Optional[str] = None

class URL(URLBase):
    short_code: str
    created_at: datetime
    is_active: bool
    is_protected: bool

    class Config:
        from_attributes = True
        
class PasswordVerify(BaseModel):
    password: str