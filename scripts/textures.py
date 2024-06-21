import pygame
import math
from scripts.tools import os_format_dir_name

class Tiles:

    size = 80

    def load_texture(file, size):
        bitmap = pygame.image.load(file)
        surface = pygame.Surface((size, size), pygame.HWSURFACE)
        surface.blit(bitmap, (0,0))
        return surface

    Grass = load_texture(os_format_dir_name("graphics{os_dir}grass2.png"), size)

    Stone = load_texture(os_format_dir_name("graphics{os_dir}stone.png"), size)

    Sand = load_texture(os_format_dir_name("graphics{os_dir}sand.png"), size)

    Lava = load_texture(os_format_dir_name("graphics{os_dir}lava.png"), size)

    Lava_Rock = load_texture(os_format_dir_name("graphics{os_dir}lava_rock.png"), size)
    
    Texture_tags = {"1": Grass, "2": Stone, "3": Sand, "4": Lava, "5": Lava_Rock}

