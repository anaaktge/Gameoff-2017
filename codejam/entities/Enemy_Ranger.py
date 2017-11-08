import pygame as pg

from entities.EnemyAdventurer import EnemyAdventurerGameObject


class EnemyRanger(EnemyAdventurerGameObject):
    def __init__(self):
        super(EnemyRanger, self).__init__()
        #do not store this id, may not be unique, used for debugging during initial building
        print("Ranger.init() id = " + str(self.id))
        self.name = "Ranger"
        self.flavor_text = "Brooding Level 1 Loner"
        self.speed = 3
        self.health = 5
        self.attack = 2
        self.attack_type = "melee"  # general attacks are melee
        self.gold = 10
        self.unicorn_tears = 0
        self.reputation = 2
        self.immunity_type = "undead"
        self.weakness = 0
        self.weakness_type = "fire"
        #TODO once we have images, put the path here
        self.image = None

    def draw(self, surface):
        print("Ranger.draw(), should be red")
        # If we dont have a graphic, default to a circle?
        if self.image is None:
            print("\tdefaulting to circle")
            red = (255, 0, 0)
            pg.draw.circle(
                surface,
                red,
                (int(self.position[0] * 5 + self.position[0]), int(self.position[1] * 5 + self.position[1])),
                4
            )
    def handle_event(self, event):
        print("Ranger handle_event()")
        super().handle_event(event)
        # Do whatever handling for the event that gets passed in here
        pass

    def update(self, dt):
        print("Ranger update()")
        super().update(dt)
        pass
