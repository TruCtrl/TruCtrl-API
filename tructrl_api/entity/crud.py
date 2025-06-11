from sqlmodel import Session, select
from .models import Entity

# Create

def create_entity(session: Session, entity: Entity) -> Entity:
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity

# Read (by id)
def get_entity(session: Session, id: str) -> Entity | None:
    return session.get(Entity, id)

# List all
def list_entities(session: Session) -> list[Entity]:
    statement = select(Entity)
    return list(session.exec(statement))

# Update
def update_entity(session: Session, id: str, updates: dict) -> Entity | None:
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
def delete_entity(session: Session, id: str) -> bool:
    entity = session.get(Entity, id)
    if not entity:
        return False
    session.delete(entity)
    session.commit()
    return True
