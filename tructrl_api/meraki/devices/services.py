from sqlmodel import Session
from ..organizations.services import get_meraki_dashboard_client
from ...config import config

def fetch_meraki_organization_devices(api_key: str, organization_id: str) -> list[dict]:
    dashboard = get_meraki_dashboard_client(api_key)
    return dashboard.organizations.getOrganizationDevices(organization_id)

def upsert_meraki_organization_devices(session: Session, organization_id: str, devices: list[dict]):
    from .models import MerakiOrganizationDevice
    for dev in devices:
        db_dev = session.get(MerakiOrganizationDevice, dev["serial"])
        if db_dev:
            db_dev.model = dev.get("model")
            db_dev.name = dev.get("name")
            db_dev.mac = dev.get("mac")
            db_dev.network_id = dev.get("networkId")
        else:
            db_dev = MerakiOrganizationDevice(
                serial=dev["serial"],
                organization_id=organization_id,
                model=dev.get("model"),
                name=dev.get("name"),
                mac=dev.get("mac"),
                network_id=dev.get("networkId")
            )
            session.add(db_dev)
    session.commit()

def sync_meraki_organization_devices(session: Session, organization_id: str):
    devices = fetch_meraki_organization_devices(config.meraki_api_key, organization_id)
    upsert_meraki_organization_devices(session, organization_id, devices)
