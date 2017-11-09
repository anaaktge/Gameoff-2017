from states.GameState import GameState
import pygame as pg

class MainMenuState(GameState):
    pg.init()
    red = pg.Color(100, 0, 0)
    red2 = pg.Color(140,0,0)
    red3 = pg.Color(80,0,0)
    black = pg.Color(0,0,0)
    tinyfont =  pg.font.SysFont('Impact', 14)
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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True




    def draw(self, surface):
        surface.fill(pg.Color("black"))

        surface.blit(self.title, self.title_rect)
        self.button(surface, "New Game", self.screen_rect.centerx-150,self.screen_rect.centery - 76,300,60, self.red, self.red2 , self.red3, action="play" , size="medium" )
        self.button(surface, "Load Game", self.screen_rect.centerx-150,self.screen_rect.centery -6,300,60, self.red, self.red2 , self.red3,action="load", size="medium" )
        self.button(surface, "Settings", self.screen_rect.centerx-150,self.screen_rect.centery + 66,300,60, self.red, self.red2, self.red3,action="settings", size="medium")
        self.button(surface, "Quit Game", self.screen_rect.centerx-150,self.screen_rect.centery + 136,300,60, self.red, self.red2, self.red3,action="quit", size="medium")

    def button(self, surface, text, x, y, width, height, inactive_color, active_color, extra_color, action, size): #button creation function
        cur = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            pg.draw.rect(surface, active_color, (x, y, width, height))
            pg.draw.rect(surface, inactive_color, (x, y, width-5, height-5))
            pg.draw.rect(surface, extra_color, (x+5, y+5, width-10, height-10))

            if click[0] == 1 and action != None:
                if action == "play":
                     pass
                if action == "load":
                    pass
                if action == "settings":
                     self.settings(surface)
                if action == "quit":
                     pg.quit()
                     quit()
                if action == "video":
                    pass
                if action =="play_audio":
                    pg.mixer.music.unpause()
                if action =="pause_audio":
                    pg.mixer.music.pause()
                if action =="rewind_audio":
                    pg.mixer.music.rewind()
        else:
            pg.draw.rect(surface, extra_color, (x, y, width, height))
            pg.draw.rect(surface, active_color, (x, y, width-5, height-5))
            pg.draw.rect(surface, inactive_color, (x+5, y+5, width-10, height-10))



        self.text_to_button(surface, text, self.black, x, y, width, height, size)

    def settings(self, surface):

        settings_menu = True
        while settings_menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        settings_menu = False
            pg.draw.rect(surface, self.red2, [self.screen_rect.centerx -300, self.screen_rect.centery -300, 600, 600])
            pg.draw.rect(surface, self.red3, [self.screen_rect.centerx -300, self.screen_rect.centery -300, 590, 590])
            pg.draw.rect(surface, self.red2, [self.screen_rect.centerx -280, self.screen_rect.centery -200, 555, 480])
            pg.draw.rect(surface, self.red, [self.screen_rect.centerx -270, self.screen_rect.centery -190, 535, 460])
            self.button(surface, "Play", self.screen_rect.centerx - 250, self.screen_rect.centery - 180, 55, 35,
                        self.red, self.red2, self.red3,action="play_audio", size="tiny")
            self.button(surface, "Pause", self.screen_rect.centerx - 190, self.screen_rect.centery - 180, 55, 35,
                        self.red, self.red2, self.red3,action="pause_audio", size="tiny")
            self.button(surface, "Rewind", self.screen_rect.centerx - 130, self.screen_rect.centery - 180, 55, 35,
                        self.red, self.red2, self.red3,action="rewind_audio", size="tiny")
            pg.display.update()
            self.clock.tick(15)


    def text_to_button(self,surface, msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"): #text in button function
        textSurf, textRect = self.text_objects(msg, color, size)
        textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
        surface.blit(textSurf, textRect)

    def text_objects(self, text, color, size): #picking the size of font function
        if size == "tiny":
            textSurface = self.tinyfont.render(text, True, color)
        elif size == "small":
            textSurface = self.smallfont.render(text, True, color)
        elif size == "medium":
            textSurface = self.medfont.render(text, True, color)
        elif size == "large":
            textSurface = self.largefont.render(text, True, color)
        else:
            textSurface = self.smallfont.render(text, True, color)

        return textSurface, textSurface.get_rect()