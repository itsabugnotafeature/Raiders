from systems import GameGUI, GameLogic, GameRenderer
import GameEngine
import pygame

pygame.init()
Engine = GameEngine.GameEngine(GameLogic.Logic(), GameGUI.GUI(), GameRenderer.Renderer())
pygame.scrap.init()
pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

while True:
    Engine.update()
