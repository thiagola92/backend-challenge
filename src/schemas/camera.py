from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, field_serializer


class Camera(BaseModel):
    id: str = Field(examples=[uuid4()])
    name: str = Field(examples=["Alice"])
    ip: IPvAnyAddress = Field(examples=["127.0.0.1"])
    is_enabled: bool = Field(examples=[True])
    customer_id: str = Field(examples=[uuid4()])

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("ip")
    def serialize_ip(self, ip) -> str:
        return str(ip)
