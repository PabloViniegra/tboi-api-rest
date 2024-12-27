from src.database.db import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    short_description = Column(String)
    quality = Column(Integer)
    description = Column(Text)
    type = Column(String)
    icon = Column(String)
    item_pool = Column(ARRAY(String))
