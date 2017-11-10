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
        self.map_width = 60
        self.map_height = 100
        self.colors = [
            (0, 0, 0),
            (255, 255, 255),
            (255, 0, 0),
            (0, 0, 255)
        ]
        self.rectangle = Rect(0, 0, 1000, 1000)
        self.size = (1950, 1100)
        self.zoom = 1
        self.engine = EnemyWaveGenerator()
        self.add_thing = False
        self.shop = None
        self.drag_mouse = False

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
        self.rectangle.centerx = self.game_map.ending_room.x
        self.rectangle.centery = self.game_map.ending_room.y

    def get_event(self, event):
        # Handle clicks here
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.MOUSEBUTTONUP:
            self.drag_mouse = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                if self.zoom > 0.2:
                    self.zoom -= .1
            elif event.button == 5:
                if self.zoom < 1.2:
                    self.zoom += .1
            if event.button == 1:
                if not self.add_thing:
                    self.drag_mouse = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rectangle.centerx - mouse_x
                    self.offset_y = self.rectangle.centery - mouse_y
                else:
                    self.game_map.generated_map[10][10] = 4

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
        draw_surface = self.get_drawable_surface()

        sub_surface = pg.Surface((self.rectangle.size[0] * self.zoom, self.rectangle.size[1] * self.zoom))

        sub_surface.blit(draw_surface, (0, 0),
                         Rect(self.rectangle.x, self.rectangle.y, 600 + (200 * self.zoom), 8000 + (200 * self.zoom)))

        s = pg.transform.scale(sub_surface, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(s, (0, 0), (0, 0, self.screen_rect.width, self.screen_rect.height))
        shop_surface = self.shop.draw((200, 800))
        surface.blit(shop_surface, (1080, 0))

    def get_drawable_surface(self):
        draw_surface = pg.Surface((6000, 6000))
        # TODO change this to drawing tiles or a mesh or something to improve performance
        for i in range(self.map_width):
            for j in range(self.map_height):
                rect = Rect(i + i * 5, j + j * 5, 5, 5)
                color = self.colors[self.game_map.generated_map[i][j]]
                pg.draw.rect(draw_surface, color, rect)

        # TODO RESEARCH BATCH DRAWING METHODS
        self.dungeon_master.draw(draw_surface)
        for enemy in self.enemies:
            enemy.draw(draw_surface)

        return draw_surface
