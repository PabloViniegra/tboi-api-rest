from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class PlainItemSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    quality: Optional[int] = None
    type: Optional[str] = None
    icon: Optional[str] = None
    item_pool: Optional[list[str]] = None


class ItemSchema(PlainItemSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResponseItemSchema(BaseModel):
    count: int
    pages: int
    page: int
    items: List[ItemSchema]

    model_config = ConfigDict(from_attributes=True)


class PatchItemSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    quality: Optional[int] = None
    type: Optional[str] = None
    icon: Optional[str] = None
    item_pool: Optional[list[str]] = None

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
