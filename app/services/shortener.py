import string
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from datetime import datetime
from fastapi import HTTPException
from ..models import model_url
from .. import schemas
from ..oauth2 import get_current_user

class URLShortener:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    @staticmethod
    def generate_short_code(length: int = 6) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    async def get_url_by_code(self, short_code: str) -> model_url.URL | None:
        query = select(model_url.URL).where(model_url.URL.short_code == short_code)
        result = await self.db.execute(query)
        url = result.scalar_one_or_none()
        
        if not url:
            return None
        
        return url

    async def get_url_by_target(self, target_url: str) -> model_url.URL | None:
        query = select(model_url.URL).where(model_url.URL.target_url == target_url)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def create_url(self, url_request: schemas.URLCreate, user_id: int | None = None) -> model_url.URL:
        short_code = url_request.custom_code or self.generate_short_code()
        
        target_url_str = url_request.get_target_url_str()
            
        url = await self.get_url_by_code(short_code)
        if url:
            if url_request.custom_code:
                  raise HTTPException(status_code=400, detail="Custom code already in use")
              
            return await self.create_url(url_request) 
              
        db_url = model_url.URL(
            target_url=target_url_str,
            short_code=short_code,
            expires_at=url_request.expires_at,
            user_id = user_id
        )
        
        if url_request.password:
            db_url.set_password(url_request.password)
        
        self.db.add(db_url)
        await self.db.commit()
        await self.db.refresh(db_url)
        
        return db_url

    async def _generate_unique_code(self) -> str:
        while True:
            short_code = self.generate_short_code()
            existing_url = await self.get_url_by_code(short_code)
            if not existing_url:
                return short_code

    async def check_url_validity(self, url_data: model_url.URL) -> None:
        if not url_data.is_active:
            raise HTTPException(status_code=410, detail="URL is no longer active")
        
        if not url_data:
            raise HTTPException(status_code=404, detail="URL not found")
        
        if url_data.expires_at and url_data.expires_at < datetime.now():
            url_data.is_active = False
            await self.db.commit()
            raise HTTPException(status_code=410, detail="URL has expired")
        
    async def get_url_by_id(self, url_id: int) -> model_url.URL | None:
        query = select(model_url.URL).where(model_url.URL.id == url_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_urls(self, user_id: int) -> list[model_url.URL]:
        query = select(model_url.URL).where(model_url.URL.user_id == user_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete_url(self, url_id: int):
        query = delete(model_url.URL).where(model_url.URL.id == url_id)
        await self.db.execute(query)
        await self.db.commit()

    async def update_url_status(self, url_id: int, is_active: bool):
        query = update(model_url.URL).where(model_url.URL.id == url_id).values(is_active=is_active)
        await self.db.execute(query)
        await self.db.commit()

    async def update_url_password(self, url_id: int, password: str | None) -> bool:
        url = await self.get_url_by_id(url_id)
        if not url:
            return False
            
        if password:
            url.set_password(password)
        else:
            url.password_hash = None
            
        await self.db.commit()
        return bool(url.password_hash)