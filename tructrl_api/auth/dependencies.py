"""
File:           dependencies.py
Module:         users
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    Dependencies Layer for User Authentication. 
                Contains reusable dependency functions for authentication, authorization, database sessions, etc. 
                Used with FastAPI's Depends system.
"""

from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from .models import TokenData
from .constants import ERROR_INVALID_CREDENTIALS
from ..config import config


from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


""" def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail=ERROR_INVALID_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(token_data.username)
    if user is None:
        raise credentials_exception
    return user
 """