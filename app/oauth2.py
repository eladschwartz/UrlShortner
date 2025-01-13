from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from .models import model_user
from .database import get_db
from fastapi import Depends, Request, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from .config import settings
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Modified OAuth2 scheme that can read from cookies
class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        # First try getting the token from the authorization header
        authorization = request.headers.get("Authorization")
        if authorization and authorization != 'Bearer null':
            scheme, param = get_authorization_scheme_param(authorization)
            if scheme.lower() == "bearer":
                return param
     
     
        token = request.cookies.get("access_token")
        if token and token.startswith("Bearer "):
                return token[7:]  # Remove 'Bearer ' prefix
            
        # If no token is found, redirect to login page
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/api/auth/login"} 
        )

# Use the modified OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACRESS_TOKEN_EXPIRE_MINTUES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=ACRESS_TOKEN_EXPIRE_MINTUES)
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logging.error(f"Token creation error: {str(e)}")
        raise
   
    
def verify_access_token(token:str, credentials_exception):
    try:
        if token is None:
         raise credentials_exception
     
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id: str = str(payload.get("user_id"))
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

    
async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    
    if not token:
        return None
        
    try:
        token_type, token = token.split()
        if token_type.lower() != "bearer":
            return None
            
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")
        if not email:
            return None
            
        query = select(model_user.User).where(model_user.User.email == email)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
            
        return user
    except JWTError as e:
        print(e)