# File:     services.py
# Package:  networks
# Package:  meraki
# Package:  tructrl_api
# Project:  TruCtrl

from ..organizations.services import get_meraki_dashboard_client
from ...config import config
from .models import MerakiNetwork

def fetch_meraki_organization_networks(organization_id: str) -> list[dict]:
    dashboard = get_meraki_dashboard_client()
    return dashboard.organizations.getOrganizationNetworks(organization_id)

def upsert_meraki_organization_networks(session, organization_id: str, networks: list[dict]):
    for net in networks:
        db_net = session.get(MerakiNetwork, net["id"])
        if db_net:
            db_net.name = net["name"]
            db_net.product_types = str(net.get("productTypes"))
            db_net.tags = str(net.get("tags"))
            db_net.time_zone = net.get("timeZone")
            db_net.notes = net.get("notes")
        else:
            db_net = MerakiNetwork(
                id=net["id"],
                organization_id=organization_id,
                name=net["name"],
                product_types=str(net.get("productTypes")),
                tags=str(net.get("tags")),
                time_zone=net.get("timeZone"),
                notes=net.get("notes")
            )
            session.add(db_net)
    session.commit()

def sync_meraki_organization_networks(session, organization_id: str):
    networks = fetch_meraki_organization_networks(organization_id)
    upsert_meraki_organization_networks(session, organization_id, networks)
