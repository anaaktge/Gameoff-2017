from states.GameState import GameState
from assets.Colors import Colors
from entities.Button import Buttons
import pygame as pg


class NewGameState(GameState):

    tinyfont = pg.font.SysFont('Impact', 15)#tiny font sizes
    smallfont =  pg.font.SysFont('Impact', 25) #small font sizes
    medfont = pg.font.SysFont('Impact', 50) # med font sizes
    largefont =  pg.font.SysFont('Impact', 75) #large font sizes

    def __init__(self):
        super(NewGameState, self).__init__()
        self.next_state = "PlayingState"
        titleFont = pg.font.SysFont('Monaco', 95)
        self.title = titleFont.render("New Master", True, Colors.PrimColor)
        self.title_rect = self.title.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery - 144))
        self.persist["screen_color"] = "black"

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
        self.text_to_screen(surface, Colors.PrimColor, 'Name', self.screen_rect.centerx-60,self.screen_rect.centery - 76, size="medium") # placeholder for name input
        Buttons.button(self,surface, "Submit", self.screen_rect.centerx-150,self.screen_rect.centery + 66,300,60, Colors.PrimColor, Colors.SecColor, Colors.TertColor,action="submit", size="medium")


    def text_to_screen (self, surface,color, text, x, y, size ):
        textSurf, textRect = Buttons.text_objects(self, text, color, size)
        textRect = (x,y)
        surface.blit(textSurf,textRect)
