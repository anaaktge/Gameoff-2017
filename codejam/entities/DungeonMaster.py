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


# TODO WRITE THIS CRAP
class DungeonMasterGameObject(object):
    def __init__(self, dungeon_master_entitiy=None):
        self.entity = dungeon_master_entitiy
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
