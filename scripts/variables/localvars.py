"""
Provides a bunch of local variable names
for referencing the GameEngine class'
game_variable_dict
"""

from scripts.variables.events import *


SPRITE_LIST = 0
GAME_STATE = 1

# GAME_STATE options
TURN_RESET = 1
PATHING = 2
MOVING = 3
ATTACKING = 4
IN_FIGHT = 5

TILE_SIZE = 2
BOARD_SIZE = 3
BOARD_OFFSET = 4
MAP_NAME = 5
FPS = 6
ACTIVE_SPRITE = 8
ACTIVE_TARGET = 9
IS_RUNNING = 10
MOVABLE_LIST = 11
OUTPUT_CONSOLE = 12
INPUT_TEXT = 13
FRIENDLY_FIRE = 14
TYPING = 15

# All input events.py past this
RMOUSE_POS = 33
ADJUSTED_RMOUSE_POS = 41
SKIP_SEQUENCE = 34
QUIT_SEQUENCE = 35
PLAYER_ACTION = 36
PAUSE = 37
MOUSE_CLICKED = 38
SCROLL_UP = 39
SCROLL_DOWN = 40
DEBUG = 42
GRID_OFFSET = 43

"""
Directions for the sprite facing variable
"""
# 0: South(Down), 1: East(Right), 2: North(Up), 3: West(Left)
SOUTH = 0
EAST = 1
NORTH = 2
WEST = 3

"""
States for gui elements
"""
CLICKED = 0
HOVERED = 1
DISABLED = 2
SELECTED = 4
BASE_STATE = 5
