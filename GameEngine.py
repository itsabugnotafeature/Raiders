import math

from systems import GameAnimator, GameGUI, GameLogic, GameRenderer, GameSound
import scripts.sprite_class

from scripts.variables.localvars import *
from scripts.variables.events import *
import ast


class GameEngine:

    def __init__(self, window, logic_system=GameLogic.Logic(), gui_system=GameGUI.GUI(),
                 renderer_system=GameRenderer.Renderer(), **kwargs):

        # Engine variables (Don't touch)
        self.font = pygame.font.SysFont("lucidaconsole", 18, True)
        self.Clock = pygame.time.Clock()

        # Default values for variables
        self.window_width, self.window_height = window.get_width(), window.get_height()
        self.display_window = window

        # Container for all variables the systems create.
        # Keys are defined in localvars, they are all ints.
        # The spritelist where all sprites are stored.
        self.game_vars = {SPRITE_LIST: [
            scripts.sprite_class.Player("Thrall", "tank", "tank.png", (0, 0)),
            scripts.sprite_class.Player("Garrosh", "tank", "warrior.png", (1, 0)),
            scripts.sprite_class.Monster("Infernus", "tank", "warrior.png", (1, 1))
        ], PAUSE: False, QUIT_SEQUENCE: False, GAME_STATE: TURN_RESET, SCROLL_DOWN: False, SCROLL_UP: False,
            MOUSE_CLICKED: False, SKIP_SEQUENCE: False, FRIENDLY_FIRE: False, TYPING: False, DEBUG: True,
            GRID_OFFSET: (0, -30), FULL_SCREEN: True
        }

        # Using the keyword arguments
        for key, value in kwargs:
            if key == "wind_dim":
                self.display_window = pygame.display.set_mode(value,
                                                              pygame.FULLSCREEN | pygame.RESIZABLE)
            elif key == "win_title":
                pygame.display.set_caption(value)
            elif key == "sprite_list":
                self.game_vars[SPRITE_LIST] = value

        # System pointers
        self.Logic = logic_system
        self.GUI = gui_system
        self.Animator = GameAnimator.Animator()
        self.GameSound = GameSound.GameSound()
        self.Renderer = renderer_system

        self.systems_list = [self.Logic, self.GUI, self.Animator, self.GameSound, self.Renderer]

        for system in self.systems_list:
            system.init(self)

        self.init()

    def init(self):
        self.game_vars[OUTPUT_CONSOLE].print_line("Welcome to Raiders!", reward_message=True)

    def main_loop(self):
        self.Clock.tick()
        self.game_vars[FPS] = self.Clock.get_fps()

        self.handle_events()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_vars[QUIT_SEQUENCE] = True

            # TODO: add support for a windowed mode
            # if event.type == pygame.VIDEORESIZE:
            #     self.display_window = pygame.display.set_mode((event.w, event.h),
            #                                                   pygame.DOUBLEBUF | pygame.RESIZABLE)
            #     self.window_height = event.h
            #     self.window_width = event.w
            #     self.GUI.handle_event(event)
            #
            #     self.GUI.handle_event(event)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.game_vars[MOUSE_CLICKED] = True
                elif event.button == 3 and not self.game_vars[TYPING] and not self.game_vars[PAUSE] and not self.game_vars[GAME_STATE] == IN_FIGHT:
                    self.game_vars[SKIP_SEQUENCE] = True
                elif event.button == 4:
                    self.game_vars[SCROLL_UP] = True
                elif event.button == 5:
                    self.game_vars[SCROLL_DOWN] = True
                self.GUI.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.GUI.handle_event(event)

            if event.type == pygame.MOUSEMOTION:
                # Rounds the mouse position to tiles of dimensions TILE_SIZE x TILE_SIZE, i.e. (320, 160)
                mouse_pos = event.pos
                mouse_x = (mouse_pos[0]-self.game_vars[GRID_OFFSET][0]) // self.game_vars[TILE_SIZE]
                mouse_y = (mouse_pos[1]-self.game_vars[GRID_OFFSET][1]) // self.game_vars[TILE_SIZE]
                self.game_vars[RMOUSE_POS] = (mouse_x * self.game_vars[TILE_SIZE], mouse_y * self.game_vars[TILE_SIZE])

                # Adjusted to the actual board position so (0, 0) is at the top left
                # and the steps are in 1's not 80's
                # Primarily used for checking sprite positions
                self.game_vars[ADJUSTED_RMOUSE_POS] = ((self.game_vars[RMOUSE_POS][0] - self.game_vars[BOARD_OFFSET][0])
                                                       // self.game_vars[TILE_SIZE],
                                                       (self.game_vars[RMOUSE_POS][1] - self.game_vars[BOARD_OFFSET][1]+60)
                                                       // self.game_vars[TILE_SIZE])
                self.GUI.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_vars[TYPING] and not self.game_vars[PAUSE] and not self.game_vars[GAME_STATE] == IN_FIGHT:
                    self.game_vars[SKIP_SEQUENCE] = True
                if event.key == pygame.K_q and event.mod & pygame.KMOD_CTRL:
                    self.game_vars[QUIT_SEQUENCE] = True
                if event.key == pygame.K_d and event.mod & pygame.KMOD_CTRL:
                    self.game_vars[DEBUG] = not self.game_vars[DEBUG]
                if event.key == pygame.K_ESCAPE:
                    self.game_vars[PAUSE] = not self.game_vars[PAUSE]
                    self.GUI.handle_event(event)
                    self.Renderer.handle_event(event)
                else:
                    self.GUI.handle_event(event)

            if event.type == pygame.KEYUP:
                self.GUI.handle_event(event)

            # My custom pygame events
            if event.type == SURFACE:
                self.Renderer.handle_event(event)

            if event.type == FIGHT_EVENT:
                if event.subtype == FIGHT_BEGIN:
                    self.game_vars[GAME_STATE] = IN_FIGHT
                    self.GUI.handle_event(event)
                if event.subtype == FIGHT_END:
                    self.GUI.handle_event(event)
                if event.subtype == ACTION:
                    self.GameSound.handle_event(event)
                    self.Logic.handle_event(event)

            if event.type == PRINT_LINE:
                # Is it a command?
                if event.message.startswith("/"):
                    self.parse_command_input(event)
                else:
                    self.GUI.handle_event(event)

            if event.type == MESSAGE_BANNER:
                self.GUI.handle_event(event)

            if event.type == FLSCRN_TOGGLE:
                self.game_vars[FULL_SCREEN] = not self.game_vars[FULL_SCREEN]

                if self.game_vars[FULL_SCREEN]:
                    self.display_window = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
                else:
                    self.display_window = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

                self.Renderer.handle_event(event)

    def update(self):
        self.main_loop()

        for system in self.systems_list:
            system.main_loop()

        # Reset values for mouse clicks
        self.game_vars[MOUSE_CLICKED] = False
        self.game_vars[SCROLL_UP] = False
        self.game_vars[SCROLL_DOWN] = False

    def parse_command_input(self, event):
        parsed_input = event.message.split(" ")
        # Is it a simulated input?
        if event.message.startswith("/event "):

            # Is it a mouse click?
            if "mouseclick" in event.message:

                # Check if there were parameters passed to the command
                if len(parsed_input) > 2:
                    try:
                        input_pos = ast.literal_eval(parsed_input[2])
                    except SyntaxError:
                        input_pos = ast.literal_eval(parsed_input[2]+parsed_input[3])
                    make_event(pygame.MOUSEMOTION, pos=input_pos, rel=(0, 0), buttons=[])
                    make_event(pygame.MOUSEBUTTONUP, pos=input_pos, button=1)
                else:
                    make_event(pygame.MOUSEBUTTONUP, pos=(2, 2), button=1)
            else:
                error_message = "Event not recognized '" + parsed_input[1] + "'"
                make_event(PRINT_LINE, message=error_message, color=(255, 255, 0))
        else:
            error_message = "Command not recognized '" + parsed_input[0] + "'"
            make_event(PRINT_LINE, message=error_message, color=(255, 255, 0))
