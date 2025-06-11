from sqlmodel import SQLModel, Field
import ulid

class Entity(SQLModel, table=True):
    id: str = Field(default_factory=lambda: ulid.new().str, primary_key=True, description="ULID primary key")
    type: str = Field(description="Type of the entity, e.g., 'organization', 'user', 'device', etc.")




