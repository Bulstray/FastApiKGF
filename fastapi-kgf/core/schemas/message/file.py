from pydantic import BaseModel


class MessageFile(BaseModel):
    name: str
    content: str
