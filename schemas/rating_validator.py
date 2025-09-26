import pydantic
from pydantic import BaseModel, NonNegativeFloat

class rating(BaseModel):
    value: NonNegativeFloat
