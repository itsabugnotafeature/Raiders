import scripts.gui_elements
import scripts.tools
from scripts.Colors import Color
from scripts.variables.localvars import *
from systems.BaseSystem import BaseSystem


class GUI(BaseSystem):

    def __init__(self):
        self.Engine = None
        self.game_vars = {}

        self.GUITheme = scripts.gui_elements.Theme(main_color=(178, 178, 178),
                                                   accent_color1=Color.Yellow,
                                                   accent_color2=Color.LightGoldenrodYellow,
                                                   accent_color3=(122, 59, 46),
                                                   chat_color=(147, 112, 219),
                                                   background_color1=(Color.with_alpha(200, Color.DimGray)),
                                                   error_color=Color.Red,
                                                   reward_color=(51, 153, 255),
                                                   fight_color=(255, 102, 0))

        self.gui_list = []
        self.base_gui_addresses = []
        self.fight_gui_addresses = []
        self.pause_gui_addresses = []

        self.pathing_highlight = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.pathing_highlight.fill(Color.with_alpha(100, Color.WhiteSmoke))
        pygame.draw.rect(self.pathing_highlight, Color.with_alpha(200, Color.WhiteSmoke), (0, 0, 78, 78), 2)

        self.move_highlight = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.move_highlight.fill(Color.with_alpha(100, Color.CornflowerBlue))
        pygame.draw.rect(self.move_highlight, Color.with_alpha(200, Color.CornflowerBlue), (0, 0, 78, 78), 2)

        self.choosing_highlight = pygame.Surface((68, 68), pygame.SRCALPHA)
        self.choosing_highlight.fill(Color.with_alpha(100, Color.Gray))
        pygame.draw.rect(self.choosing_highlight, Color.with_alpha(200, Color.DimGray), (0, 0, 66, 66), 2)

        self.fight_highlight = pygame.Surface((68, 68), pygame.SRCALPHA)
        self.fight_highlight.fill(Color.with_alpha(100, Color.IndianRed))
        pygame.draw.rect(self.fight_highlight, Color.with_alpha(200, Color.IndianRed), (0, 0, 66, 66), 2)

        self.friendly_highlight = pygame.Surface((68, 68), pygame.SRCALPHA)
        self.friendly_highlight.fill(Color.with_alpha(100, Color.LightGreen))
        pygame.draw.rect(self.friendly_highlight, Color.with_alpha(200, Color.LightGreen), (0, 0, 66, 66), 2)

    def set_up(self):
        self.pathing_highlight.convert()
        self.move_highlight.convert()
        self.fight_highlight.convert()
        self.friendly_highlight.convert()

        self.gui_list.append(scripts.gui_elements.ScrollingTextBox((4, self.Engine.window_height - 234, 400, 196),
                                                                   self.GUITheme))
        self.base_gui_addresses.append(0)

        self.gui_list.append(scripts.gui_elements.InputTextBox((4, self.Engine.window_height - 35, 400, 30),
                                                               self.GUITheme))
        self.base_gui_addresses.append(1)

        self.game_vars[OUTPUT_CONSOLE] = self.gui_list[0]

        for sprite in self.game_vars[SPRITE_LIST]:
            sprite.render_name(self.Engine.font, self.GUITheme)

    def is_mouse_on_gui(self):
        mouse_pos = pygame.mouse.get_pos()
        for gui in self.gui_list:
            if scripts.tools.is_in_bounds(mouse_pos, (gui.position[0], gui.position[1], gui.width, gui.height)):
                return True
        return False

    def fight_clean_up(self):
        self.fight_gui_addresses.reverse()
        for address in self.fight_gui_addresses:
            self.gui_list.pop(address)
        self.fight_gui_addresses = []

    def set_engine(self, new_engine):
        self.Engine = new_engine
        self.game_vars = new_engine.game_vars

    def init(self, engine):
        self.set_engine(engine)
        self.set_up()

    def display_fight_gui(self, player):
        for i in range(len(player.abilities)):
            button_x = 580 + i % 4 * 135
            button_y = 740 + (int(i / 4)) * 110
            self.gui_list.append(scripts.gui_elements.AbilityButton((button_x, button_y), i, self.GUITheme,
                                                                    player.abilities[i].name,
                                                                    image="icon_set_02",
                                                                    image_pos=(289, 487),
                                                                    uses=player.abilities[i].uses))
            self.fight_gui_addresses.append(len(self.gui_list) - 1)

    def pause_clean_up(self):
        self.pause_gui_addresses.reverse()
        for gui in self.pause_gui_addresses:
            self.gui_list.pop(gui)
        self.pause_gui_addresses = []

    def handle_event(self, event):
        if event.type == FIGHT_EVENT:
            if event.subtype == FIGHT_BEGIN:
                self.display_fight_gui(event.player)
            elif event.subtype == FIGHT_END:
                self.fight_clean_up()

        if event.type == MESSAGE_BANNER:
            surf, pos = self.prepare_message_banner(event)
            make_event(SURFACE, surf=surf, pos=pos, z=3)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game_vars[PAUSE]:
                    self.dehover_guis()
                    self.display_pause_gui()
                    for address in self.base_gui_addresses:
                        self.gui_list[address].handle_event(event)
                else:
                    self.pause_clean_up()
        if not self.game_vars[PAUSE]:
            for gui in self.gui_list:
                gui.handle_event(event)
        else:
            for address in self.pause_gui_addresses:
                self.gui_list[address].handle_event(event)

    def main_loop(self):
        if self.game_vars[GAME_STATE] == PATHING:
            for spot in self.game_vars[MOVABLE_LIST]:
                make_event(SURFACE, surf=self.pathing_highlight.copy(),
                           pos=(spot[0] * 80 + self.game_vars[BOARD_OFFSET][0],
                                spot[1] * 80 + self.game_vars[BOARD_OFFSET][1]), z=0)

        for gui in self.gui_list:
            gui.update(self.Engine)

        if self.game_vars[GAME_STATE] == ATTACKING:
            self.make_attacking_tiles()
        elif self.game_vars[GAME_STATE] == PATHING and not self.game_vars[PAUSE]:
            self.make_pathing_tiles()
        counter = 0
        for sprite in self.game_vars[SPRITE_LIST]:

            # Makes the info panels on the side for each sprite in play
            # TODO: also include dead bosses
            # pos = (counter*85, 10)
            # make_event(SURFACE, surf=sprite.get_nameplate(), pos=pos, z=1)
            # counter += 1

            if sprite.fightable:

                self.make_name_plates(sprite)

                if sprite.health < sprite.maxhealth:

                    self.make_health_bars(sprite)

        for address in self.fight_gui_addresses + self.base_gui_addresses:
            gui = self.gui_list[address]
            make_event(SURFACE, surf=gui.render(), pos=gui.position, z=1)
        if self.game_vars[PAUSE]:
            for address in self.pause_gui_addresses:
                gui = self.gui_list[address]
                make_event(SURFACE, surf=gui.render(), pos=gui.position, z=3)

    # HELPER FUNCTIONS #

    def make_health_bars(self, sprite):
        pos = (sprite.pos[0] * self.game_vars[TILE_SIZE] + self.game_vars[BOARD_OFFSET][0] + 12,
               sprite.pos[1] * self.game_vars[TILE_SIZE] + self.game_vars[BOARD_OFFSET][1] + 60)
        surf = pygame.Surface((68, 4))
        surf.fill(Color.Brown)
        health_percentage = sprite.health / sprite.maxhealth
        color = scripts.tools.get_percentage_color(health_percentage)
        if health_percentage > 0:
            pygame.draw.rect(surf, color, (0, 0, health_percentage * surf.get_width(), 10))
        make_event(SURFACE, surf=surf, pos=pos, z=0)

    def make_name_plates(self, sprite):
        pos = (sprite.pos[0] * self.game_vars[TILE_SIZE] + self.game_vars[BOARD_OFFSET][0],
               sprite.pos[1] * self.game_vars[TILE_SIZE] + self.game_vars[BOARD_OFFSET][1] - 50)
        make_event(SURFACE, surf=sprite.name_img, pos=pos, z=1)

    def make_attacking_tiles(self):
        for sprite in self.game_vars[SPRITE_LIST]:
            if self.game_vars[ADJUSTED_RMOUSE_POS] == sprite.pos:
                if sprite.type == "player":
                    if self.game_vars[FRIENDLY_FIRE]:
                        make_event(SURFACE, surf=self.friendly_highlight,
                                   pos=(sprite.pos[0] * 80 + self.game_vars[BOARD_OFFSET][0] + 8,
                                        sprite.pos[1] * 80 + self.game_vars[BOARD_OFFSET][1] + 6), z=0)
                else:
                    make_event(SURFACE, surf=self.fight_highlight,
                               pos=(sprite.pos[0] * 80 + self.game_vars[BOARD_OFFSET][0] + 8,
                                    sprite.pos[1] * 80 + self.game_vars[BOARD_OFFSET][1] + 6), z=0)
            else:
                if sprite.type == "monster":
                    make_event(SURFACE, surf=self.choosing_highlight,
                               pos=(sprite.pos[0] * 80 + self.game_vars[BOARD_OFFSET][0] + 8,
                                    sprite.pos[1] * 80 + self.game_vars[BOARD_OFFSET][1] + 6), z=0)
                elif sprite.type == "player" and self.game_vars[FRIENDLY_FIRE]:
                    make_event(SURFACE, surf=self.choosing_highlight,
                               pos=(sprite.pos[0] * 80 + self.game_vars[BOARD_OFFSET][0] + 8,
                                    sprite.pos[1] * 80 + self.game_vars[BOARD_OFFSET][1] + 6), z=0)

    def make_pathing_tiles(self):
        if self.game_vars[ADJUSTED_RMOUSE_POS] in self.game_vars[MOVABLE_LIST]:
            make_event(SURFACE, surf=self.move_highlight, pos=self.game_vars[RMOUSE_POS], z=0)

    def display_pause_gui(self):
        # The number added to self.Engine.window_width should equal the width of the button
        width = (self.Engine.window_width - 400) / 2
        height = 150
        self.gui_list.append(scripts.gui_elements.Button((width, height + 48, 400, 48), self.GUITheme,
                                                         text="Unpause (Not Implemented)"))
        self.pause_gui_addresses.append(len(self.gui_list) - 1)
        self.gui_list.append(scripts.gui_elements.Button((width, height + 48 * 2 + 16, 400, 48), self.GUITheme,
                                                         text="(Not Implemented)"))
        self.pause_gui_addresses.append(len(self.gui_list) - 1)
        self.gui_list.append(scripts.gui_elements.Button((width, height + 48 * 3 + 32, 400, 48), self.GUITheme,
                                                         text="(Not Implemented)"))
        self.pause_gui_addresses.append(len(self.gui_list) - 1)
        self.gui_list.append(scripts.gui_elements.Button((width, height + 48 * 4 + 46, 400, 48), self.GUITheme,
                                                         text="(Not Implemented)"))
        self.pause_gui_addresses.append(len(self.gui_list) - 1)
        self.gui_list.append(scripts.gui_elements.Button((width, height + 48 * 5 + 62, 400, 48), self.GUITheme,
                                                         text="(Not Implemented)"))
        self.pause_gui_addresses.append(len(self.gui_list) - 1)

    def prepare_message_banner(self, event):

        temp_surf = self.GUITheme.font.render(event.message, False, event.color)
        pos = ((self.Engine.window_width - temp_surf.get_width()) / 2, 50)
        return temp_surf, pos

    def dehover_guis(self):
        for gui in self.gui_list:
            if isinstance(gui, scripts.gui_elements.Button):
                gui.state = BASE_STATE
                gui.update_blit_image()
            if isinstance(gui, scripts.gui_elements.ScrollingTextBox):
                gui.hover = False
                gui.update_message_board()
            if isinstance(gui, scripts.gui_elements.InputTextBox):
                gui.hover = False
                gui.update_message_board()