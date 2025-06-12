# File:     models.py
# Package:  api_keys
# Package:  meraki
# Package:  tructrl_api
# Project:  TruCtrl


# --- Imports ---

# Standard Imports
from datetime import datetime
from typing import Optional

# Third-Party Imports
import ulid
from sqlmodel import SQLModel, Field

# Project Imports

# Module Imports


# --- Models ---

# API Key
class APIKey(SQLModel, table=True):
    id: ulid.ULID = Field(default_factory=ulid.new, primary_key=True)
    key: str

