# File:     models.py
# Package:  entity
# Package:  tructrl_api
# Project:  TruCtrl

# --- Imports ---

# Standard Imports
import ulid

# Third-Party Imports
from sqlmodel import SQLModel, Field

# Project Imports

# Package Imports

# --- Models ---

# Entity
class Entity(SQLModel, table=True):
    id: str = Field(default_factory=lambda: ulid.new().str, primary_key=True, description="ULID primary key")
    type: str = Field(description="Type of the entity, e.g., 'organization', 'user', 'device', etc.")




