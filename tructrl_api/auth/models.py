# File:     models.py
# Package:  auth
# Package:  tructrl_api
# Project:  TruCtrl


# --- Imports ---

# Standard Imports
from typing import Optional

# Third-Party Imports
from pydantic import BaseModel

# Project Imports

# Package Imports


# --- Models ---

# Token
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str = None

# Token Data
class TokenData(BaseModel):
    username: Optional[str] = None
