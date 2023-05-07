from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SuperPower(str, Enum):
    FLIGHT = "flight"
    SUPER_STRENGTH = "super-strength"
    SUPER_SPEED = "super-speed"
    GILLS = "gills"
    RICH = "rich"
    LEVITATION = "levitation"


class HealthResponse(BaseModel):
    status: str


class UpdateSuperhero(BaseModel):
    name: Optional[str]
    super_power: Optional[SuperPower]
    hometown: Optional[str]


class CreateSuperhero(UpdateSuperhero):
    name: str = Field(None, example="Batman")
    super_power: SuperPower = Field(None, example=SuperPower.RICH)


class GetSuperhero(CreateSuperhero):
    id: UUID


class GetHeroes(BaseModel):
    heroes: List[GetSuperhero]
