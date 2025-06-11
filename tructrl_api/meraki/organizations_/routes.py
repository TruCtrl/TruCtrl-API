from fastapi import APIRouter, Depends
from sqlmodel import Session
from ...database import get_session
from .services import sync_meraki_organizations
from .services import fetch_meraki_organizations
from .schemas import MerakiOrganizationRead

meraki_organizations_router = APIRouter(prefix="/organizations", tags=["Meraki Organizations"])

@meraki_organizations_router.get("/", status_code=200, response_model=list[MerakiOrganizationRead])
def get_meraki_organizations(session: Session = Depends(get_session)):
    """
    Fetch remote Meraki organizations using the getOrganizations API endpoint.
    """
    
    organizations = fetch_meraki_organizations()  # Call without await
    return organizations

@meraki_organizations_router.post("/sync", status_code=202)
def sync_organizations(session: Session = Depends(get_session)):
    """
    Fetch remote Meraki organizations and upsert them into the local database.
    """
    organizations = fetch_meraki_organizations()
    from .services import upsert_meraki_organizations
    upsert_meraki_organizations(session, organizations)
    return {"detail": "Meraki organizations sync completed."}



