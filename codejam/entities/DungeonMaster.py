from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class DungeonMaster(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gold = Column(Integer)
    infamy = Column(Integer)
    unicorn_tears = Column(Integer)
    health = Column(Integer)