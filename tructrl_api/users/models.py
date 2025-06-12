# File:     models.py
# Package:  users
# Package:  tructrl_api
# Project:  TruCtrl


# --- Imports ---

# Standard Imports

# Third-Party Imports
from sqlmodel import SQLModel, Field
from ulid import ulid

# Project Imports

# Package Imports


# --- Models ---

# User
class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.new()), primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_enabled: bool = True
