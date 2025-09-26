import pydantic, datetime
from pydantic import BaseModel, Field, field_validator, UUID4, PositiveInt
from datetime import date
from typing import Optional, Literal

class new_anime(BaseModel):
    name: str
    jp_name: str
    episodes: PositiveInt
    format: Literal["TV", "movie"]
    start_date: date
    end_date: date
    studio_uuid: UUID4

class update_anime(BaseModel):
    name: str
    jp_name: str
    episodes: PositiveInt
    format: Literal["TV", "movie"]
    start_date: date
    end_date: date
    studio_uuid: UUID4

