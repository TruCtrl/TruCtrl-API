# File:     crud.py
# Package:  organizations
# Package:  meraki
# Package:  tructrl_api
# Project:  TruCtrl

# --- Imports ---

# Standard Imports
from typing import List

# Third-Party Imports
from sqlmodel import Session, select

# Project Imports

# Module Imports
from .models import Organization

# List
def list(session: Session) -> List[Organization]:
    statement = select(Organization)
    return list(session.exec(statement))

# Create
def create(session: Session, org: Organization) -> Organization:
    session.add(org)
    session.commit()
    session.refresh(org)
    return org

# Upsert
def upsert(session: Session, org: Organization) -> Organization:
    existing = session.get(Organization, org.id)
    if existing:
        for key, value in org.dict(exclude_unset=True).items():
            setattr(existing, key, value)
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    else:
        session.add(org)
        session.commit()
        session.refresh(org)
        return org

# Read
def read(session: Session, id: str) -> Organization | None:
    return session.get(Organization, id)

# Update
def update(session: Session, id: str, updates: dict) -> Organization | None:
    org = session.get(Organization, id)
    if not org:
        return None
    for key, value in updates.items():
        setattr(org, key, value)
    session.add(org)
    session.commit()
    session.refresh(org)
    return org

# Delete
def delete(session: Session, id: str) -> bool:
    org = session.get(Organization, id)
    if not org:
        return False
    session.delete(org)
    session.commit()
    return True
