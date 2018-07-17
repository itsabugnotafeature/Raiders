import pygame

"""
Provides a bunch of name references for the custom
pygame events used in this game
Available Name Space = 25 - 31
"""

SURFACE = 25    # Event dict: surf=pygame.Surface, pos=(x, y), z=int
"""Allows the systems to send surfaces to the Renderer to be displayed"""

PRINT_LINE = 26     # Event dict: message="", color=(R, G, B)/(R, G, B, A)
"""Passes messages to the main output console for display"""

FIGHT_EVENT = 27    # Event dict: subtype=(any of the sub types listed), kwargs(as listed below)
"""A collection of events related to controlling and monitoring the current fight going on"""

MESSAGE_BANNER = 28     # Event dict: message="", color=(R, G, B)/(R, G, B, A)
"""Similar to PRINT_LINE, only this is displayed directly on the screen, not in the textbox"""

FLSCRN_TOGGLE = 29      # Event dict:
"""Signals GameEngine to switch between fullscreen and windowed mode"""

# FIGHT SUB EVENTS #
FIGHT_BEGIN = 0     # Signals beginning of fight, creation of buttons // kwargs(player=Player, monster=Monster)
FIGHT_END = 1       # Signals end of fight, destruction of buttons
ACTION = 2          # Signals that an action was used, two per fight turn, logging of fight events // kwargs(num=int)
RESET = 3           # Used for control, lets you rewind turns // kwargs(rewind_amount=int)


def make_event(type, **kwargs):
    pygame.event.post(pygame.event.Event(type, **kwargs))
