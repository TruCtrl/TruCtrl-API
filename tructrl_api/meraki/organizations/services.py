# File:     services.py
# Package:  organizations
# Package:  meraki
# Package:  tructrl_api
# Project:  TruCtrl

from sqlmodel import Session
from meraki import DashboardAPI
from .models import MerakiOrganization
from .crud import (
    create,
    read,
    list,
    update,
    delete,
    upsert
)
from typing import List

def pull(session: Session, id: str) -> List[MerakiOrganization]:
    # Use the API Key of the specified Meraki organization.
    org = read(session, id)
    if not org or not org.api_key:
        return []
    dash = DashboardAPI(api_key=org.api_key)
    cloud_orgs = dash.organizations.getOrganizations()
    upserted_orgs = []
    for cloud_org in cloud_orgs:
        model_data = MerakiOrganization.from_meraki_api(cloud_org)
        model_data.api_key = org.api_key  # Always use the stored API key
        upserted = upsert(session, model_data)
        upserted_orgs.append(upserted)
    return upserted_orgs