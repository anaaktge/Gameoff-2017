from states.GameState import GameState
import pygame as pg


class DragAndDrop(GameState):
    def __init__(self):
        self.rectangle_draging = False
        super(DragAndDrop, self).__init__()
        self.title = self.font.render("Splash Screen", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.offset_x = 0
        self.offset_y = 0

    def get_event(self, event):

        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.title_rect.collidepoint(event.pos):
                    self.rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.title_rect.x - mouse_x
                    self.offset_y = self.title_rect.y - mouse_y
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.rectangle_draging = False

        elif event.type == pg.MOUSEMOTION:
            if self.rectangle_draging:
                mouse_x, mouse_y = event.pos
                print(event.pos)
                self.title_rect.x = mouse_x + self.offset_x
                self.title_rect.y = mouse_y + self.offset_y
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
