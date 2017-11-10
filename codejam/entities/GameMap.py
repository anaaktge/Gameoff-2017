import random

from services.AStar import AStar


class Room(object):
    def __init__(self,x,y, type, row=0):
        self.x = x
        self.y = y
        self.type = type
        self.row = row
        self.connected = []

    def get_pos(self):
        return (self.x, self.y)

class GameMap(object):
    def __init__(self, w=36, h=66):
        self.width = w
        self.height = h
        # Initialize map to nothing
        self.generated_map = [[1 for x in range(self.height)] for y in range(self.width)]
        # initialize starting points and ending points to nothing, these will be filled in by generator
        self.starting_room = None
        self.ending_room = None
        self.rooms = []

    def get_at(self, x, y):
        return self.generated_map[x][y]

    def set_at(self, x, y, settable):
        self.generated_map[x][y] = settable

    def add_room_centered_at(self, center_x, center_y, room_type=0, row=0 , max_room_width = 3, max_room_height = 5):
        for i in range(center_x-max_room_width, center_x+max_room_width):
            for j in range(center_y-max_room_height, center_y+max_room_height):
                self.set_at(i, j, room_type)

        self.rooms.append(Room(center_x, center_y, type, row))

    def build_pathways(self):
        current_room = self.rooms.pop(0)
        solver = AStar()
        while len(self.rooms):
            next_room = self.rooms.pop(0)
            solver.clear()
            solver.init_grid(self.width, self.height, (), current_room.get_pos(), next_room.get_pos())
            solution = solver.solve()
            for i in solution:
                self.set_at(i[0], i[1], 0)
            current_room = next_room

    def add_path_between(self, room_1, room_2):
        pass


def generate_game_map(width, height, starting_positions=1):
    game_map = GameMap(width, height)

    third = height//3
    sixth = width//6
    end_room_pos = random.randint(5, width - 5)
    for i in range(end_room_pos - 2, end_room_pos + 2):
        for j in range(2, 6):
            game_map.set_at(i, j, 3)
    game_map.starting_room = Room(end_room_pos, 4, 3, 0)
    game_map.rooms.append(game_map.starting_room)

    start_poss = get_room_x_positions(sixth)

    for start_pos in start_poss:
        game_map.add_room_centered_at(random.randint(start_pos-1, start_pos+1), random.randint(13, third-5), 0, 1)

    middle_poss = get_room_x_positions(sixth)

    for middle_pos in middle_poss:
        game_map.add_room_centered_at(random.randint(middle_pos-2, middle_pos+2), random.randint((third*2)-7, (third*3)-7), 0, 2)

    end_poss = get_room_x_positions(sixth)
        
    for end_pos in end_poss:
        game_map.add_room_centered_at(random.randint(end_pos - 2, end_pos + 2), random.randint(third*2 + 4, third*3-10), 0, 3)

    end_room_pos = random.randint(5, width-5)
    for i in range(end_room_pos-3, end_room_pos+3):
        for j in range(height-6, height-2):
            game_map.set_at(i,j,2)
    game_map.ending_room = Room(end_room_pos, height-4, 2, 4)
    game_map.rooms.append(game_map.ending_room)
    game_map.build_pathways()

    return game_map


def get_room_x_positions(sixth):
    position_type = random.randint(0, 4)
    poss = []
    if position_type == 0:
        poss = [sixth, 5 * sixth]
    elif position_type == 1:
        poss = [sixth, 3 * sixth]
    elif position_type == 2:
        poss = [3 * sixth, 5 * sixth]
    elif position_type == 3:
        poss = [2 * sixth, 4 * sixth]
    elif position_type == 4:
        poss = [sixth, 3 * sixth, 5 * sixth]
    return poss
