from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)

    @model_validator(mode="after")
    def required_fields_cannot_be_null(self) -> "ItemUpdate":
        for field in {"name", "price"} & self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class ItemRead(ItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
