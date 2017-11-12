from states.GameState import GameState
from entities.Button import Buttons

import pygame as pg

class MainMenuState(GameState):
    pg.init()
    red = pg.Color(100, 0, 0)
    red2 = pg.Color(140,0,0)
    red3 = pg.Color(80,0,0)
    black = pg.Color(0,0,0)
    tinyfont = pg.font.SysFont('Impact', 15)#tiny font sizes
    smallfont =  pg.font.SysFont('Impact', 25) #small font sizes
    medfont = pg.font.SysFont('Impact', 50) # med font sizes
    largefont =  pg.font.SysFont('Impact', 75) #large font sizes

    clock = pg.time.Clock()

    def __init__(self):
        super(MainMenuState, self).__init__()
        titleFont = pg.font.SysFont('Monaco',95)
        self.title = titleFont.render("MAIN MENU", True, self.red)
        self.title_rect = self.title.get_rect(center=(self.screen_rect.centerx,self.screen_rect.centery -144) )
        self.persist["screen_color"] = "black"
        self.next_state = "PlayingState"


    def get_event(self, event):
        # EZ MODE TO MOVE ON
        # TODO GET A MENU FOR REALS
        if event.type == pg.QUIT:
            self.quit = True


    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
        Buttons.button(self, surface, "New Game", self.screen_rect.centerx-150,self.screen_rect.centery - 76,300,60, self.red, self.red2 , self.red3, action="play" , size="medium" )
        Buttons.button(self,surface, "Load Game", self.screen_rect.centerx-150,self.screen_rect.centery -6,300,60, self.red, self.red2 , self.red3,action="load", size="medium" )
        Buttons.button(self,surface, "Settings", self.screen_rect.centerx-150,self.screen_rect.centery + 66,300,60, self.red, self.red2, self.red3,action="settings", size="medium")
        Buttons.button(self,surface, "Quit Game", self.screen_rect.centerx-150,self.screen_rect.centery + 136,300,60, self.red, self.red2, self.red3,action="quit", size="medium")


    def SettingsDisplay(self, surface):

        settings_menu = True
        while settings_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        settings_menu = False
            pg.draw.rect(surface, self.red2, [self.screen_rect.centerx -310, self.screen_rect.centery -310, 610, 610])
            pg.draw.rect(surface, self.red, [self.screen_rect.centerx -300, self.screen_rect.centery -300, 600, 600])
            pg.draw.rect(surface, self.red3, [self.screen_rect.centerx -300, self.screen_rect.centery -300, 590, 590])
            pg.draw.rect(surface, self.red2, [self.screen_rect.centerx -280, self.screen_rect.centery -200, 555, 480])
            pg.draw.rect(surface, self.red, [self.screen_rect.centerx -270, self.screen_rect.centery -190, 545, 470])
            pg.draw.rect(surface, self.red3, [self.screen_rect.centerx -270, self.screen_rect.centery -190, 535, 460])
            self.text_to_screen(surface, self.black, 'Settings', self.screen_rect.centerx -280, self.screen_rect.centery -290, size="large")
            self.text_to_screen(surface, self.black, 'Music:', self.screen_rect.centerx -250, self.screen_rect.centery -180, size="medium")
            self.text_to_screen(surface, self.black, 'Video:', self.screen_rect.centerx -250, self.screen_rect.centery -100, size="medium")
            Buttons.button(self,surface, "Full Screen", self.screen_rect.centerx - 100, self.screen_rect.centery - 80, 85, 35,
                        self.red, self.red2, self.red3, action="full_screen", size="tiny")
            Buttons.button(self,surface, "Restore", self.screen_rect.centerx - 5, self.screen_rect.centery - 80, 85, 35,
                        self.red, self.red2, self.red3, action="normal_screen", size="tiny")
            Buttons.button(self,surface, "Play", self.screen_rect.centerx - 100, self.screen_rect.centery - 160, 55, 35,
                        self.red, self.red2, self.red3,action="play_audio", size="tiny")
            Buttons.button(self,surface, "Pause", self.screen_rect.centerx - 40, self.screen_rect.centery - 160, 55, 35,
                        self.red, self.red2, self.red3,action="pause_audio", size="tiny")
            Buttons.button(self,surface, "Rewind", self.screen_rect.centerx + 20, self.screen_rect.centery - 160, 55, 35,
                        self.red, self.red2, self.red3,action="rewind_audio", size="tiny")
            Buttons.button(self,surface, "Toggle volume", self.screen_rect.centerx + 80, self.screen_rect.centery - 160, 115, 35,
                        self.red, self.red2, self.red3, action="change_volume", size="tiny")
            Buttons.button(self, surface, "X", self.screen_rect.centerx + 200 , self.screen_rect.centery -280,
                           75, 35, self.red, self.red2, self.red3, action="close_settings", size="tiny")
            Buttons.button(self, surface, "Credits", self.screen_rect.centerx - 150, self.screen_rect.centery + 200,
                           300, 60, self.red, self.red2, self.red3, action="Credits", size="medium")

            pg.display.update()
            self.clock.tick(15)


    def text_to_screen (self, surface,color, text, x, y, size ):
        textSurf, textRect = Buttons.text_objects(self, text, color, size)
        textRect = (x,y)
        surface.blit(textSurf,textRect)
