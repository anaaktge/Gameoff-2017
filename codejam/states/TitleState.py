import os, time

from states.GameState import GameState
import pygame as pg


class TitleScreenState(GameState):
    def __init__(self):
        super(TitleScreenState, self).__init__()
        self.next_state = "Splash"
        self.time = 0
        self.image = pg.image.load(os.path.join('assets','splash.png'))
        self.image_rect = self.image.get_rect(center=self.screen_rect.center)
        pg.mixer.music.load(os.path.join('assets', 'TheFatRat---Jackpot.mp3'))  # music laod
        #self.startup()

    def update(self, dt):
        # Waits a bit, simple demo of waiting timeouts
        self.time += dt
        if self.time > 3000 :
            self.done = True

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

    def draw(self, surface):
        # EZ MODE FOR NOW
        surface.fill(pg.Color("white"))
        surface.blit(self.image, self.image_rect)

    def startup(self, persistent):
        pg.mixer.music.play()  # play music
