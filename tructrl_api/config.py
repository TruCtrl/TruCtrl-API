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

    # Database
    db_type: str = os.getenv("DB_TYPE", "sqlite")
    db_name: str = os.getenv("DB_NAME", "tructrl.db")
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_host: str = os.getenv("DB_HOST", "")
    db_port: str = os.getenv("DB_PORT", "")
    db_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
    sqlalchemy_database_url: str = (
        f"sqlite:///{db_path}" if db_type == "sqlite" else
        f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

config = Config()