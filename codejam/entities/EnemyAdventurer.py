from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Enemy(Base):
    __tablename__ = 'enemy'

    id = Column(Integer, primary_key=True)
    name = Column(String)
