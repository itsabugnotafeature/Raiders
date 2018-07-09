"""
Provides some helpful math functions for the game systems
"""
from scripts.variables.localvars import *
import pygame
from scripts.Colors import Color


def tup_round(tuple, digits=0):
    return round(tuple[0], digits), round(tuple[1], digits)


def get_facing_vector(pos1, pos2, original_facing):
    # Gets the difference between the two positions
    vector = (pos2[0] - pos1[0], pos2[1] - pos1[1])

    # Checks for which difference is bigger and thus more greatly affects the looking direction
    # If the two positions are the same then return the original orientation
    if abs(vector[0]) >= abs(vector[1]):
        if vector[0] > 0:
            return EAST
        elif vector[0] < 0:
            return WEST
    else:
        if vector[1] > 0:
            return SOUTH
        elif vector[1] < 0:
            return NORTH
    return original_facing


def is_in_bounds(test_pos, area_rect):
    if area_rect[0] < test_pos[0] < area_rect[0] + area_rect[2] and \
            area_rect[1] < test_pos[1] < area_rect[1] + area_rect[3]:
        return True
    return False


# Filters out miscellaneous pygame.KEYDOWN events
# returning just one character
def process_text(event):
    input_text = event.unicode
    return_text = ''
    if input_text in acceptable_characters:
        return_text = input_text
    return return_text


acceptable_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.,?!\ '/|@()#$%^&*+-=`~:;"


def four_way_scale(image, dimensions, tile_length=10):
    first_pass_image = pygame.Surface((dimensions[0], image.get_height()))
    final_image = pygame.Surface(dimensions)
    image_width = image.get_width()
    image_height = image.get_height()
    x_middle = int(image_width / 2)
    y_middle = int(image_height/2)
        
    top_left_image = pygame.Surface((x_middle, y_middle))
    top_left_image.blit(image, (0, 0), (0, 0, x_middle, y_middle))

    top_right_image = pygame.Surface((x_middle, y_middle))
    top_right_image.blit(image, (0, 0), (x_middle, 0, x_middle, y_middle))

    bottom_left_image = pygame.Surface((x_middle, y_middle))
    bottom_left_image.blit(image, (0, 0), (0, y_middle, x_middle, y_middle))

    bottom_right_image = pygame.Surface((x_middle, y_middle))
    bottom_right_image.blit(image, (0, 0), (x_middle, y_middle, x_middle, y_middle))

    final_image.blit(top_left_image, (0, 0))
    final_image.blit(top_right_image, (dimensions[0] - x_middle, 0))
    final_image.blit(bottom_left_image, (0, dimensions[1] - y_middle))
    final_image.blit(bottom_right_image, (dimensions[0] - x_middle, dimensions[1] - y_middle))

    for i in range(dimensions[0] - image_width):
        first_pass_image.blit(image, (x_middle + i, 0), (x_middle, 0, 1, image_height))

    for i in range(dimensions[1] - image_height):
        final_image.blit(first_pass_image, (0, y_middle + i), (0, y_middle, image_width, 1))

    return final_image


def get_percentage_color(percentage):
    # if percentage > .45:
    #     return Color.Green
    # elif percentage > .25:
    #     return Color.Orange
    # else:
    #     return Color.Red

    Color1 = (Color.Green[0] * percentage,
              Color.Green[1] * percentage,
              Color.Green[2] * percentage)

    Color2 = (Color.Red[0] * 1-percentage,
              Color.Red[1] * 1-percentage,
              Color.Red[2] * 1-percentage)

    output_color = (Color1[0] + Color2[0],
                    Color1[1] + Color2[1],
                    Color1[2] + Color2[2])
    return output_color
