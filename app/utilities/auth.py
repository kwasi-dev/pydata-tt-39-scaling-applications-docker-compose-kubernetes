from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.settings import get_settings
from app.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import User, TokenBlacklist
from fastapi import Request, Form, Depends, status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

settings = get_settings()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key,algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(request: Request, session: Annotated[AsyncSession, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.cookies.get("access_token")
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    blacklist_token = (await session.exec(
        select(TokenBlacklist).where(TokenBlacklist.token == token)
    )).one_or_none()

    if blacklist_token:
        raise credentials_exception
    
    user = (await session.exec(
        select(User).where(User.email == payload['sub'])
    )).one_or_none()
        
    if user is None:
        raise credentials_exception
    
    return user

