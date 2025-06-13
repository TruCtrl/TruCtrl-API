# File:     crud.py
# Package:  users
# Package:  tructrl_api
# Project:  TruCtrl

# Standard Library Imports
from typing import List

# Third-Party Imports
from sqlmodel import Session, select

# Module Imports
from .models import User

# --- CRUD Operations ---


# List all
def list_all(session: Session) -> list[User]:
    statement = select(User)
    result = session.exec(statement)
    return list(result)

# Create
def create(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Upsert
def upsert(session: Session, user: User) -> User:
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

# Read
def read(session: Session, id: str) -> User | None:
    return session.get(User, id)

# Update
def update(session: Session, id: str, updates: dict) -> User | None:
    user = session.get(User, id)
    if not user:
        return None
    for key, value in updates.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Delete
def delete(session: Session, id: str) -> bool:
    user = session.get(User, id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True