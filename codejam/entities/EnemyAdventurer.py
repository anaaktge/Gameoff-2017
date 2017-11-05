from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import pygame as pg
import math

Base = declarative_base()


class EnemyAdventurer(Base):
    __tablename__ = 'enemy'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    speed = Column(Integer)
    health = Column(Integer)


class EnemyAdventurerGameObject(object):
    def __init__(self, enemy_entity=None, position=(0, 0), path=[]):

        # Create a saveable entitiy
        # basically the entity is the loaded type from the DB
        # Make sure not to destroy it, however the game object is transient so please kill it
        self.entity = enemy_entity
        if self.entity is None:
            self.entity = EnemyAdventurer

        # Creating a dead game object is silly, lets avoid that
        self.dead = False

        # TODO Convert this and path above to a queue and just pop things off it
        self.position = position
        self.starting_position = position
        self.end_position = None

        self.path = path
        self.next_step = 1
        self.current_step = 0
        # Current direction its moving
        self.directionX = 0
        self.directionY = 0

    def handle_event(self, event):
        # Do whatever handling for the event that gets passed in here
        pass

    def draw(self, surface):
        # Prolly all this will become a blit image, we may wanna refactor to mass blit at some point
        pg.draw.circle(
            surface,
            (255, 0, 0),
            (int(self.position[0] * 10), int(self.position[1] * 10)),
            4
        )

    def take_damage(self, damage):
        ##elf explanitory
        self.entity.health -= damage
        if self.entity.health <= 0:
            self.dead = True

    def update(self, dt):
        # This is called erry tick so do whatever updates here
        next_point = self.path[self.next_step]
        current_point = self.position

        sqrted = math.sqrt(
            math.pow(
                next_point[0] - current_point[0],
                2
            ) +
            math.pow(
                next_point[1] - current_point[1],
                2)
        )

        # If close enough (cough cough here be a bug) move to next point
        if sqrted <= 1:
            if (self.next_step <= len(self.path) - 2):
                self.update_direction()
                self.position = self.path[self.next_step]
                self.current_step = self.next_step
                self.next_step = self.next_step + 1
        else:
            dx = self.directionX * self.entity.speed / dt
            dy = self.directionY * self.entity.speed / dt
            self.position = (self.position[0] + dx, self.position[1] + dy)

    def update_direction(self):
        # MAAATHHHHHHHHH
        next_point = self.path[self.next_step]
        current_point = self.path[self.current_step]
        self.distance = math.sqrt(
            math.pow(next_point[0] - current_point[0], 2) + math.pow(next_point[1] - current_point[1], 2))
        self.directionX = (next_point[1] - current_point[1]) // self.distance
        self.directionY = (next_point[1] - current_point[1]) // self.distance
