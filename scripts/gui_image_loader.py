import pygame
import ast
from scripts.tools import os_format_dir_name

class GUIComponents:

    def __init__(self, corner_image, side_image, background_image):
        self.corner_image = corner_image
        self.corner_width = self.corner_image.get_width()
        self.corner_height = self.corner_image.get_height()

        self.side_image = side_image
        self.side_width = self.side_image.get_width()
        self.side_height = self.side_image.get_height()

        self.background_image = background_image
        self.background_width = self.background_image.get_width()
        self.background_height = self.background_image.get_height()

    def render(self, dimensions):
        for value in dimensions:
            if value < 0:
                raise ValueError("Dimensions need to positive integers")
        base_image = pygame.Surface((dimensions[0], dimensions[1]))

        for i in range(int(dimensions[0]/self.background_width) + 1):
            for j in range(int(dimensions[1]/self.background_height) + 1):
                base_image.blit(self.background_image, (i*self.background_width, j*self.background_height))

        side_rotated_90 = pygame.transform.rotate(self.side_image, 90)
        side_rotated_180 = pygame.transform.rotate(self.side_image, 180)
        side_rotated_270 = pygame.transform.rotate(self.side_image, 270)

        for i in range(int(dimensions[0]/self.side_width) + 1):
            base_image.blit(self.side_image, (i*self.side_width, 0))
            base_image.blit(side_rotated_180, (i*self.side_width, (dimensions[1] - self.side_height)))

        for i in range(int(dimensions[1]/self.side_height) + 1):
            base_image.blit(side_rotated_90, (0, i*self.side_width))
            base_image.blit(side_rotated_270, (dimensions[0] - self.side_height, i*self.side_width))

        corner_rotated_90 = pygame.transform.rotate(self.corner_image, 90)
        corner_rotated_180 = pygame.transform.rotate(self.corner_image, 180)
        corner_rotated_270 = pygame.transform.rotate(self.corner_image, 270)

        base_image.blit(self.corner_image, (0, 0))
        base_image.blit(corner_rotated_90, (0, dimensions[1] - self.corner_width))
        base_image.blit(corner_rotated_180, (dimensions[0] - self.corner_width, dimensions[1] - self.corner_height))
        base_image.blit(corner_rotated_270, (dimensions[0] - self.corner_height, 0))

        # Colorkey cannot change, it removes the white bars from the corner image
        base_image.set_colorkey(base_image.get_at((0, 0)))
        return base_image


def load_gui_from_image(file_name):

    corner_dimensions = (0, 0, 1, 1)
    side_dimensions = (0, 0, 1, 1)
    background_dimensions = (0, 0, 1, 1)

    try:
        component_image = pygame.image.load(os_format_dir_name("graphics{os_dir}gui_images{os_dir}") + file_name + ".png")

        with open("graphics//gui_images//" + file_name + "_dimensions.txt") as dimensions_file:
            current_line = dimensions_file.readline()
            while current_line != "":
                split_line = current_line.split(" ")
                if split_line[0] == "corner:":
                    corner_dimensions = ast.literal_eval(split_line[1])
                elif split_line[0] == "side:":
                    side_dimensions = ast.literal_eval(split_line[1])
                elif split_line[0] == "background:":
                    background_dimensions = ast.literal_eval(split_line[1])
                else:
                    raise ValueError("Unknown identifier: " + split_line[0])
                current_line = dimensions_file.readline()
    except FileNotFoundError:
        print("Problem loading gui.")
        component_image = pygame.Surface((100, 100))

    for value in corner_dimensions:
        if value < 0:
            raise ValueError("Gui dimensions need to be positive.")
    for value in side_dimensions:
        if value < 0:
            raise ValueError("Gui dimensions need to be positive.")
    for value in background_dimensions:
        if value < 0:
            raise ValueError("Gui dimensions need to be positive.")

    corner_image = pygame.Surface((corner_dimensions[2], corner_dimensions[3]))
    side_image = pygame.Surface((side_dimensions[2], side_dimensions[3]))
    background_image = pygame.Surface((background_dimensions[2], background_dimensions[3]))

    corner_image.blit(component_image, (0, 0), (corner_dimensions[0], corner_dimensions[1], corner_dimensions[2],
                                                corner_dimensions[3]))
    side_image.blit(component_image, (0, 0), (side_dimensions[0], side_dimensions[1], side_dimensions[2],
                                              side_dimensions[3]))
    background_image.blit(component_image, (0, 0), (background_dimensions[0], background_dimensions[1],
                                                    background_dimensions[2], background_dimensions[3]))
    return GUIComponents(corner_image, side_image, background_image)
