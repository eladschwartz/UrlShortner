from fastapi import APIRouter, HTTPException, Depends, Request, Form
from ..database import get_db
from .. import schemas
import validators
from ..services.shortener import URLShortener
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import Annotated
from fastapi.templating import Jinja2Templates
from ..oauth2 import get_current_user
from ..models import model_user


router = APIRouter(
     prefix="/api",
     tags = ['API']
)

templates = Jinja2Templates(directory="templates")

async def get_shortener(db=Depends(get_db)) -> URLShortener:
    return URLShortener(db)

@router.post("/shorten", response_model=schemas.URL)
async def create_short_url(url_request: schemas.URLCreate, shortener: Annotated[URLShortener, Depends(get_shortener)], current_user: model_user.User | None = Depends(get_current_user)):
    # Validate URL
    if not validators.url(str(url_request.target_url)):
        raise HTTPException(status_code=400, detail="Invalid URL provided")
    
    # Check if URL already exists
    existing_url = await shortener.get_url_by_target(str(url_request.target_url))

    if existing_url and existing_url.is_active:
        return existing_url
    
    user_id = current_user.id if current_user else None
    return await shortener.create_url(url_request, user_id)

@router.get("/{short_code}",response_class=HTMLResponse)
async def redirect_to_url(request: Request,short_code: str,shortener: Annotated[URLShortener, Depends(get_shortener)]):
    url_data = await shortener.get_url_by_code(short_code)
    await shortener.check_url_validity(url_data)
    
    
    if url_data.password_hash:
        return templates.TemplateResponse(
            "password.html",
            {"request": request, "short_code": short_code}
        )
        
    return RedirectResponse(url=url_data.target_url)

@router.post("/{short_code}/verify")
async def verify_password(short_code: str,shortener: Annotated[URLShortener, Depends(get_shortener)],password: str = Form(...)):
    url_data = await shortener.get_url_by_code(short_code)
    await shortener.check_url_validity(url_data)
    
    if not url_data.verify_password(password):
        return templates.TemplateResponse(
            "password.html",
            {
                "request": Request,
                "short_code": short_code,
                "error": "Invalid password"
            },
            status_code=401
        )
    
    return RedirectResponse(url=url_data.target_url)


@router.delete("/urls/{url_id}")
async def delete_url(url_id: int,current_user: model_user.User = Depends(get_current_user),shortener: URLShortener = Depends(get_shortener)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    url = await shortener.get_url_by_id(url_id)
    if not url or url.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="URL not found")
        
    await shortener.delete_url(url_id)
    return {"message": "URL deleted successfully"}

@router.put("/urls/{url_id}/toggle")
async def toggle_url_status(url_id: int,status: dict,current_user: model_user.User = Depends(get_current_user),shortener: URLShortener = Depends(get_shortener)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    url = await shortener.get_url_by_id(url_id)
    if not url or url.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="URL not found")
        
    await shortener.update_url_status(url_id, status.get("is_active"))
    return {"message": "Status updated successfully"}

@router.post("/urls/{url_id}/password")
async def update_url_password(url_id: int,password_data: dict,current_user: model_user.User = Depends(get_current_user),shortener: URLShortener = Depends(get_shortener)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    url = await shortener.get_url_by_id(url_id)
    if not url or url.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="URL not found")
        
    is_protected = await shortener.update_url_password(url_id, password_data.get("password"))
    return {"is_protected": is_protected}