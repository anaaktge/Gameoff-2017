import pygame as pg

from services.AStar import AStar
from entities.GameSprite import BasicGameSprite
from entities.Enemy_Ranger import EnemyRanger
from entities.Minion_Goblin import Goblin
from entities.Trap_pitroom import Pitroom
import random

"""
anaaktge - game sprites

TODO
    add taunts to characters
    sprites should be dropping out when dying 
"""

class SpritesEngine(object):
    adventurer_ypes = ["Ranger"]
    minion_types = ["Goblin"]
    trap_types = ["Pitroom"]

    def __init__(self, map_width, map_height):
        #print("wave generator: init() ")
        # things will drop out when they are killed
        self.defenses = pg.sprite.Group()
        self.adventurers = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.combat_pairs = []
        self.wave_level = 0
        self.wave_population = 1
        self.map_width = map_width
        self.map_height = map_height
        self.solver = AStar()

    def generate_adventurer(self):
        # TODO pick a random index from the type list
        victim = EnemyRanger()
        #print("Engine generated " + victim.name + " id = " + str(victim.id))
        #print("\t health=" + str(victim.health))
        #print("\t sight=" + str(victim.sight))
        #print("\t speed=" + str(victim.speed))
        self.adventurers.add(victim)
        self.all_sprites.add(victim)

        starting_point = (self.map_width - 2, 0)
        end_point = (self.map_width // 2, self.map_height // 2)

        victim.rect.x = starting_point[0]
        victim.rect.y = starting_point[1]

        self.solver.clear()
        self.solver.init_grid(self.map_width, self.map_height, (), starting_point, end_point)
        path = self.solver.solve()
        victim.path = path

        return victim

    def generate_wave(self):
        print("engine. generate_wave()")
        # add to the groups
        for i in range(0, self.wave_population):
            self.generate_adventurer()
            print("\t\t generating adventurer # " + str(i))
        # increase wave count after generating every wave
        self.wave_level += 1
        self.wave_population = random.randint(self.wave_population, self.wave_population * self.wave_level)
        print(
            "\t wave level is now = " + str(self.wave_level) + " wave population is now = " + str(self.wave_population))

    # avoid friendly fire on both sides
    def combat_check(self):
        print("engine.combat_check()")
        for defender in self.defenses.sprites():
            print("\tchecking for combat against defender id= " + str(defender.id))
            trespassers = pg.sprite.spritecollide(defender, self.adventurers, False)
            if trespassers:
                # combat is 1 on 1
                self.combat_pairs.append((defender, trespassers[0]))
                print("\t\t combat pair created, enemy is id= " + str(trespassers[0].id) + " defender " + str(defender.id))

    #Ensure every one has a rect for combat purposes
    def combat(self):
        print("engine.combat()")
        for pair in self.combat_pairs:
            print("\t combat pair starting")
            defender = pair[0]
            trespasser = pair[1]
            initiator = defender  # if case of ties defender attacks first
            slowpoke = trespasser
            if defender.sight < trespasser.sight:
                # trespasser attacks first
                initiator = trespasser
                slowpoke = defender
            while initiator.health > 0 and slowpoke.health > 0:
                # TODO initator taunts
                slowpoke.take_damage(initiator.attack_type, initiator.attack_amt)
                # TODO slowpoke taunts
                initiator.take_damage(slowpoke.attack_type, slowpoke.attack_amt)
            print("\t 1 combat ended")
            self.combat_pairs.remove(pair)

    def update(self, dt):
        self.all_sprites.update(dt)
        # TODO send events to each pair to do their thing in an event driven manner
        self.combat_check()
        self.combat()
        pass

    def draw(self, surface):
        #print("engine.draw()")
        self.all_sprites.draw(surface)

    def handle_event(self):
        # TODO do we even need the engine to handle events?
        pass

    # test functions


    # remember that (0,0) is top left corner
    def test(self):
        minion = self.generate_minion()
        minion.rect.x = 80
        minion.rect.y = 80
        trap = self.generate_trap()
        trap.rect.x = 100
        trap.rect.y = 100

        self.generate_wave()
        self.generate_wave()

    def generate_minion(self):
        minion = Goblin()
        #print("Engine generated " + minion.name + " id = " + str(minion.id))
        #print("\t health=" + str(minion.health))
        #print("\t sight=" + str(minion.sight))
        #print("\t speed=" + str(minion.speed))
        self.defenses.add(minion)
        self.all_sprites.add(minion)
        return minion

    def generate_trap(self):
        trap = Pitroom()
        #print("Engine generated trap")
        self.defenses.add(trap)
        self.all_sprites.add(trap)
        return trap
