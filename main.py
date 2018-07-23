from systems import GameGUI, GameLogic, GameRenderer
import GameEngine
import pygame

pygame.init()
main_window = pygame.display.set_mode(pygame.display.list_modes()[0], pygame.FULLSCREEN)
pygame.display.set_caption("Raiders")
pygame.scrap.init()
pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

Engine = GameEngine.GameEngine(main_window)


while True:
    Engine.update()
