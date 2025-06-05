from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from config import config
from auth import (
    oauth2_scheme, Token, TokenData,
    store_refresh_token, get_refresh_token, revoke_refresh_token, list_active_sessions,
    create_access_token, create_refresh_token, get_current_user
)


# --- Routers ---
api_router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str

@api_router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", version=config.version)

@api_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    from main import authenticate_user  # Avoid circular import
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
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

class RefreshRequest(BaseModel):
    refresh_token: str

@api_router.post("/refresh", response_model=Token)
def refresh_access_token(request: RefreshRequest):
    from jose import JWTError, jwt
    try:
        payload = jwt.decode(request.refresh_token, config.secret_key, algorithms=[config.algorithm])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token type")
        username = payload.get("sub")
        if not username or get_refresh_token(username) != request.refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=config.access_token_expire_minutes)
    )
    # Optionally rotate refresh token here
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": request.refresh_token}

@api_router.get("/sessions")
def get_sessions():
    """Session Dashboard endpoint: List all active refresh tokens/users."""
    return list_active_sessions()

@api_router.delete("/sessions/{username}")
def revoke_session(username: str):
    """Session Dashboard endpoint: Revoke a user's refresh token (logout everywhere)."""
    revoke_refresh_token(username)
    return {"detail": f"Session for {username} revoked."}

@api_router.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user