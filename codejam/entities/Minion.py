from pygame.rect import Rect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Minion(Base):
    __tablename__ = 'minions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cost = Column(Integer)
    #width x height it takes up
    size = (1,1)
    position = (0,0)
    image = Column(String)

class MinionGameObject(object):
    def __init__(self):
        self.entity = Minion()
        self.sprite =  pg.image.load(os.path.join('assets', 'goblin.png'))

    def handle_event(self, event):
        pass

    def draw(self, surface):
        rect = Rect(self.entity.position[0] * 20, self.entity.position[1] * 20, 20, 20)
        drawable = pg.transform.scale(self.sprite, (20, 20))
        surface.blit(drawable, rect)
        pass

    def take_damage(self, damage):
        pass

    def update(self, dt):
        pass
