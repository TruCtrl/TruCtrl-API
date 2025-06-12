# File:     routes.py
# Package:  organizations
# Package:  meraki
# Package:  tructrl_api
# Project:  TruCtrl


# ----- Imports ------

# Standard Imports
from typing import List

# Third-Party Imports
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

# Project Imports
from ...database import get_session

# Package Imports
from .models import Organization
from .crud import list, create, upsert, read, update, delete

# Router Setup
router = APIRouter()


# ------ CRUD Endpoints -----

# List
@router.get("", response_model=List[Organization])
def list_organizations(session: Session = Depends(get_session)):
    return list(session)

# Create
@router.post("", response_model=Organization)
def create_organization(organizaton: Organization, session: Session = Depends(get_session)):
    return create(session, organizaton)

# Upsert
@router.post("/upsert", response_model=Organization)
def upsert_organization(organization: Organization, session: Session = Depends(get_session)):
    return upsert(session, organization)

# Read
@router.get("/{id}", response_model=Organization)
def read_organization(id: str, session: Session = Depends(get_session)):
    org = read(session, id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

# Update
@router.put("/{id}", response_model=Organization)
def update_organization(id: str, updates: dict, session: Session = Depends(get_session)):
    org = update(session, id, updates)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

# Delete
@router.delete("/{id}", response_model=bool)
def delete_organization(id: str, session: Session = Depends(get_session)):
    result = delete(session, id)
    if not result:
        raise HTTPException(status_code=404, detail="Organization not found")
    return result
