class GameMap(object):
    def __init__(self, w=60, h=100):
        self.width = w
        self.height = h
        # Initialize map to nothing
        self.generated_map = [[1 for x in range(self.height)] for y in range(self.width)]
        # initialize starting points and ending points to nothing, these will be filled in by generator
        self.starting_points = []
        self.ending_point = None


def generate_map(width, height):
    # ez mode 4 now
    # TODO CONVERT TO COORDINATE ARRAY FOR PERFORMANCE REASONS
    generated_map = GameMap(width, height)
    return generated_map
