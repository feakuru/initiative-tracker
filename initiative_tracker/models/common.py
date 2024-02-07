from pydantic import BaseModel


class Status(BaseModel):
    code: int
    message: str
