import pygame as pg

from entities.Enemy_Ranger import EnemyRanger
from entities.Minion_Goblin import Goblin

#Spits out adventurers
# Probably will have to manage combat ?
from services.AStar import AStar


class EnemyWaveGenerator(object):
    def __init__(self):
        print("wave generator: init() ")
        # probably want to use the Sprite Groups that pygames seems to want

    def generate_adventurer(self):
        victim = EnemyRanger()
        print("WaveGen, generated " + victim.name + " id = " + str(victim.id))
        print("\t health="+ str(victim.health))
        print("\t sight=" + str(victim.sight))
        print("\t speed=" + str(victim.speed))
        return victim

    def generate_minion(self):
        minion = Goblin()
        print("WaveGen, generated " + minion.name + " id = " + str(minion.id))
        print("\t health="+ str(minion.health))
        print("\t sight=" + str(minion.sight))
        print("\t speed=" + str(minion.speed))
        return minion

    def generate_enemies(self, width, height, start_pos, end_pos):
        enemies = []
        solver = AStar()
        enemy = self.generate_adventurer()

        # Dirty hack
        # minion wont move but should appear on screen, hardcoded to start, give Nick, Sy something to start on
        minion = self.generate_minion()
        minion.position = (50, 50)
        #TODO functionally should have its own sprite group, managed by engine
        #   stuck it here to test out class
        enemies.append(minion)

        # ??
        solver.clear()
        solver.init_grid(width, height, (), start_pos, end_pos)
        path = solver.solve()
        enemy.path = path
        enemy.position = start_pos
        enemies.append(enemy)
        return enemies