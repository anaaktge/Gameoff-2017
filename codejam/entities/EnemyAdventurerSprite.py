import math
import itertools

import pygame as pg
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from entities.GameSprite import BasicGameSprite

Base = declarative_base()

"""
ToDo: 
    understand Shay's code
    add a taunt table - adventurers taunt player
    add images 
    collision detection= no events, you have to do a `if rect_1.rect.colliderect(rect_2)`
"""


# For DB use, do not destroy
class EnemyAdventurer(Base):
    __tablename__ = 'enemy'

    id = Column(Integer, primary_key=True)
    image = Column(String)
    name = Column(String)
    flavor_text = Column(String)
    speed = Column(Integer)
    health = Column(Integer)
    phase = Column(String)
    attack = Column(Integer)
    attack_type = Column(String)
    gold = Column(Integer)
    unicorn_tears = Column(Integer)
    reputation = Column(Integer)
    resistance_type = Column(String)
    resistance = Column(Integer)
    weakness = Column(Integer)
    weakness_type = Column(String)
    sight = Column(Integer)


# basically the entity is the loaded type from the DB
# Make sure not to destroy it, however the game object is transient so please kill it


class EnemyAdventurerSprite(BasicGameSprite):
    def __init__(self, enemy_entity=None, position=(0, 0), path=[]):

        super().__init__()

        self.entity = EnemyAdventurer
        self.name = "Generic Adventurer"
        self.flavor_text = "I'm an adventurer"
        self.dead = False
        self.speed = 1
        self.sight = 1
        self.health = 10
        self.phase = "normal"
        self.taunts = ["Your father smelt of elderberries"]
        self.attack_amt = 1
        self.attack_type = "melee"  # general attacks are melee
        self.resistance_amt = 0
        self.resistance_type = None
        self.weakness_amt = 0
        self.weakness_type = None
        self.gold = 1
        self.unicorn_tears = 0
        self.reputation = 1

        self.image.fill(self.colors["blue"])

    def draw(self, surface):
        # print("Enemy Adventurer draw() should be blue")
        super().draw(surface)

    def update(self, dt):
        # movement
        next_point = self.path[self.next_step]
        sqrted = math.sqrt(
            math.pow(next_point[0] - self.rect.x, 2) + math.pow(next_point[1] - self.rect.y, 2))
        if sqrted <= 1:
            if self.next_step <= len(self.path) - 4:
                self.update_direction()
                self.rect.x = self.path[self.next_step][0]
                self.rect.y = self.path[self.next_step][1]
                self.current_step = self.next_step
                self.next_step = self.next_step + 1
        else:
            dx = self.directionX * self.entity.speed / dt
            dy = self.directionY * self.entity.speed / dt
            self.rect.x = self.rect.x + dx
            self.rect.y = self.rect.y + dy
        print("Enemy Adventurer id = " + str(self.id) + " type " + self.name + " moving to ("
              + str(self.rect.x) + ", " + str(self.rect.y) + ")")

    def update_direction(self):
        # print("Enemy Adventurer update_direction()")
        next_point = self.path[self.next_step]
        current_point = self.path[self.current_step]
        distance = math.sqrt(
            math.pow(next_point[0] - current_point[0], 2) + math.pow(next_point[1] - current_point[1], 2))
        self.directionX = (next_point[1] - current_point[1]) // distance
        self.directionY = (next_point[1] - current_point[1]) // distance
