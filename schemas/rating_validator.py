import pydantic
from pydantic import BaseModel, NonNegativeFloat, Field


class Rating(BaseModel):
    anime: str
    user: str
    value: Field(NonNegativeFloat, ge=0, le=5)

