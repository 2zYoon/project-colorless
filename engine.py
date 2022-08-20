import pygame
import os, sys 

from _lib.constant import *

width = 600
height = 400

pygame.init()

pygame.display.set_caption('Test') 

displaysurf = pygame.display.set_mode((width, height), 0, 32)

clock = pygame.time.Clock()

while True: 
    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit() 
            sys.exit()

    displaysurf.fill(WHITE) 
    
    pygame.display.update()
    clock.tick(FPS)

