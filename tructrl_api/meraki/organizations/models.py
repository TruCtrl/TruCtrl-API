from sqlmodel import SQLModel, Field
from typing import Optional
import ulid

class MerakiOrganization(SQLModel, table=True):
    __tablename__ = "meraki_organizations"
    id: str = Field(default_factory=lambda: ulid.new().str, primary_key=True, description="ULID primary key")
    api_key: Optional[str] = "CHANGEMECHANGEMECHANGEMECHANGEMECHANGEME"
    remote_id: str = "2930418"
    name: str = "My organization"
    url: Optional[str] = "https://dashboard.meraki.com/o/VjjsAd/manage/organization/overview"
    api_enabled: Optional[bool] = True
    licensing_model: Optional[str] = "co-term"
    cloud_region_name: Optional[str] = "North America"
    cloud_region_host_name: Optional[str] = "United States"
    management_msp_id: Optional[str] = "123456"

    @classmethod
    def from_meraki_api(cls, data: dict):
        return cls(
            remote_id=data["id"],
            name=data["name"],
            url=data.get("url"),
            api_enabled=(data.get("api") or {}).get("enabled"),
            licensing_model=(data.get("licensing") or {}).get("model"),
            cloud_region_name=(data.get("cloud") or {}).get("region", {}).get("name"),
            cloud_region_host_name=(data.get("cloud") or {}).get("region", {}).get("host", {}).get("name"),
            management_msp_id=(data.get("management") or {}).get("details", [{}])[0].get("value")
        )