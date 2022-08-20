# Engine for in-game
import pygame as pg
import os, sys 

from _lib.constants import *
from _lib.runtime import Runtime

###########
# Globals #
###########
Rt = Runtime()

def game_main(**kwargs):
    width = 600
    height = 400

    pg.init()

    pg.display.set_caption('Test') 

    displaysurf = pg.display.set_mode((width, height), 0, 32)

    clock = pg.time.Clock()

    while True: 
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit() 
                sys.exit()

        displaysurf.fill(WHITE) 
        
        pg.display.update()
        clock.tick(FPS)

