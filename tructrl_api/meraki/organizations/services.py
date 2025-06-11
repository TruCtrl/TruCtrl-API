from sqlmodel import Session
from meraki import DashboardAPI
from .models import MerakiOrganization
from .crud import (
    create_organization,
    get_organization,
    get_organization_by_remote_id,
    list_organizations,
    update_organization,
    delete_organization,
)

# Fetch organizations from Meraki cloud

def fetch_meraki_organizations_from_cloud(api_key: str = None) -> list[dict]:
    """
    Call the Meraki Dashboard API to get organizations.
    """
    # If api_key is not provided, use the default from dashboard.py
    dash = DashboardAPI(api_key=api_key)
    return dash.organizations.getOrganizations()

# Upsert a single organization from Meraki cloud into the local DB by remote_id

def sync_meraki_organization(session: Session, remote_id: str, api_key: str = None):
    orgs = fetch_meraki_organizations_from_cloud(api_key)
    for org in orgs:
        if org.get("id") == remote_id:
            model_data = MerakiOrganization.from_meraki_api(org)
            existing = get_organization_by_remote_id(session, model_data.remote_id)
            if existing:
                update_organization(session, existing.id, model_data.dict(exclude_unset=True))
            else:
                create_organization(session, model_data)
            break
