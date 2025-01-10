from src.database.db import Base
from sqlalchemy import Column, Integer, String, Text

class Monster(Base):
    __tablename__ = 'monsters'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=True)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
