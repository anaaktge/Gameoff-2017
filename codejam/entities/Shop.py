import json
import os

import pygame as pg


class Shop(object):
    def __init__(self, dungeon_master):
        self.dm = dungeon_master
        self.inventory = {}
        with open(os.path.join('assets', 'minions.json')) as data_file:
            self.inventory = json.load(data_file)
        self.font = pg.font.Font(None, 24)
        self.image = pg.image.load(os.path.join('assets', 'shop_wrapper.png'))
        self.coin_image = pg.image.load(os.path.join('assets', 'coin.png'))
        self.coin_image.convert()
        self.coin_image = pg.transform.scale(self.coin_image,(20, 20))
        self.tears_image = pg.image.load(os.path.join('assets', 'tears.png'))
        self.tears_image.convert()
        self.tears_image = pg.transform.scale(self.tears_image, (20, 20))
    def draw(self, surface_size):
        surface = pg.Surface(surface_size)
        surface.blit(self.image, (0,0))
        i = 0
        for item in self.inventory:
            self.draw_item(i, item, surface)

            i += 1
        return surface

    def draw_item(self, i, item, surface):
        title = self.font.render(item['name'], True, pg.Color("black"))
        surface.blit(title, (50, 110 * i + 130))
        img = pg.image.load(os.path.join('assets', item['image']))
        img.convert()
        img = pg.transform.scale(img, (75, 75))
        surface.blit(img, (30, 110 * i + 140))
        surface.blit(self.coin_image, (105, 110 * i + 150))
        title = self.font.render("%s" % item['gold_cost'], True, pg.Color("black"))
        surface.blit(title, (130, 110 * i + 153))

        surface.blit(self.tears_image, (105, 110 * i + 180))
        title = self.font.render("%s" % item['unicorn_tear_cost'], True, pg.Color("black"))
        surface.blit(title, (130, 110 * i + 183))

