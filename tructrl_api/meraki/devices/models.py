from sqlmodel import SQLModel, Field
from typing import Optional

# Rename class to match import usage
class MerakiOrganizationDevice(SQLModel, table=True):
    __tablename__ = "meraki_devices"
    serial: str = Field(primary_key=True)
    organization_id: str = Field(index=True)
    model: Optional[str] = None
    name: Optional[str] = None
    mac: Optional[str] = None
    network_id: Optional[str] = None
    # Add more fields as needed from the Meraki API response









