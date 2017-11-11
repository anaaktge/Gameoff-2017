import os

import pygame  as pg
from pygame.rect import Rect

from entities import GameMap
from entities.DungeonMaster import DungeonMasterGameObject
from entities.Shop import Shop
from services.EnemyWaveGenerator import EnemyWaveGenerator
from states.GameState import GameState


class PlayingState(GameState):
    def __init__(self):
        super(PlayingState, self).__init__()
        self.dungeon_master = DungeonMasterGameObject()
        self.enemies = None
        self.shop = None
        self.game_map = None
        self.map_width = 36
        self.map_height = 66
        self.zoom = 1
        self.tile_width = 20
        self.sprites = [
            pg.image.load(os.path.join('assets', 'grass.png')),
            pg.image.load(os.path.join('assets', 'cobble.png')),
            pg.image.load(os.path.join('assets', 'player_start.png')),
            pg.image.load(os.path.join('assets', 'enemy_start.png'))
        ]
        # wall, path, start, end
        self.colors = [
            (165, 42, 42),
            (128, 128, 128),
            (255, 0, 0),
            (0, 0, 255),
            (0, 255, 0),
            (255, 255, 0)
        ]
        self.size = (1950, 1100)
        self.drag_mouse = False
        self.rectangle = Rect(0, 0, 1000, 1000)
        self.drawn_size = 10
        self.offset_y = 0
        self.offset_x = 0
        self.add_thing = False
        self.engine = EnemyWaveGenerator()

    def startup(self, persistent):
        self.persist = persistent
        # Ensure everything exists and is persisted across states
        if 'game_map' in self.persist and self.persist['game_map'] is not None:
            self.game_map = self.persist['game_map']
        else:
            self.game_map = GameMap.generate_game_map(self.map_width, self.map_height)
            self.persist['map'] = self.game_map

        # TODO Convert to wave generator at some point
        if 'enemies' in self.persist and self.persist['enemies'] is not None:
            self.enemies = self.persist['enemies']
        else:
            self.enemies = self.engine.generate_enemies(self.map_width, self.map_height,
                                                        self.game_map.starting_room.get_pos(),
                                                        self.game_map.ending_room.get_pos())
            self.persist['enemies'] = self.enemies

        if 'dungeon_master' in self.persist and self.persist['dungeon_master'] is not None:
            self.dungeon_master = self.persist['dungeon_master']
        else:
            self.persist['dungeon_master'] = self.dungeon_master

        self.shop = Shop(self.dungeon_master)
        self.rectangle.x = self.game_map.ending_room.x
        self.rectangle.y = self.game_map.ending_room.y

    def get_event(self, event):
        # Handle clicks here
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.MOUSEBUTTONUP:
            self.drag_mouse = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                if self.zoom > 0.3:
                    self.zoom -= .1
            elif event.button == 5:
                if self.zoom < 1.7:
                    self.zoom += .1
            elif event.button == 1:
                if not self.add_thing:
                    pass
        elif event.type == pg.MOUSEMOTION:
            if self.drag_mouse:
                mouse_x, mouse_y = event.pos
                self.rectangle.center = (mouse_x + self.offset_x, mouse_y + self.offset_y)

        self.dungeon_master.handle_event(event)
        # TODO ADD MINION AND TARP HANDLING
        for enemy in self.enemies:
            enemy.handle_event(event)

    def update(self, dt):
        # Do all tick based updates here
        # These things include checking if a wave is done, updating minions,enemies, traps, yourself
        # autosave would go here
        # see SplashScreen for timeout example
        # Basically we need to have a "state" machine here to toggle between during wave and non wave times
        # TODO WRITE THIS
        self.dungeon_master.update(dt)
        for enemy in self.enemies:
            enemy.update(dt)

    def draw(self, surface):
        # DRAW EVERYTHING HERE
        surface.fill(pg.Color("black"))
        draw_surface = self.do_draw()

        sub_surface = pg.Surface((self.rectangle.size[0], self.rectangle.size[1]))

        sub_surface.blit(draw_surface, (0, 0),
                         Rect(0, 0, 900, 1000))

        s = pg.transform.scale(sub_surface, (self.screen_rect.width, self.screen_rect.height))

        surface.blit(s, (0, 0), (0, 0, self.screen_rect.width, self.screen_rect.height))

        shop_surface = self.shop.draw((200, 800))
        surface.blit(shop_surface, (1080, 0))

    def do_draw(self):
        draw_surface = pg.Surface((6000, 6000))
        # DRAW EVERYTHING HERE
        # TODO change this to drawing tiles or a mesh or something to improve performance
        for i in range(0, self.map_width - 1):
            for j in range(0, self.map_height - 1):
                rect = Rect(i * self.tile_width*self.zoom+self.rectangle.x, j * self.tile_width*self.zoom+self.rectangle.y, int(self.tile_width*self.zoom), int(self.tile_width*self.zoom))
                color = self.sprites[self.game_map.generated_map[i][j]]
                if self.game_map.generated_map[i][j] != 1:
                    color = pg.transform.scale(color, (int(self.tile_width*self.zoom), int(self.tile_width*self.zoom)))
                    draw_surface.blit(color, rect)

        # TODO RESEARCH BATCH DRAWING METHODS
        self.dungeon_master.draw(draw_surface)
        for enemy in self.enemies:
            enemy.draw(draw_surface)

        return draw_surface
