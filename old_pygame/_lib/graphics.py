import pygame as pg
from pygame.locals import *

import os

from pyparsing import alphanums

from _lib.commons import *

# All of them must be used after pg.init() 


ASSET_BASEDIR = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "assets")

FONTSIZES = {
    "tiny": 8,
    "small": 16,
    "medium": 24,
    "large": 32,
}

def FontLoad(fname):
    fonts = dict()
    for key, size in FONTSIZES.items():
        fonts[key] = pg.font.Font(os.path.join(os.path.join(ASSET_BASEDIR, "fonts"), fname), size)
    
    return fonts


def ImgLoad(fname, size=None):
    img = pg.image.load(os.path.join(ASSET_BASEDIR, fname)).convert_alpha()
    if size:
        img =  pg.transform.scale(img, size)

    return img


class Graphic:
    def __init__(self, win_size):
        self.win_size = win_size
        self.main_screen = pg.display.set_mode(self.win_size,
            # FULLSCREEN |
            # HWSURFACE | 
              DOUBLEBUF)

        #####################
        # LOAD BASIC ASSETS #
        #####################
        self.basic_asset = dict()
        self.basic_asset["background"] = dict()
        self.basic_asset["background"]["default"] = ImgLoad("backgrounds/default.jpg", win_size)

#        self.basic_asset["background"] = ImgLoad("basic_ui/bg.jpg", win_size)
        
        self.basic_asset["fonts"] = dict()
        self.basic_asset["fonts"]["arial"] = FontLoad("arial.ttf")
        self.basic_asset["fonts"]["consolas"] = FontLoad("consolas.ttf")

        ##############
        # LAYER INIT #
        ##############
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
            pg.Surface(win_size).convert_alpha(),    
            pg.Surface(win_size).convert_alpha(),    
            pg.Surface(win_size).convert_alpha(),    
            pg.Surface(win_size).convert_alpha(),         
        ]
    
        pg.display.set_caption('Test') 


    def clear_screen(self):        
        for l in self.layers:
            l.fill(TRANSPARENT)

        self.layers[0].blit(self.basic_asset["background"]["default"], [0, 0])

    def show_screen(self, exclude=[]):
        for i in range(len(self.layers)):
            if i not in exclude:
                self.main_screen.blit(self.layers[i], [0, 0])

    def get_basic_asset(self, key, size=None):
        if size == None:
            return self.basic_asset[key]
        else:
            return pg.transform.scale(self.basic_asset[key], size)

    def get_win_size(self):
        return self.win_size

    # @rect: if rect is given, returns rect-aware center position
    def get_center(self, rect=None):
        if rect == None:
            return [self.win_size[0] // 2, self.win_size[1] // 2]
        else:
            # x, y, w, h
            if len(rect) == 4:
                return [(self.win_size[0] - list(rect)[2]) // 2, (self.win_size[1] - list(rect)[3]) // 2]
            # w, h
            elif len(rect) == 2:
                return [(self.win_size[0] - list(rect)[0]) // 2, (self.win_size[1] - list(rect)[1]) // 2]
            else:
                assert("get_center: invalid rect")


    def draw_rect(self, rect, screen_num=0, color=BLACK, alpha=ALPHA(100), border_width=0):
        pg.draw.rect(self.layers[screen_num], list(color) + [alpha], list(rect), border_width)
        

        return

        if str(type(rect)) == "<class \'pygame.Rect\'>":
            pg.draw.rect(self.layers[screen_num], list(color) + [alpha], rect, border_width)

        elif len(rect) == 4:
            pg.draw.rect(self.layers[screen_num], list(color) + [alpha], rect, border_width)
        
        else:
            assert(0)

    def draw_text(self, rect, text, screen_num=0, color=BLACK, alpha=ALPHA(100), font="consolas", fontsize="large"):
        txt = self.basic_asset["fonts"][font][fontsize].render(text, True, list(color) + [alpha])

        self.layers[screen_num].blit(txt, rect)

    def draw_grid(self, screen_num=-1, color=WHITE, alpha=ALPHA(100)):
        for x in range(32, self.win_size[0], 32):
            pg.draw.line(self.layers[screen_num], list(color)+[alpha], [x, 0], [x, self.win_size[1]])
        for y in range(32, self.win_size[1], 32):
            pg.draw.line(self.layers[screen_num], list(color)+[alpha], [0, y], [self.win_size[0], y])
