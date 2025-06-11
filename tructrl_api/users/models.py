"""
File:           routes.py
Module:         users
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    Routes Layer for User Management.
                Defines the API endpoints (HTTP routes) and connects them to the service or CRUD functions.
                Handles request/response, dependency injection, and error handling.
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from ulid import ulid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.new()), primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
