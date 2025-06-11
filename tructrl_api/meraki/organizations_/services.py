"""
File:           services.py
Module:         meraki
Project:        TruCtrl-API
Copyrigh:       © 2025 McGuire Technology, LLC and TruCtrl Contributors
License:        MIT
Description:    Service layer for Meraki integration.
"""
from dotenv import load_dotenv
import os

# Load .env file for MERAKI_API_KEY
load_dotenv()

import meraki
from sqlmodel import Session
from .models import MerakiOrganization
from ...config import config  # Adjust if you store your API key elsewhere

def get_meraki_dashboard_client():
    api_key = os.getenv('MERAKI_API_KEY')
    if not api_key:
        raise ValueError('MERAKI_API_KEY not found in .env file')
    return meraki.DashboardAPI(api_key=api_key, suppress_logging=True)

def fetch_meraki_organizations() -> list[dict]:
    dashboard = get_meraki_dashboard_client()
    return dashboard.organizations.getOrganizations()

def upsert_meraki_organizations(session: Session, orgs: list[dict]):
    for org in orgs:
        db_org = session.get(MerakiOrganization, org["id"])
        if db_org:
            db_org.name = org["name"]
            db_org.url = org.get("url")
        else:
            db_org = MerakiOrganization(id=org["id"], name=org["name"], url=org.get("url"))
            session.add(db_org)
    session.commit()

def sync_meraki_organizations(session: Session):
    orgs = fetch_meraki_organizations()
    upsert_meraki_organizations(session, orgs)
