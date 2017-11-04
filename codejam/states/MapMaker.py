import random

from pygame.rect import Rect
import pygame as pg
import math
from services.AStar import AStar
from states.GameState import GameState

class P(object):
    def __init__(self, starting_position, end_position, w, h):
        self.position = starting_position
        self.starting_position = starting_position
        self.end_position = end_position
        self.find_path(w, h)
        self.speed = 2
        self.health = 100
        self.dead = False

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True

    def do_update(self, dt):
        next_point = self.solution[self.next_step]
        current_point = self.position
        self.take_damage(1)
        sqrted = math.sqrt(math.pow(next_point[0]-current_point[0],2)+ math.pow(next_point[1]-current_point[1],2))
        if  sqrted <=1:
            if (self.next_step <= len(self.solution)-4):
                self.update_direction()
                self.position = self.solution[self.next_step]
                self.current_step = self.next_step
                self.next_step = self.next_step + 1
        else:
            dx = self.directionX * self.speed/dt
            dy = self.directionY * self.speed/dt
            self.position = (self.position[0]+ dx, self.position[1]+dy)

    def find_path(self, w, h):
        solver = AStar()
        solver.init_grid(w, h, (), self.starting_position, self.end_position)
        self.solution = solver.solve()
        self.next_step = 1
        self.current_step = 0
        self.update_direction()

    def update_direction(self):
        next_point = self.solution[self.next_step]
        current_point = self.solution[self.current_step]
        self.distance = math.sqrt(math.pow(next_point[0]-current_point[0],2)+ math.pow(next_point[1]-current_point[1],2))
        self.directionX = (next_point[1] - current_point[1]) // self.distance
        self.directionY = (next_point[1] - current_point[1]) // self.distance


class MapMaker(GameState):
    def __init__(self, h=101, w=61):
        super(MapMaker, self).__init__()
        self.map = [[1 for x in range(h)] for y in range(w)]
        self.width = w
        self.height = h

        self.colors = [
            (0, 0, 0),
            (255, 255, 255),
            (255, 0, 0)
        ]
        self.starting_points = [
            (self.width - 2, 0),
            (1, 0),
            (self.width // 2, 0),
        ]

        self.players = []
        self.end_point = (self.width // 2, self.height//2)
        self.generate_map2()
        for item in self.starting_points:
            self.players.append(P(item, self.end_point, w, h))


    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.generate_map2()

    def update(self, dt):
        for player in self.players:
            player.do_update(dt)
            if player.dead:
                self.players.remove(player)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for i in range(self.width):
            for j in range(self.height):
                rect = Rect(i + i * 5, j + j * 5, 5, 5)
                color = self.colors[self.map[i][j]]
                pg.draw.rect(surface, color, rect)
        for player in self.players:
            pg.draw.circle(surface, (255,0,0), (int(player.position[0]*5+player.position[0]), int(player.position[1]*5+player.position[1])), 4)

    def generate_map2(self):
        self.map[self.width-2][0] = 0
        self.map[1][0] = 0
        self.map[self.width//2][0]=0

        half_width = self.width//2
        for i in range(half_width-2, half_width+2):
            for j in range(self.height//2-2, self.height//2-2):
                self.map[i][j] = 0

        solver = AStar()
        for i in range(0, len(self.starting_points)):
            solver.clear()
            solver.init_grid(self.width, self.height, (), self.starting_points[i],  self.end_point)
            solution = solver.solve()
            if solution:
                for item in solution:
                    self.map[item[0]][item[1]] = 0

    def get_rooms(self):
        return []