from scripts.variables.localvars import *
import scripts.map_engine
from scripts.Colors import Color
import scripts.tools
from scripts.tools import os_format_dir_name
from systems.BaseSystem import BaseSystem


class Renderer(BaseSystem):

    def __init__(self):
        self.Engine = None
        self.game_vars = {}
        
        self.mapname = os_format_dir_name("maps{os_dir}Elemental_plane.map")
        self.terrain = scripts.map_engine.Map_Engine.load_map(self.mapname)

        # Surfaces in this are blitted before the sprites
        self.surf_dict0 = {}
        # Surfaces in this are blitted after sprites
        self.surf_dict1 = {}
        # Surfaces in this are blitted after the base gui
        self.surf_dict2 = {}
        # Surfaces in this are blitted after the pause screen
        self.surf_dict3 = {}
        # Surfaces in this are always blitted and updated
        self.surf_dict4 = {}

        # Make sure this contains all surf_dicts
        self.surf_dict_list = [self.surf_dict0, self.surf_dict1, self.surf_dict2, self.surf_dict3, self.surf_dict4]

        # Prevents surfaces from tearing on the screen during pause menu by holding all rects from all surfaces in
        # surf_dict4
        self.surf_dict4_copy = []

        self.cursor_img = pygame.Surface((31, 27))
        self.cursor_img.blit(pygame.image.load(os_format_dir_name("graphics{os_dir}gui_images{os_dir}cursor.png")), (0, 0))
        self.cursor_img.set_colorkey(Color.Red)

        self.background_img = None

        self.pause_layer = pygame.Surface((0, 0))

        self.pause_frame = pygame.Surface((0, 0))
        self.paused = False
        self.pause_flagged = False

        # Used for tracking blits per frame for debugging purposes
        self.bpf = 0

    def set_up(self):
        self.terrain.convert()
        self.cursor_img.convert()
        self.game_vars[TILE_SIZE] = 80
        self.game_vars[BOARD_OFFSET] = (self.game_vars[TILE_SIZE] * 7, self.game_vars[TILE_SIZE])

        self.pause_layer = pygame.Surface((self.Engine.window_width, self.Engine.window_height), pygame.SRCALPHA)
        self.pause_layer.fill(Color.with_alpha(100, (127, 127, 127)))
        self.pause_layer.convert()

        self.background_img = pygame.Surface((self.Engine.window_width, self.Engine.window_height))
        self.background_img.fill(Color.Wheat)
        self.background_img.blit(self.terrain, self.game_vars[BOARD_OFFSET])

    def set_engine(self, new_engine):
        self.Engine = new_engine
        self.game_vars = new_engine.game_vars
        return True

    def init(self, engine):
        self.set_engine(engine)
        self.set_up()
        pygame.mouse.set_visible(False)

    def handle_event(self, event):
        if event.type == SURFACE:
            try:
                self.add_surface(event.surf, event.pos, event.z)
            except AttributeError as e:
                print("Invalid surface event")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.game_vars[PAUSE]:
                # This gives the rest of the systems one frame to react to the game being paused
                self.pause_flagged = True
            else:
                self.paused = False
                self.surf_dict4_copy.clear()

        if event.type == FLSCRN_TOGGLE:
            self.Engine.display_window.blit(self.pause_frame, (0, 0))
            pygame.display.flip()

    def main_loop(self):

        # Rest bpf value
        self.bpf = 0

        if self.pause_flagged:
            self.do_pause_screencap()
            self.pause_flagged = False
            self.paused = True

        # TODO: do everything in a 1/16 scale and then scale up (1 square becomes 20x20)
        if not self.paused:
            self.Engine.display_window.fill(Color.Wheat)

            offset = (self.game_vars[BOARD_OFFSET][0]+self.game_vars[GRID_OFFSET][0],
                      self.game_vars[BOARD_OFFSET][1]+self.game_vars[GRID_OFFSET][1])
            self.Engine.display_window.blit(self.terrain, offset)
            self.count_blit()

            for surf in self.surf_dict0:
                for spot in self.surf_dict0[surf]:
                    self.Engine.display_window.blit(surf, spot)
                    self.count_blit()

            for sprite in self.game_vars[SPRITE_LIST]:
                self.Engine.display_window.blit(sprite.draw(),
                                                (sprite.pos[0] * 80 + offset[0] + sprite.offset[0],
                                                sprite.pos[1] * 80 + offset[1] + sprite.offset[1]))
                self.count_blit()

            for surf in self.surf_dict1:
                for spot in self.surf_dict1[surf]:
                    self.Engine.display_window.blit(surf, spot)
                    self.count_blit()

            for surf in self.surf_dict2:
                for spot in self.surf_dict2[surf]:
                    self.Engine.display_window.blit(surf, spot)
                    self.count_blit()
        else:
            self.Engine.display_window.blit(self.pause_frame, (0, 0))
            self.count_blit()

            for surf in self.surf_dict3:
                for spot in self.surf_dict3[surf]:
                    self.Engine.display_window.blit(surf, spot)
                    self.count_blit()

        for surf in self.surf_dict4:
            for spot in self.surf_dict4[surf]:
                self.Engine.display_window.blit(surf, spot)
                self.count_blit()

        # To account for the mouse blit, which comes after and therefore can't be logged normally
        self.count_blit()

        if self.game_vars[DEBUG]:
            self.display_debug_info()

        self.Engine.display_window.blit(self.cursor_img, pygame.mouse.get_pos())

        self.update_screen()

        for surf_dict in self.surf_dict_list:
            surf_dict.clear()

    def do_pause_screencap(self):
        self.Engine.display_window.fill(Color.Wheat)

        offset = (self.game_vars[BOARD_OFFSET][0] + self.game_vars[GRID_OFFSET][0],
                  self.game_vars[BOARD_OFFSET][1] + self.game_vars[GRID_OFFSET][1])

        self.Engine.display_window.blit(self.terrain, offset)
        self.count_blit()

        for surf in self.surf_dict0:
            for spot in self.surf_dict0[surf]:
                self.Engine.display_window.blit(surf, spot)
                self.count_blit()

        for sprite in self.game_vars[SPRITE_LIST]:
            self.Engine.display_window.blit(sprite.draw(),
                                            (sprite.pos[0] * 80 + offset[0] +
                                             sprite.offset[0],
                                             sprite.pos[1] * 80 + offset[1] +
                                             sprite.offset[1]))
            self.count_blit()

        for surf in self.surf_dict1:
            for spot in self.surf_dict1[surf]:
                self.Engine.display_window.blit(surf, spot)
                self.count_blit()

        for surf in self.surf_dict2:
            for spot in self.surf_dict2[surf]:
                self.Engine.display_window.blit(surf, spot)
                self.count_blit()

        self.pause_frame = self.Engine.display_window.copy()
        self.paused = True
        self.pause_frame.blit(self.pause_layer, (0, 0))
        self.count_blit()
        self.Engine.display_window.blit(self.pause_frame, (0, 0))
        self.count_blit()
        pygame.display.flip()

    def display_debug_info(self):
        self.Engine.display_window.blit(self.Engine.font.render("FPS: " + str(round(self.game_vars[FPS], 1)),
                                                                0, Color.Red), (0, 0))
        self.count_blit()
        self.Engine.display_window.blit(self.Engine.font.render("Dimensions: " + str((self.Engine.window_width,
                                                                                      self.Engine.window_height)),
                                                                0, Color.Red), (0, 50))
        self.count_blit()
        self.Engine.display_window.blit(self.Engine.font.render("RMOUSE: " + str(self.Engine.game_vars[RMOUSE_POS]),
                                                                0, Color.Red), (0, 100))
        self.count_blit()
        self.Engine.display_window.blit(
            self.Engine.font.render("ARM: " + str(self.Engine.game_vars[ADJUSTED_RMOUSE_POS]),
                                    0, Color.Red), (0, 150))
        self.count_blit()

        # To account for blitting the debug info
        self.count_blit()
        self.Engine.display_window.blit(
            self.Engine.font.render("BPF: " + str(self.bpf), 0, Color.Red), (0, 200))

    def update_screen(self):
        if not self.paused:
            pygame.display.flip()
        else:
            x_pos = (self.Engine.window_width - 400) / 2
            pygame.display.update((x_pos, 0, 400, self.Engine.window_height))
            mousex, mousey = pygame.mouse.get_pos()
            pygame.display.update((mousex-150, mousey-100, 300, 200))
            if self.game_vars[DEBUG]:
                pygame.display.update((0, 0, 300, 250))
            for rect in self.surf_dict4_copy:
                pygame.display.update(rect)

    def count_blit(self):
        self.bpf += 1

    def add_surface(self, surface, pos,  z_val):
        # This finds the blit layer that the surface belongs to
        eventz = min(z_val, len(self.surf_dict_list) - 1)
        # This adds the the surf and pos to the appropriate list in the dict,
        # or if there is no list, it makes a new one.
        # The surf is the key to a list of positions where it is to be blitted to
        if self.surf_dict_list[eventz].get(surface) is None:
            self.surf_dict_list[eventz][surface] = [pos]
        else:
            self.surf_dict_list[eventz][surface].append([pos])
            
        if eventz == 4:
            rect = (pos[0], pos[1], surface.get_width(), surface.get_height())
            if rect not in self.surf_dict4_copy:
                self.surf_dict4_copy.append(rect)
