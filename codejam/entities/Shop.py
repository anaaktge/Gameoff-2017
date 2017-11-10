import json
import os

import pygame as pg


class Shop(object):
    def __init__(self, dungeon_master, ):
        self.dm = dungeon_master
        self.inventory = {}
        with open(os.path.join('assets', 'minions.json')) as data_file:
            self.inventory = json.load(data_file)
        self.font = pg.font.Font(None, 24)

    def draw(self, surface_size):
        surface = pg.Surface(surface_size)
        surface.fill(pg.Color("grey"))
        i = 0
        for item in self.inventory:
            title = self.font.render(item['name'], True, pg.Color("black"))
            surface.blit(title, (75, 120 * i + 110))
            #img = pg.image.load(os.path.join('assets', item['img']))
            #img.convert()
            #img = pg.transform.scale(img, (100, 100))
            #surface.blit(img, (50, 120 * i + 120))
            i += 1
        return surface
