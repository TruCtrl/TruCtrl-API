from pydantic import BaseModel
from typing import Optional, List

class MerakiOrganizationAPI(BaseModel):
    enabled: Optional[bool] = True

class MerakiOrganizationLicensing(BaseModel):
    model: Optional[str] = "co-term"

class MerakiOrganizationCloudRegionHost(BaseModel):
    name: Optional[str] = "United States"

class MerakiOrganizationCloudRegion(BaseModel):
    name: Optional[str] = "North America"
    host: Optional[MerakiOrganizationCloudRegionHost] = MerakiOrganizationCloudRegionHost()

class MerakiOrganizationCloud(BaseModel):
    region: Optional[MerakiOrganizationCloudRegion] = MerakiOrganizationCloudRegion()

class MerakiOrganizationManagementDetail(BaseModel):
    name: Optional[str] = "customer number"
    value: Optional[str] = "CUSTOMER_NUMBER_EXAMPLE"

class MerakiOrganizationManagement(BaseModel):
    details: Optional[List[MerakiOrganizationManagementDetail]] = [MerakiOrganizationManagementDetail()]

class MerakiOrganizationRead(BaseModel):
    id: str = "ORG_ID_EXAMPLE"
    name: str = "Example Organization"
    url: Optional[str] = "https://example.meraki.com/o/EXAMPLE/manage/organization/overview"
    api: Optional[MerakiOrganizationAPI] = MerakiOrganizationAPI()
    licensing: Optional[MerakiOrganizationLicensing] = MerakiOrganizationLicensing()
    cloud: Optional[MerakiOrganizationCloud] = MerakiOrganizationCloud()
    management: Optional[MerakiOrganizationManagement] = MerakiOrganizationManagement()

