# File:     routes.py
# Package:  networks
# Package:  meraki
# Package:  tructrl_api
# Project:  TruCtrl

from fastapi import APIRouter, Depends
from sqlmodel import Session
from ...database import get_session
from .services import sync_meraki_organization_networks

networks_router = APIRouter(prefix="/networks", tags=["Meraki Networks"])

@networks_router.post("/sync/{organization_id}", status_code=202)
def sync_networks(organization_id: str, session: Session = Depends(get_session)):
    """
    Sync Meraki networks for an organization from the Meraki cloud and upsert to the local database.
    """
    sync_meraki_organization_networks(session, organization_id)
    return {"detail": f"Meraki networks sync started for organization {organization_id}."}
