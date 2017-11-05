import os

from states.GameState import GameState
import pygame as pg


class SplashScreenState(GameState):
    def __init__(self):
        super(SplashScreenState, self).__init__()
        self.next_state = "MainMenu"
        self.time = 0
        self.image = pg.image.load(os.path.join('assets', 'splash.png'))
        self.image_rect = self.image.get_rect(center=self.screen_rect.center)

    def update(self, dt):
        # Waits a bit, simple demo of waiting timeouts
        self.time += dt
        if self.time > 5000:
            self.done = True

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

    def draw(self, surface):
        # EZ MODE FOR NOW
        surface.fill(pg.Color("white"))
        surface.blit(self.image, self.image_rect)
