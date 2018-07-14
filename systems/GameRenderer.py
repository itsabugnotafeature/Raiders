from scripts.variables.localvars import *
import scripts.map_engine
from scripts.Colors import Color
import scripts.tools
from systems.BaseSystem import BaseSystem


class Renderer(BaseSystem):

    def __init__(self):
        self.Engine = None
        self.game_vars = {}
        
        self.mapname = "maps//Elemental_plane.map"
        self.terrain = scripts.map_engine.Map_Engine.load_map(self.mapname)

        # Surfaces in this are blitted before the sprites
        self.surf_dict0 = {}
        # Surfaces in this are blitted after sprites
        self.surf_dict1 = {}
        # Surfaces in this are blitted after the base gui
        self.surf_dict2 = {}
        # Surfaces in this are blitted after the pause screen
        self.surf_dict3 = {}

        self.surf_dict_list = [self.surf_dict0, self.surf_dict1, self.surf_dict2, self.surf_dict3]

        self.cursor_img = pygame.Surface((31, 27))
        self.cursor_img.blit(pygame.image.load("graphics//gui_images//cursor.png"), (0, 0))
        self.cursor_img.set_colorkey(Color.Red)

        self.background_img = None

        self.pause_layer = pygame.Surface((0, 0))

        self.pause_frame = pygame.Surface((0, 0))
        self.paused = False
        self.pause_flagged = False

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
            # This finds the blit layer that the surface belongs to
            eventz = min(event.z, len(self.surf_dict_list)-1)
            # This adds the the surf and pos to the appropriate list in the dict,
            # or if there is no list, it makes a new one.
            # The surf is the key to a list of positions where it is to be blitted to
            if not self.surf_dict_list[eventz].get(event.surf):
                self.surf_dict_list[eventz][event.surf] = [event.pos]
            else:
                self.surf_dict_list[eventz][event.surf] += [event.pos]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.game_vars[PAUSE]:
                # This gives the rest of the systems one frame to react to the game being paused
                self.pause_flagged = True
            else:
                self.paused = False

        if event.type == FLSCRN_TOGGLE:
            self.Engine.display_window.blit(self.pause_frame, (0, 0))
            pygame.display.flip()

    def main_loop(self):

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

            for surf in self.surf_dict0:
                for spot in self.surf_dict0[surf]:
                    self.Engine.display_window.blit(surf, spot)

            for sprite in self.game_vars[SPRITE_LIST]:
                self.Engine.display_window.blit(sprite.draw(),
                                                (sprite.pos[0] * 80 + offset[0] + sprite.offset[0],
                                                sprite.pos[1] * 80 + offset[1] + sprite.offset[1]))

            for surf in self.surf_dict1:
                for spot in self.surf_dict1[surf]:
                    self.Engine.display_window.blit(surf, spot)

            for surf in self.surf_dict2:
                for spot in self.surf_dict2[surf]:
                    self.Engine.display_window.blit(surf, spot)
        else:
            self.Engine.display_window.blit(self.pause_frame, (0, 0))

            for surf in self.surf_dict3:
                for spot in self.surf_dict3[surf]:
                    self.Engine.display_window.blit(surf, spot)

        if self.game_vars[DEBUG]:
            self.display_debug_info()

        self.Engine.display_window.blit(self.cursor_img, pygame.mouse.get_pos())

        self.surf_dict0.clear()
        self.surf_dict1.clear()
        self.surf_dict2.clear()
        self.surf_dict3.clear()

        if not self.paused:
            pygame.display.flip()
        else:
            width = (self.Engine.window_width - 400) / 2
            pygame.display.update((width, 0, 400, self.Engine.window_height))
            mousex, mousey = pygame.mouse.get_pos()
            pygame.display.update((mousex-100, mousey-100, 200, 200))
            pygame.display.update((0, 0, 300, 200))

    def do_pause_screencap(self):
        self.Engine.display_window.fill(Color.Wheat)

        offset = (self.game_vars[BOARD_OFFSET][0] + self.game_vars[GRID_OFFSET][0],
                  self.game_vars[BOARD_OFFSET][1] + self.game_vars[GRID_OFFSET][1])

        self.Engine.display_window.blit(self.terrain, offset)

        for surf in self.surf_dict0:
            for spot in self.surf_dict0[surf]:
                self.Engine.display_window.blit(surf, spot)

        for sprite in self.game_vars[SPRITE_LIST]:
            self.Engine.display_window.blit(sprite.draw(),
                                            (sprite.pos[0] * 80 + offset[0] +
                                             sprite.offset[0],
                                             sprite.pos[1] * 80 + offset[1] +
                                             sprite.offset[1]))

        for surf in self.surf_dict1:
            for spot in self.surf_dict1[surf]:
                self.Engine.display_window.blit(surf, spot)

        for surf in self.surf_dict2:
            for spot in self.surf_dict2[surf]:
                self.Engine.display_window.blit(surf, spot)

        self.pause_frame = self.Engine.display_window.copy()
        self.paused = True
        self.pause_frame.blit(self.pause_layer, (0, 0))
        self.Engine.display_window.blit(self.pause_frame, (0, 0))
        pygame.display.flip()

    def display_debug_info(self):
        self.Engine.display_window.blit(self.Engine.font.render("FPS: " + str(round(self.game_vars[FPS], 1)),
                                                                0, Color.Red), (0, 0))
        self.Engine.display_window.blit(self.Engine.font.render("Dimensions: " + str((self.Engine.window_width,
                                                                                      self.Engine.window_height)),
                                                                0, Color.Red), (0, 50))
        self.Engine.display_window.blit(self.Engine.font.render("RMOUSE: " + str(self.Engine.game_vars[RMOUSE_POS]),
                                                                0, Color.Red), (0, 100))
        self.Engine.display_window.blit(
            self.Engine.font.render("ARM: " + str(self.Engine.game_vars[ADJUSTED_RMOUSE_POS]),
                                    0, Color.Red), (0, 150))
