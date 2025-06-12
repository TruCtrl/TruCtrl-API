# File:     routes.py
# Package:  entity
# Package:  tructrl_api
# Project:  TruCtrl

# Standard Library Imports
from typing import List

# Third-Party Imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

# Project Imports
from ..database import get_session

# Module Imports
from .constants import *
from .models import Entity
from .crud import create, read, update, delete, list, upsert

# Router Setup
router = APIRouter(prefix="/entity", tags=[ENTITY])

@router.get("", response_model=List[Entity])
def list_entity(session: Session = Depends(get_session)):
    return list(session)

@router.post("", response_model=Entity)
def create_entity(entity: Entity, session: Session = Depends(get_session)):
    return create(session, entity)

@router.post("/upsert", response_model=Entity)
def upsert_entity(entity: Entity, session: Session = Depends(get_session)):
    return upsert(session, entity)

@router.get("/{id}", response_model=Entity)
def read_entity(id: str, session: Session = Depends(get_session)):
    entity = read(session, id)
    if not entity:
        raise HTTPException(status_code=404, detail=ENTITY_NOT_FOUND)
    return entity

@router.put("/{id}", response_model=Entity)
def update_entity(id: str, updates: dict, session: Session = Depends(get_session)):
    entity = update(session, id, updates)
    if not entity:
        raise HTTPException(status_code=404, detail=ENTITY_NOT_FOUND)
    return entity

@router.delete("/{id}", response_model=bool)
def delete_entity(id: str, session: Session = Depends(get_session)):
    result = delete(session, id)
    if not result:
        raise HTTPException(status_code=404, detail=ENTITY_NOT_FOUND)
    return result