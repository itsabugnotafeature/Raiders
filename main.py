import GameEngine
import pygame
from scripts.variables.localvars import *


pygame.mixer.init()

pygame.init()
display_size = (pygame.display.list_modes()[2][0]//2, pygame.display.list_modes()[2][1]//2)
main_window = pygame.display.set_mode(display_size)
pygame.display.set_caption("Raiders")

#pygame.scrap.init()
#pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

Engine = GameEngine.GameEngine(main_window)

if __name__ != '__main__':
    Engine.game_vars[FULL_SCREEN] = False

while True:
    Engine.update()
