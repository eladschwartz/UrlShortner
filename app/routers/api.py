from fastapi import APIRouter, HTTPException, Depends, Request
from ..database import get_db
from .. import schemas
import validators
from ..services.shortener import URLShortener
from fastapi.responses import RedirectResponse
from typing import Annotated


router = APIRouter(
     prefix="/api",
     tags = ['API']
)

async def get_shortener(db=Depends(get_db)) -> URLShortener:
    return URLShortener(db)

@router.post("/shorten", response_model=schemas.URL)
async def create_short_url(url_request: schemas.URLCreate, shortener: Annotated[URLShortener, Depends(get_shortener)]):
    # Validate URL
    if not validators.url(str(url_request.target_url)):
        raise HTTPException(status_code=400, detail="Invalid URL provided")
    
    # Check if URL already exists
    existing_url = await shortener.get_url_by_target(str(url_request.target_url))

    if existing_url and existing_url.is_active:
        return existing_url
    
    return await shortener.create_url(url_request)

@router.get("/{short_code}")
async def redirect_to_url(request: Request,short_code: str,shortener: Annotated[URLShortener, Depends(get_shortener)]):
    url_data = await shortener.get_url_by_code(short_code)
    await shortener.check_url_validity(url_data)
    
    return RedirectResponse(url=url_data.target_url)