from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pygame as pg
import itertools

Base = declarative_base()

#TODO it might make sense for traps to inherit from MinionGameObject

# DB object do not destroy
class Minion(Base):
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



class MinionGameObject(pg.sprite.Sprite):
    id_generator = itertools.count(1)

    def __init__(self, position=(0, 0)):
        super().__init__()

        self.id = next(self.id_generator)
        print("Minion.__init__() id= "+str(self.id))

        self.dead = False
        self.name = "Generic Minion"
        self.flavor_text = "Yes, Master"
        self.speed = 1
        self.sight = 1
        self.health = 10
        self.attack = 1
        self.attack_type = "melee"  # general attacks are melee
        self.gold_cost = 1
        self.unicorn_tears_cost = 0
        self.reputation_cost = 0 # not a true cost, this minion will only work for you when you are evil enough
        self.resistance_type = None
        self.resistance = 0
        self.weakness = 0
        self.weakness_type = None
        self.image = None
        self.phase = "normal"
        self.position = position

        self.log_me()

    def handle_event(self, event):
        print("Minion.handle_event()")
        pass

    def draw(self, surface):
        print("Minion.draw should be pink")
        if self.image is None:
            print("\tdefaulting to circle")
            pink = (255, 200, 200)
            pg.draw.circle(
                surface,
                pink,
                (int(self.position[0] * 5 + self.position[0]), int(self.position[1] * 5 + self.position[1])),
                4
            )

    # resistance wears off after a while
    def take_damage(self, damage_amt, damage_type):
        print("Minion.take_damage(" + str(damage_amt) + "," + damage_type + ")")
        if damage_type == self.resistance_type:
            if self.resistance <= 0:
                self.health -= damage_amt
                # If the resistance drops below 0, you've lost it
                self.resistance_type = None
                self.resistance = 0 # If fell below, reset to 0
                print("minion has lost its resistance")
            else:
                self.resistance -= damage_amt
                print("\tminion is resistant to that damage type, new resistance = " + str(self.resistance))
        self.health -= damage_amt
        print("\tminion takes full damage. new health="+str(self.entity.health))
        if self.health <= 0:
            print("\tminion id= " + str(self.id) + "is dead")
            self.dead = True
            # TODO Nick - animate death?
            self.kill()

    def do_attack(self):
        print("Minion.attack")
        pass

    def combat_check(self, distance):
        print("Minion.combat_check(distance=" + str(distance) + ")")
        return False

    # minions should probably just stay put where they are placed for now
    def update(self, dt):
        print("Minion.update()")
        if self.combat_check(self.sight):
            # engage in combat
            # unclear if we need both a take damage and an attack function
            self.do_attack()
            print("\tMinion starting combat")

    def log_me(self):
        print("Minion, id = "+str(self.id) + " type" + self.name)
        print("\t image path " + str(self.image))
        print("\t dead = " + str(self.dead))
        print("\t phase = " + str(self.phase))
        print("\t health = " + str(self.health))
        print("\t speed = "+str(self.speed) + " sight distance = " + str(self.sight))
        print("\t attack type = " + self.attack_type + " amt = " + str(self.attack))
        print("\t immunity type = " + str(self.resistance_type) + " amt = " + str(self.resistance))
        print("\t weakness type = " + str(self.weakness_type) + " amt = " + str(self.weakness))
        print("\t DM cost: reputation = " + str(self.reputation_cost) + " gold = " + str(self.gold_cost) + " unicorn tears = " + str(self.unicorn_tears_cost))

        # TODO Should minions move? Might be bonus feature
        print("\t position is (" + str(self.position[0]) + ", " + str(self.position[1]) + ")")
        #print("\t direction X = " + str(self.directionX) + " direction Y = " + str(self.directionY))
        #print("\t starting position is (" + str(self.starting_position[0]) + ", " + str(self.starting_position[1]) + ")")
        # interpreter says i cant convert this one  to string
        # TODO bug Shay about it
        #print("\t ending position is (" + str(self.end_position[0]) + ", " + str(self.end_position[1]) + ")")
        #print("\t current step = " + str(self.current_step) + " next step = " + str(self.next_step))
        #print("\t path " + str(self.path))
        print("\t flavor text: " + str(self.flavor_text))