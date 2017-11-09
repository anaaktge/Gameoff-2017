from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Minion(Base):
    __tablename__ = 'minions'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class MinionGameObject(object):
    def __init__(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pass

    def take_damage(self, damage):
        pass

    def update(self, dt):
        pass
