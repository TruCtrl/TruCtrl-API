from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .models import Entity
from .crud import (
    create_entity,
    get_entity,
    list_entities,
    update_entity,
    delete_entity,
)
from ..database import get_session

router = APIRouter(prefix="/entity", tags=["Entity"])

@router.post("/", response_model=Entity)
def create(entity: Entity, session: Session = Depends(get_session)):
    return create_entity(session, entity)

@router.get("/", response_model=list[Entity])
def list_all(session: Session = Depends(get_session)):
    return list_entities(session)

@router.get("/{id}", response_model=Entity)
def get(id: str, session: Session = Depends(get_session)):
    entity = get_entity(session, id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

@router.put("/{id}", response_model=Entity)
def update(id: str, updates: dict, session: Session = Depends(get_session)):
    entity = update_entity(session, id, updates)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

@router.delete("/{id}", response_model=bool)
def delete(id: str, session: Session = Depends(get_session)):
    result = delete_entity(session, id)
    if not result:
        raise HTTPException(status_code=404, detail="Entity not found")
    return result
