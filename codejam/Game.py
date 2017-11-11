import sys
import pygame as pg
from pygame.locals import *
from states.MainMenuState import MainMenuState
from states.TitleState import TitleScreenState
from states.PlayingState import PlayingState
from states.SplashScreenState import SplashScreenState


class Game(object):
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.state.startup(self.state.persist)

    def event_loop(self):
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    pg.init()

    flags = DOUBLEBUF
    screen = pg.display.set_mode((1280, 800), flags)
    states = {
        "Title": TitleScreenState(),
        "Splash": SplashScreenState(),
        "MainMenu": MainMenuState(),
        "PlayingState": PlayingState()
    }
    game = Game(screen, states, "PlayingState")
    game.run()
    pg.quit()
    sys.exit()
