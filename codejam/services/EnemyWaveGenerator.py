from entities.EnemyAdventurer import EnemyAdventurerGameObject
from services.AStar import AStar


class EnemyWaveGenerator(object):
    def __init__(self):
        pass

    def generate_enemies(self, width, height, start_pos, end_pos):
        enemies = []
        solver = AStar()
        walls = []

        enemy = EnemyAdventurerGameObject()
        enemy.entity.speed = 2
        solver.clear()
        solver.init_grid(width, height, walls, start_pos, end_pos)
        path = solver.solve()
        path.append(end_pos)
        enemy.position = start_pos
        enemy.path = path
        enemies.append(enemy)
        return enemies
