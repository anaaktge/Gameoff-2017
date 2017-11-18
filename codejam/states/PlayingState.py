import pygame as pg
from pygame.rect import Rect

from entities import GameMap
from entities.DungeonMaster import DungeonMasterGameObject
from services.SpritesEngine import SpritesEngine
from states.GameState import GameState


class PlayingState(GameState):
    def __init__(self):
        super(PlayingState, self).__init__()
        self.dungeon_master = DungeonMasterGameObject()
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
        self.engine = SpritesEngine(self.map_width, self.map_height)

    def startup(self, persistent):
        self.persist = persistent
        # Ensure everything exists and is persisted across states
        if 'game_map' in self.persist and self.persist['game_map'] is not None:
            self.game_map = self.persist['game_map']
        else:
            self.game_map = GameMap.generate_game_map(self.map_width, self.map_height)
            self.persist['map'] = self.game_map

        # TODO Convert to wave generator at some point
        if 'engine' in self.persist and self.persist['engine'] is not None:
            self.engine = self.persist['engine']
        else:
            self.persist['engine'] = self.engine

        if 'dungeon_master' in self.persist and self.persist['dungeon_master'] is not None:
            self.dungeon_master = self.persist['dungeon_master']
        else:
            self.persist['dungeon_master'] = self.dungeon_master

        #anaaktge test
        self.engine.test()

    def get_event(self, event):
        # Handle clicks here
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.game_map = GameMap.generate_game_map(self.map_width, self.map_height)
        self.dungeon_master.handle_event(event)
        self.engine.handle_event()

    # When a minion gets hired or a trap gets bought
    #   do whatever needs to be done here
    def add_defender(self, shiny_new_toy):
        self.engine.add(shiny_new_toy)
        print("added new defender")

    def update(self, dt):
        # Do all tick based updates here
        # These things include checking if a wave is done, updating minions,enemies, traps, yourself
        # autosave would go here
        # see SplashScreen for timeout example
        # Basically we need to have a "state" machine here to toggle between during wave and non wave times
        # TODO WRITE THIS
        self.dungeon_master.update(dt)
        self.engine.update(dt)

    def draw(self, surface):
        # DRAW EVERYTHING HERE
        surface.fill(pg.Color("black"))
        # TODO change this to drawing tiles or a mesh or something to improve performance
        for i in range(self.map_width):
            for j in range(self.map_height):
                rect = Rect(i + i * 5, j + j * 5, 5, 5)
                color = self.colors[self.game_map.generated_map[i][j]]
                pg.draw.rect(surface, color, rect)

        # TODO RESEARCH BATCH DRAWING METHODS
        self.dungeon_master.draw(surface)
        self.engine.draw(surface)

