# File:     routes.py
# Package:  devices
# Package:  meraki
# Package:  tructrl_api
# Project:  TruCtrl

from fastapi import APIRouter, Depends
from sqlmodel import Session
from ...database import get_session
from .services import sync_meraki_organization_devices, fetch_meraki_organization_devices
from .models import MerakiOrganizationDevice
from .schemas import MerakiDeviceRead
from ...config import config

devices_router = APIRouter(prefix="/devices", tags=["Meraki Devices"])

@devices_router.post("/sync/{organization_id}", status_code=202)
def sync_devices(organization_id: str, session: Session = Depends(get_session)):
    """
    Sync Meraki devices for an organization from the Meraki cloud and upsert to the local database.
    """
    sync_meraki_organization_devices(session, organization_id)
    return {"detail": f"Meraki devices sync started for organization {organization_id}."}