"""
File:           dependencies.py
Module:         users
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    Dependency Layer for User Management
                Contains reusable dependency functions for authentication, authorization, database sessions, etc.
                Used with FastAPI's Depends system.
"""

from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from ..database import get_session
from .models import User

# Example dependency: get a user by ID
def get_user_by_id(user_id: str, session: Session = Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Add more user-related dependencies as needed
