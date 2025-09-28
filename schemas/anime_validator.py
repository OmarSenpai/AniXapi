import pydantic, datetime
from pydantic import BaseModel, PositiveInt, ConfigDict, field_serializer, model_validator
from datetime import date
from typing import Literal, Optional
from utils.uuid_conv import binary_to_uuid, uuid_to_binary

class NewAnime(BaseModel):
    name: str
    jp_name: str
    episodes: PositiveInt
    format: Literal["TV", "movie"]
    start_date: date
    end_date: date
    studio_uuid: str

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def check_anime_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("start date can't come after end date !")
        return self


class AnimeResponse(BaseModel):
    uuid: str
    name: str
    jp_name: str
    episodes: PositiveInt
    format: Literal["TV", "movie"]
    start_date: date
    end_date: date
    studio_uuid: str

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('uuid')
    def serialize_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)


class AnimeUpdate(BaseModel):
    uuid: Optional[str] = None
    name: Optional[str] = None
    jp_name: Optional[str] = None
    episodes: Optional[PositiveInt] = None
    format: Optional[Literal["TV", "movie"]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    studio_uuid: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('uuid')
    def serialize_uuid(self, uuid_binary:bytes) -> str:
        return binary_to_uuid(uuid_binary)

    @model_validator(mode='after')
    def check_anime_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("start date can't come after end date !")
        return self

