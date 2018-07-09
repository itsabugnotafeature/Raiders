import pygame
from scripts.textures import *


class Map_Engine:

    def add_tile(tile, pos, addTo):
        addTo.blit(tile, (pos[0] * Tiles.size, pos[1] * Tiles.size))

    def load_map(file):
        with open(file, "r") as mapfile:
            map_data = mapfile.read()

        map_data = map_data.split("-")

        map_size = map_data[len(map_data) - 1]
        map_data.remove(map_size)
        map_size = map_size.split(",")
        map_size[0] = int(map_size[0]) * Tiles.size
        map_size[1] = int(map_size[1]) * Tiles.size

        tiles = []

        for tile in range(len(map_data)):
            map_data[tile] = map_data[tile].replace("\n", "")
            tiles.append(map_data[tile].split(":"))
        for tile in tiles:
            tile[0] = tile[0].split(",")
            pos = tile[0]
            for p in pos:
                pos[pos.index(p)] = int(p)

            tiles[tiles.index(tile)] = [pos, tile[1]]

        terrain = pygame.Surface((80 * 8, 80 * 8), pygame.HWSURFACE)

        for tile in tiles:
            if tile[1] in Tiles.Texture_tags:
                Map_Engine.add_tile(Tiles.Texture_tags[tile[1]], tile[0], terrain)

        return terrain
