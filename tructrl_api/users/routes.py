# File:     routes.py
# Package:  users
# Package:  tructrl_api
# Project:  TruCtrl


# --- Imports ---

# Standard Library Imports
from typing import List

# Third-Party Imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

# Project Imports
from ..database import get_session

# Module Imports
from .constants import *
from .models import User
from .crud import list, create, upsert, read, update, delete

# Router Setup
router = APIRouter(prefix="/users", tags=[USERS])


# --- CRUD Endpoints ---

# List
@router.get("", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    return list(session)

# Create
@router.post("", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    return create(session, user)

# Upsert
@router.post("/upsert", response_model=User)
def upsert_user(user: User, session: Session = Depends(get_session)):
    return upsert(session, user)

# Read
@router.get("/{id}", response_model=User)
def get_user(id: str, session: Session = Depends(get_session)):
    user = read(session, id)
    if not user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return user

# Update
@router.put("/{id}", response_model=User)
def update_user(id: str, updates: dict, session: Session = Depends(get_session)):
    user = update(session, id, updates)
    if not user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return user

# Delete
@router.delete("/{id}", response_model=bool)
def delete_user(id: str, session: Session = Depends(get_session)):
    result = delete(session, id)
    if not result:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return result
