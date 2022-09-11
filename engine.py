# Engine for in-game

from cmath import rect
from re import M
import pygame as pg
from pygame.locals import *
import os, sys 

from _lib.commons import *
from _lib.runtime import *
from _lib.graphics import *
from _lib.map import *

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

    # MAIN LOOP
    while True: 
        map_current = m_test

        #################
        # Event handler #
        #################
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit() 
                sys.exit()
                # TODO: Add saving data

            # FIXME: for test
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
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

            # FIXME: for test
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    Rt.moveto_ch(graphic.get_center(rect=rect_test))

        #######################
        # Main ingame handler #
        #######################
        # move character
        if (not Rt.get_mode(MODE_KEY_SYS, MODEBIT_SYS_MOVE_STUCK)) and not (move_delta[0] == move_delta[1] == 0):
            Rt.move_ch(move_delta, bound=map_current.get_size())
            # for test
            #print(Rt.get_ch_loc_int())

        ###########        
        # DISPLAY #
        ###########
        # This must be called first
        graphic.clear_screen()

        ########
        # TEST #
        ########

        # LEFT SIDE MENU
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

        # RIGHT SIDE MENU
        if Rt.get_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_RIGHT_MENU):
            graphic.draw_rect(rect=[graphic.win_size[0]-256, 0, 256, graphic.win_size[1]], 
                                screen_num=4, 
                                color=BLACK_PERCENT(90), 
                                alpha=ALPHA(100))


        # GRID
        if Rt.get_mode(MODE_KEY_GP, MODEBIT_GP_SHOW_GRID):
            graphic.draw_grid(1, WHITE, ALPHA(20))


        # Calculate map drawing start/end point
        # Example:
        #     ===== ===== WINDOW ===== =====
        # 10:    -----@-----[]-----@-----
        # 5 :          -----[]-----@-----@-----    
        # 0 :               []-----@-----@-----@-----
        
        start_x_on_window = graphic.get_center()[0] - Rt.get_ch_loc()[0]
        start_y_on_window = graphic.get_center()[1] - Rt.get_ch_loc()[1]

        #start_x_on_map = max(0, map_current.get_size()[0] // 2 - Rt.get_ch_loc()[0])
        #start_y_on_map = max(0, map_current.get_size()[1] // 2 - Rt.get_ch_loc()[1])


        for y in range(map_current.get_size_grid()[1]):
            for x in range(map_current.get_size_grid()[0]):
                # TODO: skip rendering if the rect is not visible (out of window)

                screen_num, render_type, value = map_current.render_tile(x, y)
            
                if render_type == RENDER_TYPE_COLOR:
                    color_to_render = ((value >> 24) & 0xff, 
                                        (value >> 16) & 0xff,
                                        (value >> 8) & 0xff
                    )
                    alpha_to_render = value & 0xff

                    graphic.draw_rect(
                        rect=[start_x_on_window + GRID(x), start_y_on_window + GRID(y)] + [GRID(1), GRID(1)],
                        screen_num=screen_num,
                        color=color_to_render,
                        alpha=alpha_to_render
                    )
                
                if render_type == RENDER_TYPE_IMAGE:
                    pass # TODO

        # Character
        graphic.draw_rect(rect=graphic.get_center(rect=[GRID(1), GRID(1)]) + [GRID(1), GRID(1)],
                            screen_num=4,
                            color=BLACK,
                            alpha=ALPHA(100))
    
        graphic.show_screen()
        pg.display.update()
        clock.tick(FPS)

# for test
if __name__ == "__main__":
    game_main()