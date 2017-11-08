import os
from pygame.rect import Rect
import pygame  as pg

from entities import GameMap
from entities.DungeonMaster import DungeonMasterGameObject
from entities.EnemyAdventurer import EnemyAdventurerGameObject
from entities.Shop import Shop
from services.AStar import AStar
from states.GameState import GameState


class PlayingState(GameState):
    def __init__(self):
        super(PlayingState, self).__init__()
        self.dungeon_master = DungeonMasterGameObject()
        self.enemies = None
        self.shop = Shop()
        self.game_map = None
        self.map_width = 36*2
        self.map_height = 66*2
        self.zoom = 1
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
        self.rectangle = Rect(0,0,1000,1000)
        self.drawn_size = 10
        self.offset_y = 0
        self.offset_x = 0
        self.add_thing = False

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
            self.enemies = self.generate_enemies()
            self.persist['enemies'] = self.enemies

        if 'dungeon_master' in self.persist and self.persist['dungeon_master'] is not None:
            self.dungeon_master = self.persist['dungeon_master']
        else:
            self.persist['dungeon_master'] = self.dungeon_master
        self.rectangle.centerx = self.game_map.ending_room.x
        self.rectangle.centery = self.game_map.ending_room.y

    def get_event(self, event):
        # Handle clicks here
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                self.add_thing = not self.add_thing
            if event.key == pg.K_ESCAPE:
                self.done = True
                self.quit = True
            if event.key == pg.K_t:
                self.game_map = GameMap.generate_game_map(self.map_width, self.map_height)
                self.enemies = self.generate_enemies()
        if event.type == pg.MOUSEBUTTONUP:
            self.drag_mouse = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.zoom -= .01
            elif event.button == 5:
                self.zoom += .01
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
                self.rectangle.center = (mouse_x + self.offset_x , mouse_y + self.offset_y)
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
        draw_surface = pg.Surface((6000, 6000))
        # DRAW EVERYTHING HERE
        # TODO change this to drawing tiles or a mesh or something to improve performance
        for i in range(0,self.map_width-1):
            for j in range(0, self.map_height-1):
                rect = Rect(i * 20, j * 20, 20, 20)
                color = self.sprites[self.game_map.generated_map[i][j]]
                if self.rectangle.contains(rect) and self.game_map.generated_map[i][j]!=1:
                    color = pg.transform.scale(color, (20,20))
                    draw_surface.blit(color, rect)

        # TODO RESEARCH BATCH DRAWING METHODS
        self.dungeon_master.draw(draw_surface)
        for enemy in self.enemies:
            enemy.draw(draw_surface)
        #this does the drawing in the square on the screen
        #TODO prolly figure out a better method of doing this
        sub_surface = pg.Surface(self.rectangle.size)
        sub_surface.blit(draw_surface, (0, 0), Rect(self.rectangle.x,self.rectangle.y,800,1000))
        s = pg.transform.scale(sub_surface, (self.screen_rect.width, self.screen_rect.height))
        surface.blit(s, (0,0), (0,0,self.screen_rect.width, self.screen_rect.height))
        self.draw_sidebar(surface)

    def generate_enemies(self):
        enemies = []
        solver = AStar()
        walls = []
        for i in range(0, self.game_map.width):
            for j in range(0, self.game_map.height):
                if self.game_map.generated_map[i][j] != 0:
                    walls.append((i, j))

        enemy = EnemyAdventurerGameObject()
        enemy.entity.speed = 2
        solver.clear()
        solver.init_grid(self.map_width, self.map_height, walls, self.game_map.starting_room.get_pos(), self.game_map.ending_room.get_pos())
        path = solver.solve()
        enemy.position = self.game_map.starting_room.get_pos()
        self.persist['path'] = path
        enemy.path = path
        enemies.append(enemy)
        return enemies

    def draw_sidebar(self, surface):
        draw_surface = pg.Surface((200, 800))
        self.shop.draw(draw_surface)
        surface.blit(draw_surface, (1080,0))


