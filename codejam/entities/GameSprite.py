# Base Class for Game Sprites since there's a lot there have in common

import math
import itertools
import random

import pygame as pg
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

"""
ToDo: 
    move Taunts to json?
    rename table 

"""

"""
Notes
    desendants responsible for draw() and update functions()
    
    Values 
        (x,y) self.position = position
        (x,y) self.starting_position = position
        (x,y) self.end_position = None
        [] self.path = path
        int self.next_step = 1
        int self.current_step = 0
        int self.directionX = 0
        int self.directionY = 0
        str self.name = Adventurer typ name
        str self.flavor_text = basic flavour text
        bool self.dead = is the game sprite still alive
        int self.speed = speed the sprite came move, should eventually represent the numbers of tiles 
        int self.sight = distance to engage enemy 
        int self.health = sprite is dead when health is 0 
        str self.phase = "normal", "combat"
        int self.attack_amt = 1
        str self.attack_type = "melee"  # general attacks are melee
        int self.resistance_amt = 0
        str self.resistance_type = None
        int self.weakness_amt = 0
        str self.weakness_type = None
        [] self.taunt = 
        str self.image = None
        int self.gold = 1
        int self.unicorn_tears = 0
        int self.reputation = For Adventurers, the amount of imfamy the DM will gain, for killing them, 
            for defenders it represents a minion amount of infamy they require to work for that DM 
            
            
    self.position in shays code needs to be self.rect.x/y as thats how pygame sprites move 
"""


# For DB use, do not destroy
class GameSprite(Base):
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


# For game use, destroy away
class BasicGameSprite(pg.sprite.Sprite):
    id_generator = itertools.count(1)

    # immunities and weaknesses come from this list as well
    damage_types = ["melee",
                    "fire",
                    "mental"]

    # states sprites can be in
    phase = ["normal",
             "combat"]

    # colors in one place
    colors = {"black": (0, 0, 0), # basegamesprite
              "red": (255, 0, 0), #Ranger
              "pink": (255, 200, 200), #DefenderSprite base
              "blue": (0, 0, 250), #EnemyAdventurer base
              "green": (0, 255, 0), #Goblin
              "purple": (128,0,128) #pitroom
              }

    def __init__(self, entity=None, position=(0, 0), path=[]):

        super().__init__()

        self.id = next(self.id_generator)
        #print("Base class init() id= " + str(self.id))

        self.entity = entity
        if self.entity is None:
            self.entity = GameSprite

        self.starting_position = position
        self.end_position = None

        self.path = path
        self.next_step = 1
        self.current_step = 0
        # Current direction its moving
        self.directionX = 0
        self.directionY = 0

        # default values
        self.name = "Base Sprite"
        self.flavor_text = "If you see this, you've done something wrong"
        self.dead = False
        self.speed = 1
        self.sight = 1
        self.health = 5
        self.phase = "normal"
        self.attack_amt = 1
        self.attack_type = "melee"  # general attacks are melee
        self.resistance_amt = 0
        self.resistance_type = None
        self.weakness_amt = 0
        self.weakness_type = None
        self.taunts = ["yo mama"]
        self.gold = 0
        self.unicorn_tears = 0
        self.reputation = 0

        # there must be an image & a rect for most of the pygames sprite class code to work
        # This could also be an image loaded from the disk.
        self.image = pg.Surface([10, 10])
        self.image.fill(self.colors["black"])

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    def handle_event(self, event):
        # print("Sprite handle_event(" + str(event) + ")")
        # Mostly these seem to be mouse events, which we are not using atm
        super().handle_event(event)
        pass

    def draw(self, surface):
        super().draw(surface)

    def update(self, dt):
        super().update(dt)

    def random_taunt(self):
        i = random.randint(0, len(self.taunts) - 1)
        taunt = self.taunts[i]
        print("taunting " + taunt)

    def take_damage(self, damage_type, damage_amt):
        print("id= " + str(self.id) + " take_damage(" + str(damage_amt) + "," + str(damage_type) + ")")

        if damage_type == self.resistance_type:
            print("\tid = " + str(self.id) + "is immune to that damage type")
            # TODO add in resistance chipping away its self.resitance_amt
            self.random_taunt()

        if damage_type == self.weakness_type:
            # TODO add in weakness types
            pass

        # generic damage then
        self.health -= damage_amt
        print("\t id " + str(self.id) + " takes full damage. new health=" + str(self.health))

        if self.health <= 0:
            print("\t id " + str(self.id) + " is dead")
            self.dead = True

    def log_me(self):
        print("id = " + str(self.id) + " name = " + self.name)
        print("\t image path " + str(self.image))
        print("\t entity = " + str(self.entity))
        print("\t dead = " + str(self.dead))
        print("\t phase = " + str(self.phase))
        print("\t health = " + str(self.health))
        print("\t speed = " + str(self.speed) + " sight distnace = " + str(self.sight))
        print("\t attack type = " + self.attack_type + " amt = " + str(self.attack_amt))
        print("\t immunity type = " + str(self.resistance_type) + " amt = " + str(self.resistance_amt))
        print("\t weakness type = " + str(self.weakness_type) + " amt = " + str(self.weakness_amt))
        print("\t DM will gain: imfamy/reputation = " + str(self.reputation) + " gold = " + str(
            self.gold) + " unicorn tears = " + str(self.unicorn_tears))

        print("\t position is (" + str(self.position[0]) + ", " + str(self.position[1]) + ")")
        print("\t direction X = " + str(self.directionX) + " direction Y = " + str(self.directionY))
        print(
            "\t starting position is (" + str(self.starting_position[0]) + ", " + str(self.starting_position[1]) + ")")
        # interpreter says i cant convert this one  to string
        # TODO bug Shay about this nonprintable type
        # print("\t ending position is (" + str(self.end_position[0]) + ", " + str(self.end_position[1]) + ")")
        print("\t current step = " + str(self.current_step) + " next step = " + str(self.next_step))
        print("\t path " + str(self.path))
        print("\t flavor text: " + str(self.flavor_text))
