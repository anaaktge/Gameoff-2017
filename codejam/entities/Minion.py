from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Minion(Base):
    __tablename__ = 'minions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
