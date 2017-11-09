import pygame as pg

from entities.Enemy_Ranger import EnemyRanger
from entities.Minion_Goblin import Goblin

#Spits out adventurers
# Probably will have to manage combat ?

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

    def generate_wave(self):
        print("generating wave of enemies")
        # add to the groups
        pass

    def update(self):
        #will be called form palying state
        # do combat checks
        pass