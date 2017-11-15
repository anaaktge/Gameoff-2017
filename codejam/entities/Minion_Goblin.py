from entities.DefenderSprite import DefenderSprite
import pygame as pg


class Goblin(DefenderSprite):
    def __init__(self):
        super().__init__()
        self.dead = False
        self.name = "Goblin"
        self.flavor_text = "You don't pay enough for manners"
        self.taunts = ["I'll wipe that smile off your smug mug"]
        self.speed = 1
        self.sight = 2
        self.health = 10
        self.attack = 1
        self.attack_type = "melee"  # general attacks are melee
        self.gold_cost = 2
        self.unicorn_tears_cost = 0
        self.reputation_cost = 0  # not a true cost, this minion will only work for you when you are evil enough
        self.immunity_type = None
        self.weakness = 0
        self.weakness_type = None
        self.image.fill(self.colors["green"])
        print("Goblin.__init__() id = " + str(self.id))

    def update(self, dt):
        #print("Goblin.update")
        super().update(dt)
