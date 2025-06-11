from sqlmodel import SQLModel, Field
from typing import Optional

class MerakiNetwork(SQLModel, table=True):
    __tablename__ = "meraki_networks"
    id: str = Field(primary_key=True)
    organization_id: str = Field(index=True)
    name: str
    product_types: Optional[str] = None  # Comma-separated or JSON string
    tags: Optional[str] = None
    time_zone: Optional[str] = None
    notes: Optional[str] = None
    # Add more fields as needed from the Meraki API response