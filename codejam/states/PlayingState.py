import pygame  as pg
from pygame.rect import Rect

from entities import GameMap
from entities.DungeonMaster import DungeonMasterGameObject
from entities.EnemyAdventurer import EnemyAdventurerGameObject
from services.AStar import AStar
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
            self.enemies = self.generate_enemies()
            self.persist['enemies'] = self.enemies

        if 'dungeon_master' in self.persist and self.persist['dungeon_master'] is not None:
            self.dungeon_master = self.persist['dungeon_master']
        else:
            self.persist['dungeon_master'] = self.dungeon_master

    def get_event(self, event):
        # Handle clicks here
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.game_map = GameMap.generate_game_map(self.map_width, self.map_height)
                self.enemies = self.generate_enemies()
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
        # TODO change this to drawing tiles or a mesh or something to improve performance
        for i in range(self.map_width):
            for j in range(self.map_height):
                rect = Rect(i + i * 5, j + j * 5, 5, 5)
                color = self.colors[self.game_map.generated_map[i][j]]
                pg.draw.rect(surface, color, rect)

        # TODO RESEARCH BATCH DRAWING METHODS
        self.dungeon_master.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)

    def generate_enemies(self):
        enemies = []
        starting_points = [
            (self.map_width - 2, 0),
            (1, 0),
            (self.map_width // 2, 0),
        ]

        self.players = []
        self.end_point = (self.map_width // 2, self.map_height // 2)

        solver = AStar()
        for i in range(0, len(starting_points) - 1):
            enemy = self.engine.generate_adventurer()

            # Dirty hack
            # minion wont move but should appear on screen, hardcoded to start, give Nick, Sy something to start on
            minion = self.engine.generate_minion()
            minion.position = (50 + (i*5), 50)
            #TODO functionally should have its own sprite group, managed by engine
            #   stuck it here to test out class
            enemies.append(minion)

            # ??
            solver.clear()
            solver.init_grid(self.map_width, self.map_height, (), starting_points[i], self.end_point)
            path = solver.solve()
            enemy.path = path
            enemy.position = starting_points[i]
            enemies.append(enemy)

        return enemies