"""
File:           models.py
Module:         meraki
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    ORM models for Meraki integration.
"""
from sqlmodel import SQLModel, Field
from typing import Optional

class MerakiOrganization(SQLModel, table=True):
    __tablename__ = "meraki_organizations"
    id: str = Field(primary_key=True)
    name: str
    url: Optional[str] = None



