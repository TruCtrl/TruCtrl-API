from datetime import datetime, timedelta
from jose import jwt
from ..config import config
from .constants import TOKEN_TYPE_REFRESH

# --- In-memory store for refresh tokens ---
refresh_tokens_db = {}

def store_refresh_token(username: str, refresh_token: str):
    global refresh_tokens_db
    refresh_tokens_db[username] = refresh_token

def get_refresh_token(username: str):
    return refresh_tokens_db.get(username)

def revoke_refresh_token(username: str):
    refresh_tokens_db.pop(username, None)

def list_active_sessions():
    return [
        {"username": username, "refresh_token": token}
        for username, token in refresh_tokens_db.items()
    ]

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.refresh_token_expire_minutes))
    to_encode.update({"exp": expire, "type": TOKEN_TYPE_REFRESH})
    return jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
