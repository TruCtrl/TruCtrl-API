from pydantic import BaseModel
from typing import Optional

class MerakiDeviceRead(BaseModel):
    serial: str = "Q2XX-XXXX-XXXX"
    organization_id: str = "123456"
    model: Optional[str] = "MX68"
    name: Optional[str] = "Branch MX"
    mac: Optional[str] = "00:11:22:33:44:55"
    network_id: Optional[str] = "N_1234567890"
