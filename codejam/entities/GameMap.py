import random
from collections import deque
import math

from services.AStar import AStar


class GameMap(object):
    def __init__(self, w=60, h=100):
        self.width = w
        self.height = h
        # Initialize map to nothing
        self.generated_map = [[1 for x in range(self.height)] for y in range(self.width)]
        # initialize starting points and ending points to nothing, these will be filled in by generator
        self.starting_points = []
        self.ending_point = None


def __create_starting_points(size, end_position, side, min_distance, starting_points_count=1):
    starting_points = []
    while starting_points_count != 0:
        if side == 1:
            # left
            starting_point_x = 0
            starting_point_y = random.randint(0, size[1] - 1)
            pass
        else:
            # right
            starting_point_x = size[0] - 1
            starting_point_y = random.randint(0, size[1] - 1)
        point = (starting_point_x, starting_point_y)

        if math.hypot(end_position[0] - starting_point_x, end_position[1] - starting_point_y) > min_distance:
            starting_points.append(point)
            starting_points_count -= 1

    return starting_points


def __generate_ending_point(size):
    width, height = size
    side = random.randint(0, 1)
    if side == 0:
        # left
        pos_x = random.randint(5, 20)
        pos_y = random.randint(5, height - 5)
    else:
        # right
        pos_x = random.randint(width - 20, width - 5)
        pos_y = random.randint(5, height - 5)

    end_point = (pos_x, pos_y)
    return (end_point, side)


def __isFarAway(x1, x2, y1, y2, min_distance):
    return math.hypot(x2 - x1, y2 - y1) > min_distance


def __generate_rooms(width, height, starting_points, ending_point, room_count=1):
    rooms = [starting_points[0]]

    while room_count != 0:
        x = random.randint(10, width - 10)
        y = random.randint(10, height - 10)
        if __isFarAway(x, rooms[-1][0], y, rooms[-1][1], 20) and __isFarAway(ending_point[0], x, ending_point[1], y,
                                                                             20):
            rooms.append((x, y))
            room_count -= 1
    return rooms


def generate_map(width, height, starting_points_count=1, complexity=100):
    # ez mode 4 now
    # TODO CONVERT TO COORDINATE ARRAY FOR PERFORMANCE REASONS
    generated_map = GameMap(width, height)

    ending_point, side = __generate_ending_point((generated_map.width, generated_map.height))
    generated_map.ending_point = ending_point

    generated_map.starting_points = __create_starting_points(
        (generated_map.width, generated_map.height),
        ending_point,
        side,
        100,
        starting_points_count
    )

    rooms = __generate_rooms(width, height, generated_map.starting_points, generated_map.ending_point, room_count=2)

    room_deque = deque(rooms)

    room_deque.append(generated_map.ending_point)

    solver = AStar()
    current_point = room_deque.pop()

    while len(room_deque):
        next_solve_point = room_deque.pop()
        solver.clear()

        solver.init_grid(width, height, (), current_point, next_solve_point)
        solution = solver.solve()
        for i in solution:
            generated_map.generated_map[i[0]][i[1]] = 0
            if i[0] + 1 in range(0, width - 1):
                generated_map.generated_map[i[0] + 1][i[1]] = 0
            if i[0] - 1 in range(0, width - 1):
                generated_map.generated_map[i[0] - 1][i[1]] = 0
            if i[1] + 1 in range(0, height - 1):
                generated_map.generated_map[i[0]][i[1] + 1] = 0
            if i[1] - 1 in range(0, height - 1):
                generated_map.generated_map[i[0]][i[1] - 1] = 0
            if i[0] + 2 in range(0, width - 2):
                generated_map.generated_map[i[0] + 2][i[1]] = 0
            if i[0] - 2 in range(0, width - 2):
                generated_map.generated_map[i[0] - 2][i[1]] = 0
            if i[1] + 2 in range(0, height - 2):
                generated_map.generated_map[i[0]][i[1] + 2] = 0
            if i[1] - 2 in range(0, height - 2):
                generated_map.generated_map[i[0]][i[1] - 2] = 0
        current_point = next_solve_point

    for current_point in rooms:
        generated_map.generated_map[current_point[0]][current_point[1]] = 0
    for point in generated_map.starting_points:
        generated_map.generated_map[point[0]][point[1]] = 0
    generated_map.generated_map[ending_point[0]][ending_point[1]] = 0

    return generated_map
