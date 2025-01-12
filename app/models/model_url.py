from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from ..utils import hash, verify


class Base(AsyncAttrs, DeclarativeBase):
    pass

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    
    @property
    def is_protected(self) -> bool:
        return bool(self.password_hash)
    
    def set_password(self, password: str):
        if password:
            self.password_hash = hash(password)
    
    def verify_password(self, password: str) -> bool:
        if not self.password_hash:
            return True
        return verify(password, self.password_hash)