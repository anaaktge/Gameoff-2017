from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pygame as pg
import math
import itertools

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


class EnemyAdventurerGameObject(pg.sprite.Sprite):

    id_generator = itertools.count(1)

    def __init__(self, enemy_entity=None, position=(0, 0), path=[]):

        super().__init__()

        self.id = next(self.id_generator)
        print("Enemy Adventurer init() id= "+str(self.id))

        self.entity = enemy_entity
        if self.entity is None:
            self.entity = EnemyAdventurer

        # TODO Convert this and path above to a queue and just pop things off it
        #TODO - Make Shay explain
        self.position = position
        self.starting_position = position
        self.end_position = None

        self.path = path
        self.next_step = 1
        self.current_step = 0
        # Current direction its moving
        self.directionX = 0
        self.directionY = 0


        # default values
        self.name = "Generic Adventurer"
        self.flavor_text = "I'm an adventurer"
        self.dead = False
        self.speed = 1
        self.sight = 1
        self.health = 10
        self.phase = "normal"
        self.attack = 1
        self.attack_type = "melee"  # general attacks are melee
        self.resistance = 0
        self.resistance_type = None
        self.weakness = 0
        self.weakness_type = None
        self.image = None
        self.gold = 1
        self.unicorn_tears = 0
        self.reputation = 1

        self.log_me()

    def handle_event(self, event):
        #print("Enemy Adventurer handle_event(" + str(event) + ")")
        # Mostly these seem to be mouse events, which we are not using atm
        pass

    def draw(self, surface):
        #print("Enemy Adventurer draw() should be blue")
        # If we dont have a graphic, default to a circle?
        # Remove this before shipping
        if self.image is None:
            #print("EnemyAdventurer.draw() defaulting to circle")
            blue = (0, 0, 250)
            pg.draw.circle(
                surface,
                blue,
                (int(self.position[0] * 5 + self.position[0]), int(self.position[1] * 5 + self.position[1])),
                4
            )
        if self.phase == "combat":
            print("EA id = " + str(self.id) + " name = " + self.name + "combat animation")
            # TODO Nick - Animate Combat here
        if self.phase == "normal":
            # TODO Nick - Amimate regular motion
            # print("EA id = " + str(self.id) + " name = " + self.name + "normal animation")
            pass

    def take_damage(self, damage_amt, damage_type):
        print("Enemy Adventurer id= " + str(self.id) + " take_damage(" + str(damage_amt) + "," + damage_type + ")")
        if damage_type == self.entity.immunity_type :
            print("\tadventurer is immune to that damage type")
            #TODO would be a good place to taunt the Dungeon Master
        self.entity.health -= damage_amt
        print("\tadventurer " + str(self.id) + " takes full damage. new health="+str(self.entity.health))
        if self.entity.health <= 0:
            print("\tadventurer " + str(self.id) + " is dead")
            self.dead = True

    #TODO rec
    def combat_check(self, distance=1):
        print("EnemyAdventurer.combat_check(" + str(distance) + ") id=" + str(id(self)))
        return False

    # TODO - bug in update
    def update(self, dt):
        #print("Enemy Adventurer base update()")

        # Since this can't know what the other sprite might be to do the proper pygame rect chec
        #it would be foolish to expect every adventurer to have knowlege of all
        #    the traps, minions, etc. race conditions galore

        # If there is no combat (interaction with traps count as combat) move on
        next_point = self.path[self.next_step]
        current_point = self.position
        sqrted = math.sqrt(
            math.pow(next_point[0] - current_point[0], 2) + math.pow(next_point[1] - current_point[1], 2))
        # If close enough (cough cough here be a bug) move to next point
        if sqrted <= 1:
            if (self.next_step <= len(self.path) - 4):
                self.update_direction()
                self.position = self.path[self.next_step]
                self.current_step = self.next_step
                self.next_step = self.next_step + 1
        else:
            dx = self.directionX * self.entity.speed / dt
            dy = self.directionY * self.entity.speed / dt
            self.position = (self.position[0] + dx, self.position[1] + dy)
        print("Enemy Adventurer id = " + str(self.id) + " type " + self.name + " moving to (" + str(self.position[0])+", " + str(self.position[1]) + ")")

    def update_direction(self):
        # print("Enemy Adventurer update_direction()")
        next_point = self.path[self.next_step]
        current_point = self.path[self.current_step]
        self.distance = math.sqrt(
            math.pow(next_point[0] - current_point[0], 2) + math.pow(next_point[1] - current_point[1], 2))
        self.directionX = (next_point[1] - current_point[1]) // self.distance
        self.directionY = (next_point[1] - current_point[1]) // self.distance

    def log_me(self):
        print("EA id = "+str(self.id) + " name = " + self.name)
        print("\t image path " + str(self.image))
        print("\t entity = "+ str(self.entity))
        print("\t dead = " + str(self.dead))
        print("\t phase = " + str(self.phase))
        print("\t health = " + str(self.health))
        print("\t speed = "+str(self.speed) + " sight distnace = " + str(self.sight))
        print("\t attack type = " + self.attack_type + " amt = " + str(self.attack))
        print("\t immunity type = " + str(self.resistance_type) + " amt = " + str(self.resistance))
        print("\t weakness type = " + str(self.weakness_type) + " amt = " + str(self.weakness))
        print("\t DM will gain: imfamy/reputation = " + str(self.reputation) + " gold = " + str(self.gold) + " unicorn tears = " + str(self.unicorn_tears))

        print("\t position is (" + str(self.position[0]) + ", " + str(self.position[1]) + ")")
        print("\t direction X = " + str(self.directionX) + " direction Y = " + str(self.directionY))
        print("\t starting position is (" + str(self.starting_position[0]) + ", " + str(self.starting_position[1]) + ")")
        # interpreter says i cant convert this one  to string
        # TODO bug Shay about this nonprintable type
        #print("\t ending position is (" + str(self.end_position[0]) + ", " + str(self.end_position[1]) + ")")
        print("\t current step = " + str(self.current_step) + " next step = " + str(self.next_step))
        print("\t path " + str(self.path))
        print("\t flavor text: " + str(self.flavor_text))

