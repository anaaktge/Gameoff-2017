from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pygame as pg
from entities.GameSprite import BasicGameSprite

Base = declarative_base()


# DB object do not destroy
class Defender(Base):
    __tablename__ = 'minions'

    id = Column(Integer, primary_key=True)
    image = Column(String)
    name = Column(String)
    flavor_text = Column(String)
    speed = Column(Integer)
    health = Column(Integer)
    attack = Column(Integer)
    attack_type = Column(String)
    gold_cost = Column(Integer)
    unicorn_tears_cost = Column(Integer)
    reputation_cost = Column(Integer)
    resistance_type = Column(String)
    resistance = Column(Integer)
    weakness = Column(Integer)
    weakness_type = Column(String)
    sight = Column(Integer)
    phase = Column(String)


class DefenderSprite(BasicGameSprite):
    def __init__(self):
        super().__init__()

        self.entity = DefenderSprite
        self.name = "Base Minion&Trap"
        self.flavor_text = "Yes master"
        self.dead = False
        self.speed = 1
        self.sight = 1
        self.health = 10
        self.phase = "normal"
        self.taunts = ["Who do you think you are? Dirk the Dauntless?"]
        self.attack_amt = 1
        self.attack_type = "melee"  # general attacks are melee
        self.resistance_amt = 0
        self.resistance_type = None
        self.weakness_amt = 0
        self.weakness_type = None
        self.gold = 1
        self.unicorn_tears = 0
        self.reputation = 1
        self.image.fill(self.colors["pink"])

    def draw(self, surface):
        # print("Minion.draw should be pink")
        super().draw(surface)

    # minions should probably just stay put where they are placed for now
    def update(self, dt):
        # print("Minion.update()")
        super().update(dt)
