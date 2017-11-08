from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pygame as pg

Base = declarative_base()


class Trap(Base):
    __tablename__ = 'traps'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class TrapGameObject(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pass

    def take_damage(self, damage):
        pass

    def update(self, dt):
        pass
