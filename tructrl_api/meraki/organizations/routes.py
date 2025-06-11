from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...database import get_session
from .models import MerakiOrganization
from .crud import (
    create_organization,
    get_organization,
    get_organization_by_remote_id,
    list_organizations,
    update_organization,
    delete_organization,
)
from .services import sync_meraki_organization

router = APIRouter(prefix="/organizations", tags=["Meraki Organizations"])

@router.post("", response_model=MerakiOrganization)
def create_org(org: MerakiOrganization, session: Session = Depends(get_session)):
    return create_organization(session, org)

@router.get("", response_model=list[MerakiOrganization])
def list_orgs(session: Session = Depends(get_session)):
    return list_organizations(session)

@router.get("/{id}", response_model=MerakiOrganization)
def get_org(id: str, session: Session = Depends(get_session)):
    org = get_organization(session, id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.get("/remote/{remote_id}", response_model=MerakiOrganization)
def get_org_by_remote_id(remote_id: str, session: Session = Depends(get_session)):
    org = get_organization_by_remote_id(session, remote_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.put("/{id}", response_model=MerakiOrganization)
def update_org(id: str, updates: dict, session: Session = Depends(get_session)):
    org = update_organization(session, id, updates)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.delete("/{id}", response_model=bool)
def delete_org(id: str, session: Session = Depends(get_session)):
    result = delete_organization(session, id)
    if not result:
        raise HTTPException(status_code=404, detail="Organization not found")
    return result

@router.post("/{id}/sync", response_model=MerakiOrganization)
def sync_org(id: str, session: Session = Depends(get_session)):
    sync_meraki_organization(session, id)
    org = get_organization_by_remote_id(session, id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found after sync")
    return org
