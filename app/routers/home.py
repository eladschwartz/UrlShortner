from fastapi import APIRouter, Request, Depends,status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from ..oauth2 import get_current_user
from ..models import model_user
from ..services.shortener import URLShortener
from ..database import get_db

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="",
    tags=['']
)

async def get_shortener(db=Depends(get_db)) -> URLShortener:
    return URLShortener(db)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, current_user: model_user.User | None = Depends(get_current_user)):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "current_user": current_user}
    )
    
    
    
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request, 
    current_user: model_user.User = Depends(get_current_user),
    shortener: URLShortener = Depends(get_shortener)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/auth/login"}
        )
        
    urls = await shortener.get_user_urls(current_user.id)
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request, 
            "current_user": current_user,
            "urls": urls
        }
    )