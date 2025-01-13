from fastapi import APIRouter, HTTPException, status, Depends, Request, Form, Response
from fastapi.responses import RedirectResponse, JSONResponse
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import model_user
from ..utils import hash, verify
from .. import oauth2
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    
    query = select(model_user.User).where(model_user.User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
         return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password"},
            status_code=401
        )
    
    if not verify(password, user.password):
         return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid email or password"},
            status_code=401
        )
     
    access_token = oauth2.create_access_token(data={"user_id": user.id, "sub": email})
    response = RedirectResponse(url="/", status_code=302)
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=18000,
        expires=18000,
        samesite='lax'
    )
    return response

@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


def checkPassword(request, password, confirm_password):
     if password != confirm_password:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Passwords do not match"},
            status_code=400
        )
        
        
async def check_if_user_exist(email, db) -> model_user.User:
    # Check if user exists
    query = select(model_user.User).where(model_user.User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_user(db, email,password) -> model_user.User:
    user = model_user.User(email=email)
    user.password = hash(password)
    
    db.add(user)
    await db.commit()
    return user

@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: AsyncSession = Depends(get_db)):
    
    checkPassword(request,password,confirm_password)
    existing_user = await check_if_user_exist(email, db)
    
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username or email already exists"},
            status_code=400
        )
    
    user = await create_user(db,email,password)
    access_token = oauth2.create_access_token(data={"user_id": user.id, "sub":email})
    
   
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=18000,
        expires=18000,
        samesite='lax'
    )
    
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response