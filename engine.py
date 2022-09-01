# Engine for in-game

from cmath import rect
import pygame as pg
from pygame.locals import *
import os, sys 

from _lib.commons import *
from _lib.runtime import Runtime
from _lib.graphics import ImgLoad, Graphic


###########
# Globals #
###########
Rt = Runtime()

########
# Main #
########
def game_main(**kwargs):
    global Rt

    pg.init()
        
    clock = pg.time.Clock()

    graphic = Graphic(kwargs.get("resolution", [1280, 768]))
    
    
    rect_test = pg.Rect(GRID(1), GRID(1), GRID(1), GRID(1))
    
    print(graphic.get_center())


    # initial setting (temp)
    Rt.set_mode(MODE_KEY_SYS, MODEBIT_SYS_MOVE_4K_ALLOWED)
    Rt.set_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_LEFT_MENU)
    Rt.set_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_RIGHT_MENU)
    Rt.set_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_GRID)

    # Assets
    test_img = ImgLoad("test/gears.png")

    move_delta = [0, 0] # x, y

    while True: 
        #################
        # Event handler #
        #################
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit() 
                sys.exit()
                # TODO: Add saving data

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

            # FIXME: for test
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    Rt.moveto_ch(graphic.get_center(rect=rect_test))

        #######################
        # Main ingame handler #
        #######################
        # move character
        if not Rt.get_mode(MODE_KEY_SYS, MODEBIT_SYS_MOVE_STUCK):
            Rt.move_ch(move_delta)

        ###########        
        # DISPLAY #
        ###########
        # This must be called first
        graphic.clear_screen()

        if Rt.get_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_LEFT_MENU):
            graphic.draw_rect(rect=[GRID(0), GRID(0), GRID(8), graphic.win_size[1]], 
                                screen_num=4, 
                                color=BLACK_PERCENT(90), 
                                alpha=ALPHA(100))
            for i in range(5):
                graphic.draw_rect(rect=[GRID(1), GRID(22-1.1*i), GRID(6), GRID(1)], 
                                    screen_num=4, 
                                    color=BLACK_PERCENT(95), 
                                    alpha=ALPHA(100))

        if Rt.get_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_RIGHT_MENU):
            graphic.draw_rect(rect=[graphic.win_size[0]-256, 0, 256, graphic.win_size[1]], 
                                screen_num=4, 
                                color=BLACK_PERCENT(90), 
                                alpha=ALPHA(100))


        if Rt.get_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_GRID):
            graphic.draw_grid(1, WHITE, ALPHA(20))

        #print(Rt.get_ch_loc())
        graphic.draw_rect(rect=Rt.get_ch_loc() + [GRID(1), GRID(1)],
                            screen_num=4,
                            color=BLACK,
                            alpha=ALPHA(100))

        graphic.show_screen()
        pg.display.update()
        clock.tick(FPS)

# for test
if __name__ == "__main__":
    game_main()