from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from ..utils import hash, verify
from ..database import Base
from sqlalchemy.orm import relationship

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String, index=True)
    short_code = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", back_populates="urls")
    
    
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