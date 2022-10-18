from pydantic import BaseModel
from typing import Union

class Device(BaseModel):
    id: int
    code: str
    name: str
    size: str
    weight: int
    provider: Union[str, None] = None
    description: Union[str, None] = None