# Engine for in-game
from tkinter import W
import pygame as pg
import os, sys 

from _lib.constants import *
from _lib.runtime import Runtime

# This must be called at first.

###########
# Helpers #
###########
def ImgLoad(fname):
    asset_basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "assets")
    return pg.image.load(os.path.join(asset_basedir, fname)).convert_alpha()


###########
# Globals #
###########
Rt = Runtime()

####################
# Assets (preload) #
####################

########
# Main #
########
def game_main(**kwargs):
    global Rt

    pg.init()
        
    width, height = kwargs.get("resolution", [1024, 768])    
    pg.display.set_caption('Test') 

    screen_base = pg.display.set_mode((width, height), 0, 32)
    clock = pg.time.Clock()

    # initial setting
    Rt.set_mode(MODE_MOVE_4K_ALLOWED)
    Rt.set_mode(MODE_SHOW_UPPER_MENU)

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
            if Rt.get_mode(MODE_MOVE_4K_ALLOWED):
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

        screen_base.fill(BLACK) 
        if Rt.get_mode(MODE_SHOW_UPPER_MENU):
            print(Rt.get_ch_loc_int())
            screen_base.blit(test_img, Rt.get_ch_loc_int())

        # move
        if not Rt.get_mode(MODE_MOVE_STUCK):
            Rt.move_ch(move_delta)
        
        pg.display.update()
        clock.tick(FPS)

# for test
if __name__ == "__main__":
    game_main()