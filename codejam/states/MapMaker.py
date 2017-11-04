from pygame.rect import Rect
import pygame as pg
from services.AStar import AStar
from states.GameState import GameState


class MapMaker(GameState):
    def __init__(self, h=101, w=61):
        super(MapMaker, self).__init__()
        self.map = [[1 for x in range(h)] for y in range(w)]
        self.width = w
        self.height = h

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for i in range(self.width):
            for j in range(self.height):
                rect = Rect(i + i * 5, j + j * 5, 5, 5)
                color = self.colors[self.map[i][j]]
                pg.draw.rect(surface, color, rect)
        for player in self.players:
            pg.draw.circle(surface, (255, 0, 0), (
            int(player.position[0] * 5 + player.position[0]), int(player.position[1] * 5 + player.position[1])), 4)

    def generate_map2(self):
        self.map[self.width - 2][0] = 0
        self.map[1][0] = 0
        self.map[self.width // 2][0] = 0

        half_width = self.width // 2
        for i in range(half_width - 2, half_width + 2):
            for j in range(self.height // 2 - 2, self.height // 2 - 2):
                self.map[i][j] = 0

        solver = AStar()
        for i in range(0, len(self.starting_points)):
            solver.clear()
            solver.init_grid(self.width, self.height, (), self.starting_points[i], self.end_point)
            solution = solver.solve()
            if solution:
                for item in solution:
                    self.map[item[0]][item[1]] = 0

    def get_rooms(self):
        return []
