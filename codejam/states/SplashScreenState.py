from states.GameState import GameState
import pygame as pg


class SplashScreenState(GameState):
    def __init__(self):
        super(SplashScreenState, self).__init__()
        self.title = self.font.render("Splash Screen", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "MainMenu"
        self.time = 0

    def update(self, dt):
        # Waits a bit, simple demo of waiting timeouts
        self.time += dt
        if self.time > 1000:
            self.done = True

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True

    def draw(self, surface):
        # EZ MODE FOR NOW
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
