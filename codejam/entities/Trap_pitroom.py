from entities.DefenderSprite import DefenderSprite
import pygame as pg


class Pitroom(DefenderSprite):
    def __init__(self):
        super().__init__()
        self.entity = Pitroom
        self.name = "Pitroom"
        self.flavor_text = "A giant pit where the room should be"
        self.image.fill(self.colors["purple"])
        print("pitroom init id= " + str(self.id))

    def update(self, dt):
        #print("pitroom update")
        super().update(dt)

    def draw(self, surface):
        #print("pitroom.draw()")
        super().draw(surface)

