import string
import random
from sqlalchemy import select
from datetime import datetime
from fastapi import HTTPException
from ..models import model_url
from .. import schemas

class URLShortener:
    def __init__(self, db):
        self.db = db
        
    @staticmethod
    def generate_short_code(length: int = 6) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    async def get_url_by_code(self, short_code: str) -> model_url.URL | None:
        query = select(model_url.URL).where(model_url.URL.short_code == short_code,model_url.URL.is_active)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_url_by_target(self, target_url: str) -> model_url.URL | None:
        query = select(model_url.URL).where(model_url.URL.target_url == target_url)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create_url(self, url_request: schemas.URLCreate) -> model_url.URL:
        if url_request.custom_code:
            if not url_request.custom_code.isalnum():
                raise HTTPException(
                    status_code=400,
                    detail="Custom code can only contain letters and numbers"
                )
            existing_url = await self.get_url_by_code(url_request.custom_code)
            if existing_url:
                raise HTTPException(
                    status_code=400,
                    detail="Custom code already in use"
                )
            short_code = url_request.custom_code
        else:
            short_code = await self._generate_unique_code()

        db_url = model_url.URL(
            target_url=str(url_request.target_url),
            short_code=short_code,
            expires_at=url_request.expires_at
        )
        
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
        if not url_data:
            raise HTTPException(status_code=404, detail="URL not found")
        
        if url_data.expires_at and url_data.expires_at < datetime.now():
            url_data.is_active = False
            await self.db.commit()
            raise HTTPException(status_code=410, detail="URL has expired")