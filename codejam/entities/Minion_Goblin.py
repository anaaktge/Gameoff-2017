from entities.Minion import MinionGameObject
import pygame as pg


class Goblin(MinionGameObject):
    def __init__(self):
        print("Goblin.__init__()")
        super(Goblin, self).__init__()
        self.dead = False
        self.name = "Goblin"
        self.flavor_text = "I'll wipe that smile off your smug mug"
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
        self.image = None

    def draw(self, surface):
        print("Golbin.draw(), should be green")
        # If we dont have a graphic, default to a circle?
        if self.image is None:
            print("\tdefaulting to circle")
            green = (0, 255, 0)
            pg.draw.circle(
                surface,
                green,
                (int(self.position[0] * 5 + self.position[0]), int(self.position[1] * 5 + self.position[1])),
                4
            )
    def handle_event(self, event):
        print("Goblin.handle_event()")
        super().handle_event(event)

    def update(self, dt):
        print("Goblin.update")
        super().update(dt)
