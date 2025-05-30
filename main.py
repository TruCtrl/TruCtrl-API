"""
FastAPI Starter App for TruCtrl
Demonstrates best practices: structure, type hints, config, logging, and modularity.
"""

from fastapi import FastAPI, APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import uvicorn
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from jose import JWTError, jwt  # Use 'jwt', not 'JWT'
from datetime import datetime, timedelta
from typing import Optional
import redis
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "TruCtrl API")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    version: str = os.getenv("APP_VERSION", "1.0.0")

settings = Settings()

# --- Logging ---
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(settings.app_name)

# --- OAuth2 Config ---
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str = None

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Redis Setup ---
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# --- Helper functions for refresh tokens ---
def store_refresh_token(username: str, refresh_token: str):
    redis_client.set(f"refresh_token:{username}", refresh_token)

def get_refresh_token(username: str):
    return redis_client.get(f"refresh_token:{username}")

def revoke_refresh_token(username: str):
    redis_client.delete(f"refresh_token:{username}")

def list_active_sessions():
    pattern = "refresh_token:*"
    keys = redis_client.keys(pattern)
    sessions = []
    for key in keys:
        username = key.split(":", 1)[1]
        token = redis_client.get(key)
        sessions.append({"username": username, "refresh_token": token})
    return sessions

# --- Fake DB for testing ---
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": "fakehashedpassword"
    }
}

def fake_hash_password(password: str):
    return "fakehashed" + password

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["hashed_password"] != fake_hash_password(password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=5))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# --- Routers ---
api_router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str

@api_router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok", version=settings.version)

@api_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    store_refresh_token(user["username"], refresh_token)
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

class RefreshRequest(BaseModel):
    refresh_token: str

@api_router.post("/refresh", response_model=Token)
def refresh_access_token(request: RefreshRequest):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token type")
        username = payload.get("sub")
        if not username or get_refresh_token(username) != request.refresh_token:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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

# --- App Factory ---
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug
    )
    app.include_router(api_router)  # Removed prefix="/api"

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
