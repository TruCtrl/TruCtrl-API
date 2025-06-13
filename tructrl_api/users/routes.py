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

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@router.post("", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/upsert", response_model=User)
def upsert_user(user: User, session: Session = Depends(get_session)):
    existing = session.get(User, user.id)
    if existing:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(existing, key, value)
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    else:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.get("/{id}", response_model=User)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{id}", response_model=User)
def update_user(id: int, user_update: User, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user




@router.delete("/{id}", response_model=bool)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()
    return True
    
    
@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user