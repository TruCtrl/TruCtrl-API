import os
from pydantic import BaseModel


class Config(BaseModel):

    # General
    app_name: str = "TruCtrl-API"
    version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"

    # 0Auth2
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))
    refresh_token_expire_minutes: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))

    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))

config = Config()