import os

from entities.Minion import MinionGameObject
import pygame as pg

class Shop(object):
    def __init__(self):
        self.wrapper =  pg.image.load(os.path.join('assets', "shop_wrapper.png"))
        self.wrapper.convert()
        self.options = {
            'Minion': {
                'clazz': MinionGameObject,
                'cost': 10,
                'img': 'goblin_face.png'
            },
            'Minion2': {
                'clazz': MinionGameObject,
                'cost': 10,
                'img': 'goblin_face.png'
            },
            'Minion3': {
                'clazz': MinionGameObject,
                'cost': 10,
                'img': 'goblin_face.png'
            },
            'Minion4': {
                'clazz': MinionGameObject,
                'cost': 10,
                'img': 'goblin_face.png'
            },
            'Minion5': {
                'clazz': MinionGameObject,
                'cost': 10,
                'img': 'goblin_face.png'
            }
        }
        self.font = pg.font.Font(None, 24)

    def draw(self, surface):
        i=0
        surface.blit(self.wrapper, (0,0))
        for name, item in self.options.items():
            title = self.font.render(name, True, pg.Color("black"))
            surface.blit(title, (75, 120*i+110))
            img = pg.image.load(os.path.join('assets', item['img']))
            img.convert()
            img = pg.transform.scale(img, (100,100))
            surface.blit(img, (50, 120*i+120))
            i+=1