from assets.Colors import Colors
import pygame as pg

class Buttons(object):
    musicVolume = 'normal'

    def button(self, surface, text, x, y, width, height, inactive_color, active_color, extra_color, action, size): #button creation function
        cur = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x + width > cur[0] > x and y + height > cur[1] > y:
            pg.draw.rect(surface, active_color, (x, y, width, height))
            pg.draw.rect(surface, inactive_color, (x, y, width-5, height-5))
            pg.draw.rect(surface, extra_color, (x+5, y+5, width-10, height-10))

            if click[0] == 1 and action != None:
                if action == "play":
                    pg.mixer.music.stop()
                    self.done = True
                if action == "load":
                    pass
                if action == "settings":
                    self.SettingsDisplay(surface)
                if action == "quit":
                     pg.quit()
                     quit()
                if action == 'close_settings':
                    pass # self.SettingsDisplay.settings_menu = False
                if action == "full_screen":
                    pg.display.set_mode((0, 0), pg.FULLSCREEN)
                if action == "normal_screen":
                    pg.display.set_mode((1280, 720))
                if action == "change_volume":
                    Buttons.toggleMusicVolume()
                if action =="play_audio":
                    pg.mixer.music.unpause()
                if action =="pause_audio":
                    pg.mixer.music.pause()
                if action =="rewind_audio":
                    pg.mixer.music.rewind()
                if action == "credits":
                    pass
        else:
            pg.draw.rect(surface, extra_color, (x, y, width, height))
            pg.draw.rect(surface, active_color, (x, y, width-5, height-5))
            pg.draw.rect(surface, inactive_color, (x+5, y+5, width-10, height-10))



        Buttons.text_to_button(self, surface, text, self.black, x, y, width, height, size)

    def text_to_button(self, surface, msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):  # text in button function
        textSurf, textRect = Buttons.text_objects(self, msg, color, size)
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

    def toggleMusicVolume():
        if Buttons.musicVolume == 'normal':
            Buttons.decreaseMusicVolume()
        else:
            Buttons.restoreMusicVolume()

    def decreaseMusicVolume():
        pg.mixer.music.set_volume(0.1)
        Buttons.musicVolume = 'decreased'

    def restoreMusicVolume():
        pg.mixer.music.set_volume(1.0)
        Buttons.musicVolume = 'normal'

