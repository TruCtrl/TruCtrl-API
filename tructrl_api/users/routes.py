"""
File:         routes.py
Module:       users
Project:      TruCtrl-API
Copyrigh:     © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:      MIT
Description:  API routes for user management in the TruCtrl-API application.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session, select
from ..database import get_session
from ..auth.dependencies import get_current_user
from .models import User

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@users_router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@users_router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
