import random

from services.AStar import AStar

# Wrapper for x,y,type
class Room(object):
    def __init__(self, x, y, type, row=0):
        self.x = x
        self.y = y
        self.type = type
        self.row = row
        self.connected = []

    def get_pos(self):
        return (self.x, self.y)

# Game map class
# Basically a wrapper around a 2d array
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

    # Getter
    def get_at(self, x, y):
        return self.generated_map[x][y]

    #Setter
    def set_at(self, x, y, settable):
        self.generated_map[x][y] = settable

    #Add room of random width and height at position in row(for later use) of type
    def add_room_centered_at(self, center_x, center_y, room_type=0, row=0):
        room_width = random.randint(3, 6)
        room_height = random.randint(3, 6)
        for i in range(center_x - room_width, center_x + room_width):
            for j in range(center_y - room_height, center_y + room_height):
                self.set_at(i, j, room_type)

        self.rooms.append(Room(center_x, center_y, type, row))

    # A* pathfinding thingamadooger,
    # TODO Replace eventually
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


def generate_game_map(width, height, starting_positions=1):
    #Create a game map of x*y size
    game_map = GameMap(width, height)

    # Get a third of the height, used to gen vertical positions
    third = height // 3
    # Get a sixth of the width, to handle room spawn type
    sixth = width // 6

    #Create a starting room for the enemies
    start_room_pos = random.randint(5, width - 5)
    for i in range(start_room_pos - 2, start_room_pos + 2):
        for j in range(2, 6):
            game_map.set_at(i, j, 3)
    game_map.starting_room = Room(start_room_pos, 4, 3, 0)
    game_map.rooms.append(game_map.starting_room)

    #Calculate top row type and add rooms
    top_row = get_center_x(sixth)
    for start_pos in top_row:
        game_map.add_room_centered_at(random.randint(start_pos - 1, start_pos + 1), random.randint(13, third - 5), 0, 1)

    # Calculate middle row type and add rooms
    middle_row_rooms = get_center_x(sixth)
    for middle_row in middle_row_rooms:
        game_map.add_room_centered_at(random.randint(middle_row - 2, middle_row + 2),
                                      random.randint(third  + 5, (third * 2) - 7), 0, 2)
    # Calculate end row type and add rooms
    end_row = get_center_x(sixth)
    for end_pos in end_row:
        game_map.add_room_centered_at(random.randint(end_pos - 2, end_pos + 2),
                                      random.randint(third * 2 + 4, third * 3 - 10), 0, 3)
    # Calculate end room aka dungeon master position and add it
    end_room_pos = random.randint(5, width - 5)
    for i in range(end_room_pos - 3, end_room_pos + 3):
        for j in range(height - 5, height - 1):
            game_map.set_at(i, j, 2)
    game_map.ending_room = Room(end_room_pos, height - 4, 2, 4)
    game_map.rooms.append(game_map.ending_room)

    #Create all dem good pathways
    game_map.build_pathways()

    return game_map

"""
This decides where the rooms are located in a set pattern. super simple
"""
def get_center_x(sixth):
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