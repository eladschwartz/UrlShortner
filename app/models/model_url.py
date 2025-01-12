from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

class Base(AsyncAttrs, DeclarativeBase):
    pass

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)