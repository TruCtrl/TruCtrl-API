from sqlmodel import Session, select
from .models import MerakiOrganization
from typing import List

# Create
def create_organization(session: Session, org: MerakiOrganization) -> MerakiOrganization:
    session.add(org)
    session.commit()
    session.refresh(org)
    return org


# Read (by id)
def get_organization(session: Session, id: str) -> MerakiOrganization | None:
    return session.get(MerakiOrganization, id)

# Read (by remote_id)
def get_organization_by_remote_id(session: Session, remote_id: str) -> MerakiOrganization | None:
    statement = select(MerakiOrganization).where(MerakiOrganization.remote_id == remote_id)
    return session.exec(statement).first()

# List all
def list_organizations(session: Session) -> List[MerakiOrganization]:
    statement = select(MerakiOrganization)
    return list(session.exec(statement))

# Update
def update_organization(session: Session, id: str, updates: dict) -> MerakiOrganization | None:
    org = session.get(MerakiOrganization, id)
    if not org:
        return None
    for key, value in updates.items():
        setattr(org, key, value)
    session.add(org)
    session.commit()
    session.refresh(org)
    return org

# Delete
def delete_organization(session: Session, id: str) -> bool:
    org = session.get(MerakiOrganization, id)
    if not org:
        return False
    session.delete(org)
    session.commit()
    return True
