from states.GameState import GameState
import pygame as pg


class MainMenuState(GameState):
    def __init__(self):
        super(MainMenuState, self).__init__()
        self.title = self.font.render("MAIN MENU", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "PlayingState"

    def get_event(self, event):
        # EZ MODE TO MOVE ON
        # TODO GET A MENU FOR REALS
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))

        surface.blit(self.title, self.title_rect)
