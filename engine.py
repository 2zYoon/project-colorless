# Engine for in-game

import pygame as pg
from pygame.locals import *
import os, sys 

from _lib.constants import *
from _lib.runtime import Runtime


###########
# Globals #
###########
Rt = Runtime()

####################
# Graphics Helpers #
####################
def ImgLoad(fname):
    asset_basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "assets")
    return pg.image.load(os.path.join(asset_basedir, fname)).convert_alpha()


class Graphic:
    def __init__(self, win_size):
        self.win_size = win_size
        self.main_screen = pg.display.set_mode(self.win_size,
            # FULLSCREEN |
            # HWSURFACE | 
              DOUBLEBUF)

        self.basic_asset = dict()
        self.basic_asset["background"] = pg.transform.scale(ImgLoad("basic_ui/bg.jpg"), win_size)
        
        #########
        # LAYER #
        #########
        #
        # Layer 1: Background
        # Layer 2: 
        # Layer 5: Basic UIs

        self.layers = [
            pg.Surface(win_size).convert_alpha(), 
            pg.Surface(win_size).convert_alpha(),
            pg.Surface(win_size).convert_alpha(), 
            pg.Surface(win_size).convert_alpha(), 
            pg.Surface(win_size).convert_alpha(),         
        ]
    
        pg.display.set_caption('Test') 

    def clear_screen(self):        
        for l in self.layers:
            l.fill(TRANSPARENT)

        self.layers[0].blit(self.basic_asset["background"], [0, 0])

    def show_screen(self, exclude=[]):
        for i in range(len(self.layers)):
            if i not in exclude:
                self.main_screen.blit(self.layers[i], [0, 0])


    def get_basic_asset(self, key, size=None):
        if size == None:
            return self.basic_asset[key]
        else:
            return pg.transform.scale(self.basic_asset[key], size)

    def draw_rect(self, rect, screen_num=0, color=BLACK, alpha=255, border_width=0, border_color=BLACK, text=None, fontsize=None, fontcolor=None):
        if str(type(rect)) == "<class \'pygame.Rect\'>":
            pg.draw.rect(self.layers[screen_num], list(color) + [alpha], rect, border_width)

        elif len(rect) == 4:
            pg.draw.rect(self.layers[screen_num], list(color) + [alpha], rect, border_width)
        
        else:
            assert(0)

    def draw_grid(self, screen_num=-1, color=WHITE, alpha=255):
        for x in range(32, self.win_size[0], 32):
            pg.draw.line(self.layers[screen_num], list(color)+[alpha], [x, 0], [x, self.win_size[1]])
        for y in range(32, self.win_size[1], 32):
            pg.draw.line(self.layers[screen_num], list(color)+[alpha], [0, y], [self.win_size[0], y])
    


########
# Main #
########
def game_main(**kwargs):
    global Rt

    pg.init()
        
    width, height = kwargs.get("resolution", [1280, 768])    


    clock = pg.time.Clock()

    graphic = Graphic([width, height])

    a = pg.Rect([30, 30, 30, 30])
    


    # initial setting (temp)
    Rt.set_mode(MODE_KEY_SYS, MODEBIT_SYS_MOVE_4K_ALLOWED)
    Rt.set_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_LEFT_MENU)
    Rt.set_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_RIGHT_MENU)
    Rt.set_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_GRID)

    # Assets
    test_img = ImgLoad("test/gears.png")

    move_delta = [0, 0] # x, y
    while True: 
        # event handler
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit() 
                sys.exit()

            # Handles arrow keys to try to move            
            if Rt.get_mode(MODE_KEY_SYS, MODEBIT_SYS_MOVE_4K_ALLOWED):
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        move_delta[0] -= 1
                    if event.key == pg.K_RIGHT:
                        move_delta[0] += 1
                    if event.key == pg.K_UP:
                        move_delta[1] -= 1
                    if event.key == pg.K_DOWN:
                        move_delta[1] += 1
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT:
                        move_delta[0] += 1
                    if event.key == pg.K_RIGHT:
                        move_delta[0] -= 1
                    if event.key == pg.K_UP:
                        move_delta[1] += 1
                    if event.key == pg.K_DOWN:
                        move_delta[1] -= 1

        # move
        if not Rt.get_mode(MODE_KEY_SYS, MODEBIT_SYS_MOVE_STUCK):
            Rt.move_ch(move_delta)

        ###########        
        # DISPLAY #
        ###########
        # This must be called first
        graphic.clear_screen()

        if Rt.get_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_LEFT_MENU):
            graphic.draw_rect(rect=[0, 0, 256, graphic.win_size[1]], 
                                screen_num=4, 
                                color=BLACK, 
                                alpha=225)

        if Rt.get_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_RIGHT_MENU):
            graphic.draw_rect(rect=[graphic.win_size[0]-256, 0, 256, graphic.win_size[1]], 
                                screen_num=4, 
                                color=BLACK, 
                                alpha=225)


        if Rt.get_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_GRID):
            graphic.draw_grid(1, WHITE, 55)

        graphic.show_screen()
        pg.display.update()
        clock.tick(FPS)

# for test
if __name__ == "__main__":
    game_main()