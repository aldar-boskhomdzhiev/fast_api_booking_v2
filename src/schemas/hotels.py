from pydantic import BaseModel

class Hotel(BaseModel):
    title: str
    name: str
