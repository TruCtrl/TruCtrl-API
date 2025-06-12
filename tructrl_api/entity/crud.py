# File:     crud.py
# Package:  entity
# Package:  tructrl_api
# Project:  TruCtrl

# --- Imports ---

# Third-Party Imports
from sqlmodel import Session, select

# Module Imports
from .models import Entity

# Create
def create(session: Session, entity: Entity) -> Entity:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

# Read
def read(session: Session, id: str) -> Entity | None:
    return session.get(Entity, id)

# Update
def update(session: Session, id: str, updates: dict) -> Entity | None:
    entity = session.get(Entity, id)
    if not entity:
        return None
    for key, value in updates.items():
        setattr(entity, key, value)
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

# Delete
def delete(session: Session, id: str) -> bool:
    entity = session.get(Entity, id)
    if not entity:
        return False
    session.delete(entity)
    session.commit()
    return True

# List
def list(session: Session) -> list[Entity]:
    statement = select(Entity)
    return list(session.exec(statement))

# Upsert
def upsert(session: Session, entity: Entity) -> Entity:
    existing = session.get(Entity, entity.id)
    if existing:
        for key, value in entity.dict(exclude_unset=True).items():
            setattr(existing, key, value)
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    else:
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity