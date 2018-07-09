import pygame
import math


class Tiles:

    size = 80

    def load_texture(file, size):
        bitmap = pygame.image.load(file)
        surface = pygame.Surface((size, size), pygame.HWSURFACE)
        surface.blit(bitmap, (0,0))
        return surface

    Grass = load_texture("graphics\\grass2.png", size)

    Stone = load_texture("graphics\\stone.png", size)

    Sand = load_texture("graphics\\sand.png", size)

    Lava = load_texture("graphics\\lava.png", size)

    Lava_Rock = load_texture("graphics\\lava_rock.png", size)
    
    Texture_tags = {"1": Grass, "2": Stone, "3": Sand, "4": Lava, "5": Lava_Rock}

