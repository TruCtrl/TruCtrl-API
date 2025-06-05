# SPDX-FileCopyrightText: 2025 McGuire Technology, LLC and TruCtrl Contributors
# SPDX-License-Identifier: MIT
#
# SPDX-FileComment:

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from config import config
from .models import Token
from .utils import (
    store_refresh_token, get_refresh_token, revoke_refresh_token, list_active_sessions,
    create_access_token, create_refresh_token
)
from .dependencies import get_current_user
from .constants import (
    ERROR_INVALID_CREDENTIALS, ERROR_INVALID_REFRESH_TYPE, ERROR_INVALID_REFRESH, TOKEN_TYPE_REFRESH
)
from jose import JWTError, jwt

api_router = APIRouter()

class HealthResponse(Token):
    status: str
    version: str

@api_router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", version=config.version, access_token="", token_type="", refresh_token=None)

@api_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    from main import authenticate_user  # Avoid circular import
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail=ERROR_INVALID_CREDENTIALS)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=config.access_token_expire_minutes)
    )
    refresh_token = create_refresh_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=config.refresh_token_expire_minutes)
    )
    store_refresh_token(user["username"], refresh_token)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

class RefreshRequest(Token):
    refresh_token: str

@api_router.post("/refresh", response_model=Token)
def refresh_access_token(request: RefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, config.secret_key, algorithms=[config.algorithm])
        if payload.get("type") != TOKEN_TYPE_REFRESH:
            raise HTTPException(status_code=401, detail=ERROR_INVALID_REFRESH_TYPE)
        username = payload.get("sub")
        if not username or get_refresh_token(username) != request.refresh_token:
            raise HTTPException(status_code=401, detail=ERROR_INVALID_REFRESH)
    except JWTError:
        raise HTTPException(status_code=401, detail=ERROR_INVALID_REFRESH)
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=config.access_token_expire_minutes)
    )
    # Optionally rotate refresh token here
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": request.refresh_token}

@api_router.get("/sessions")
def get_sessions():
    return list_active_sessions()

@api_router.delete("/sessions/{username}")
def revoke_session(username: str):
    revoke_refresh_token(username)
    return {"detail": f"Session for {username} revoked."}

@api_router.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
