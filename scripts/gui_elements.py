import math
import time
import random

from scripts.gui_image_loader import load_gui_from_image
from scripts import tools
from scripts.variables.localvars import *
from scripts.Colors import Color
from scripts.banners import Banner

pygame.font.init()


class Theme:

    """
    Provides am adaptable container for themes
     of the GUI items in this file, multiple themes are fine
     Six colors per theme are supported
     one main color, three accent colors, and two background colors.
     Colors are stored as RGB or RGBA tuples
    """

    def __init__(self, main_color=(0, 0, 0, 255), accent_color1=(0, 0, 0, 255), accent_color2=(0, 0, 0, 255),
                 accent_color3=(0, 0, 0, 255), chat_color=(0, 0, 0, 255), background_color1=(0, 0, 0, 255), background_color2=(0, 0, 0, 255),
                 error_color=(0, 0, 0, 255), reward_color=(0, 0, 0, 255), fight_color=(0, 0, 0, 255), font="lucidaconsole"):

        self.main_color = main_color

        self.accent1 = accent_color1
        self.accent2 = accent_color2
        self.accent3 = accent_color3

        self.chat_color = chat_color

        self.background_color1 = background_color1
        self.background_color2 = background_color2

        self.error_color = error_color
        self.reward_color = reward_color
        self.fight_color = fight_color

        self.font = pygame.font.SysFont(font, 15, True)


class ScrollingTextBox:

    def __init__(self, rect, theme, message_cap=40):

        self.position = (rect[0], rect[1])
        self.width = rect[2]
        self.height = rect[3]

        self.hover = False

        self.theme = theme
        self.font = self.theme.font

        self.MAXCHARACTERS = int(self.width/self.font.size("M")[0])

        self.ignore_next = False

        self.message_list = []
        self.message_dict = {}  # Key: message (string) / Value: color it should be (RBG/RGBA tuple)
        self.message_cap = message_cap  # Most amount of messages that can be held onto before they are deleted

        # Creates a copyable Surface for the final blit_image
        self.gui_texture = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.gui_texture.fill(self.theme.background_color1)
        pygame.draw.rect(self.gui_texture, self.theme.main_color, (0, 0, self.width, self.height), 3)

        # Provides memoization for the message strings that we'll be rendering
        self.message_board = pygame.Surface((self.width, (self.font.get_linesize() + 3) * self.message_cap))
        self.message_board.set_colorkey((0, 0, 0))
        self.message_board.convert()

        # The final image for blitting
        self.blit_image = self.gui_texture.copy()
        self.blit_image.convert()

        self.scroll_height = self.message_board.get_height() - self.height + 10

        self.init()

    def set_font(self, font):
        self.font = font

    def display_messages(self):
        self.blit_image = self.gui_texture.copy()
        self.blit_image.blit(self.message_board, (5, 5),
                             (0, self.scroll_height, self.width, self.height))
        pygame.draw.rect(self.blit_image, self.theme.main_color, (0, 0, self.width, self.height), 3)

    def update_message_board(self):

        # Clears the message board with its color_key
        self.message_board.fill((0, 0, 0))

        counter = 1
        for message in self.message_list:
            surface = self.font.render(message, False, self.message_dict[message])

            # This puts the newest messages closer to the bottom of the message_board
            self.message_board.blit(surface, (0, self.message_board.get_height() - (counter * (self.font.get_linesize() + 3))))
            counter += 1

        self.message_board.convert()
        self.display_messages()

    def init(self):
        self.update_message_board()

    def print_line(self, message, error_message=False, reward_message=False, fight_message=False, custom_color=None):

        # Message should be a single string
        # If custom_color is specified it should be an RGB or RGBA tuple
        # If custom_color is not specified then it render_color defaults to whatever the theme's accent1 is

        if custom_color:
            self.message_dict[message] = custom_color
        elif error_message:
            self.message_dict[message] = self.theme.error_color
        elif reward_message:
            self.message_dict[message] = self.theme.reward_color
        elif fight_message:
            self.message_dict[message] = self.theme.fight_color
        else:
            self.message_dict[message] = (178, 178, 178)

        self.message_list.insert(0, message)
        self.message_list = self.message_list[:self.message_cap]
        for message in self.message_list[self.message_cap:]:
            self.message_dict.pop(message)

        # Makes sure that when a new message appears the message box scrolls down to it
        self.scroll_height = self.message_board.get_height() - self.height + 10
        self.update_message_board()

    def handle_event(self, event):
        if event.type == PRINT_LINE:
            if self.ignore_next:
                self.ignore_next = False
                return
            message = event.message
            if message == "":
                if random.random() < .15:
                    message = "'Some people have nothing to say, and they say it all the time.' -Bono"
                else:
                    return
            elif message == "_del":
                # A control message used for removing the most recent message
                self.message_dict.pop(self.message_list[0])
                self.message_list = self.message_list[1:]
                return
            elif message == "_ign":
                # A control message use for ignoring the next message
                self.ignore_next = True
                return
            try:
                color = event.color
            except AttributeError:
                color = self.theme.main_color

            while len(message) > self.MAXCHARACTERS:
                split_point = 0

                # If the message is too long find the first space and cut the message there
                # TODO: move to [while:] loop and out of recursion
                for i in range(self.MAXCHARACTERS - 1, 0, -1):
                    if message[i] == " ":
                        split_point = i
                        break
                else:
                    split_point = self.MAXCHARACTERS - 1

                self.print_line(message[:split_point], custom_color=color)

                message = " " + message[split_point:]
            else:
                self.print_line(message, custom_color=color)

    def on_hover(self, engine):
        self.hover = True
        pygame.draw.rect(self.blit_image, self.theme.accent2, (0, 0, self.width, self.height), 3)
        if engine.game_vars[SCROLL_UP]:
            self.scroll_up()
        if engine.game_vars[SCROLL_DOWN]:
            self.scroll_down()

    def scroll_up(self):
        if len(self.message_list) > self.height / (self.font.get_linesize() + 3):
            self.scroll_height = max(self.scroll_height - self.font.get_linesize() + 3,
                                     self.message_board.get_height() - len(self.message_list) * (self.font.get_linesize() + 3) - 3)
        self.display_messages()

    def scroll_down(self):
        self.scroll_height = min(self.scroll_height + self.font.get_linesize(),
                                 self.message_board.get_height() - self.height + 10)
        self.display_messages()

    def update(self, engine):
        mouse_pos = pygame.mouse.get_pos()
        if self.position[0] <= mouse_pos[0] <= self.position[0] + self.width and \
                self.position[1] <= mouse_pos[1] <= self.position[1] + self.height:
            self.on_hover(engine)
        elif self.hover:
            self.hover = False
            pygame.draw.rect(self.blit_image, self.theme.main_color, (0, 0, self.width, self.height), 3)

    def render(self):
        return self.blit_image


class InputTextBox:

    def __init__(self, rect, theme):
        self.position = (rect[0], rect[1])
        self.width = rect[2]
        self.height = rect[3]

        self.theme = theme
        self.font = theme.font

        self.delete_held = False
        self.hold_time = 0      # Value for tracking duration of key holds, only allows one key button to be held at a time
        self.BUTTON_INTERVAL = .4

        self.XPADDING = 4
        self.YPADDING = self.height/2 - self.font.get_linesize()/2

        # Creates a copyable Surface for the final blit_image
        self.gui_texture = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.gui_texture.fill(self.theme.background_color1)
        pygame.draw.rect(self.gui_texture, self.theme.main_color, (0, 0, self.width, self.height), 3)

        # Provides memoization for the message strings that we'll be rendering
        self.message_board = pygame.Surface((self.width, self.font.get_linesize()))
        self.message_board.set_colorkey((0, 0, 0))
        self.message_board.convert()

        self.blit_img = self.gui_texture.copy().convert()

        self.active = False
        self.text = ''
        self.hover = False

        self.update_message_board()

    def on_hover(self):
        self.hover = True
        if self.active:
            pygame.draw.rect(self.blit_img, self.theme.reward_color, (0, 0, self.width, self.height), 3)
        else:
            pygame.draw.rect(self.blit_img, self.theme.accent2, (0, 0, self.width, self.height), 3)

    def update_message_board(self):

        # Clear the board by filling it with its colorkey
        self.message_board.fill((0, 0, 0))
        try:
            surface = self.font.render(self.text, False, self.theme.accent1)
        except ValueError:
            print("Problem rendering '{}'.".format(self.text))
            return
        self.message_board.blit(surface, (0, 0))

        # Clear the blit_img for nex round of text
        self.blit_img = self.gui_texture.copy()

        self.blit_img.blit(self.message_board, (self.XPADDING, self.YPADDING))

        if self.active:
            pygame.draw.rect(self.blit_img, self.theme.reward_color, (0, 0, self.width, self.height), 3)
        else:
            if self.hover:
                pygame.draw.rect(self.blit_img, self.theme.accent2, (0, 0, self.width, self.height), 3)
            else:
                pygame.draw.rect(self.blit_img, self.theme.main_color, (0, 0, self.width, self.height), 3)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SLASH:
                if not self.active:
                    self.text = ""
                    self.update_message_board()
                self.active = True
                pygame.draw.rect(self.blit_img, self.theme.reward_color, (0, 0, self.width, self.height), 3)
            if event.key == pygame.K_t:
                if not self.active:
                    self.active = True
                    pygame.draw.rect(self.blit_img, self.theme.reward_color, (0, 0, self.width, self.height), 3)
                    return
            if event.key == pygame.K_ESCAPE:
                pygame.draw.rect(self.blit_img, self.theme.main_color, (0, 0, self.width, self.height), 3)
                self.active = False
                if self.hover:
                    pygame.draw.rect(self.blit_img, self.theme.accent2, (0, 0, self.width, self.height), 3)
                else:
                    pygame.draw.rect(self.blit_img, self.theme.main_color, (0, 0, self.width, self.height), 3)
                return
            if event.key == pygame.K_RETURN:
                if self.active:
                    make_event(PRINT_LINE, message=self.text, color=self.theme.chat_color)
                    self.text = ""
                    self.active = False
                    self.update_message_board()
                    if self.hover:
                        pygame.draw.rect(self.blit_img, self.theme.accent2, (0, 0, self.width, self.height), 3)
                    else:
                        pygame.draw.rect(self.blit_img, self.theme.main_color, (0, 0, self.width, self.height), 3)
                return
            if event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                if self.active:
                    clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT).decode("utf8", "ignore")
                    clipboard_text = clipboard_text[:-1]
                    self.text += clipboard_text
                    self.update_message_board()
                    return

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[0:-1]
                self.delete_held = True
                self.update_message_board()
                return

            processed_text = tools.process_text(event)
            if self.active:
                # TODO: make the textbox scroll over if you have typed more than it can show
                self.text += processed_text
                self.update_message_board()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.delete_held = False
                self.hold_time = 0
                self.BUTTON_INTERVAL = .4

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            if self.position[0] <= mouse_pos[0] <= self.position[0] + self.width and \
                    self.position[1] <= mouse_pos[1] <= self.position[1] + self.height:
                self.on_hover()
            elif self.hover:
                self.hover = False
                if self.active:
                    pygame.draw.rect(self.blit_img, self.theme.reward_color, (0, 0, self.width, self.height), 3)
                else:
                    pygame.draw.rect(self.blit_img, self.theme.main_color, (0, 0, self.width, self.height), 3)

        if event.type == pygame.MOUSEBUTTONUP:
            if self.hover:
                self.active = True
                pygame.draw.rect(self.blit_img, self.theme.reward_color, (0, 0, self.width, self.height), 3)

                # Delete the error message produced by GameLogic
                make_event(PRINT_LINE, message="_ign")
            else:
                self.active = False
                pygame.draw.rect(self.blit_img, self.theme.main_color, (0, 0, self.width, self.height), 3)

    def update(self, engine):
        if self.active:
            if self.delete_held:
                self.hold_time += 1/engine.game_vars[FPS]
                if self.hold_time >= self.BUTTON_INTERVAL:
                    self.BUTTON_INTERVAL = min(self.BUTTON_INTERVAL - .1, self.BUTTON_INTERVAL)
                    self.BUTTON_INTERVAL = max(.1, self.BUTTON_INTERVAL)
                    self.hold_time = 0
                    if self.text == "":
                        return
                    if self.text[-1] != " ":
                        self.text = self.text[0:-1]
                    else:
                        self.text = self.text[0:-2]
                    self.update_message_board()

            # TODO: optimize the typing variable use to only set once, do it in the event handler
            engine.game_vars[TYPING] = True
        else:
            engine.game_vars[TYPING] = False

    def render(self):
        return self.blit_img


class Button:

    def __init__(self, rect, theme, action=None, action_kwargs=None, text="", style="rounded_gui"):
        self.position = (rect[0], rect[1])
        self.width = rect[2]
        self.height = rect[3]

        self.font = theme.font
        self.action = action
        if action_kwargs is None:
            self.action_kwargs = {}
        else:
            self.action_kwargs = action_kwargs
        self.text_img = self.font.render(text, False, Color.Gray)

        self.style = load_gui_from_image(style)

        base_image = self.style.render((self.width, self.height))
        base_image.blit(self.text_img, ((self.width-self.text_img.get_width())/2, (self.height-self.text_img.get_height())/2))
        base_image.convert()

        self.state = BASE_STATE

        self.base_state_image = None
        self.hovered_state_image = None
        self.disabled_state_image = None

        self.init_blit_images(base_image)

        # Signal that they are about to play
        self.play_sound = False
        self.stream_hash = None

        self.sound_file = "sounds/gui/gui_passover_01.wav"

        self.blit_image = self.base_state_image

    def set_position(self, pos):
        assert isinstance(pos, tuple)
        self.position = pos

    def in_bounds(self, pos):
        if tools.is_in_bounds(pos, (self.position[0], self.position[1], self.width, self.height)):
            return True
        return False

    def clean_up(self, lists):
        for containing_list in lists:
            if self in containing_list:
                containing_list.remove(self)

    def update_blit_image(self):
        if self.state == BASE_STATE:
            self.blit_image = self.base_state_image
        elif self.state == HOVERED:
            self.blit_image = self.hovered_state_image

    def render(self):
        return self.blit_image

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.in_bounds(event.pos) and self.state != DISABLED:
                self.use_action()
        elif event.type == pygame.MOUSEMOTION:
            if self.in_bounds(event.pos) and self.state != DISABLED:
                if self.state != HOVERED:
                    # If this is the first time the mouse is moving on it
                    self.play_sound = True
                self.state = HOVERED
            elif self.state == HOVERED:
                # If the button is hovered but the mouse isn't on it
                self.state = BASE_STATE
        self.update_blit_image()

    def update(self, engine):
        if self.play_sound:
            self.play_sound = False
            self.stream_hash = engine.Audio.play(self.sound_file)

    def use_action(self):
        try:
            print("GUI_ELEMENTS: Button '{}' created event of type {}.".format(str(hash(self)),
                                                                               str(self.action_kwargs["type"])))
        except KeyError:
            print("GUI ELEMENTS: Error parsing event type.")

        if self.action is not None:
            self.action(**self.action_kwargs)
        else:
            make_event(BANNER, message="Not Implemented Yet from " + str(hash(self)), color=Color.Red)

    def init_blit_images(self, base_image):

        # Create all necessary surfaces ahead of time and store them as fields
        self.base_state_image = base_image.copy()

        self.hovered_state_image = base_image.copy()
        temp_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        temp_surf.fill(Color.with_alpha(50, Color.WhiteSmoke))
        self.hovered_state_image.blit(temp_surf, (0, 0))
        self.hovered_state_image.set_colorkey(self.hovered_state_image.get_at((0, 0)))


class AbilityButton(Button):

    # The action_num argument is the index of the ability in the corresponding player's ability list

    def __init__(self, pos, action_num, ability, theme, player, target, grid):

        self.uses = ability.uses
        self.text = ability.name

        super().__init__((pos[0], pos[1], 96, 96), theme, make_event,
                         {"type": FIGHT_EVENT, "subtype": ACTION, "num": action_num}, ability.name,
                         "semi_rounded_gui")

        self.is_usable = lambda: player.is_ability_usable(player.abilities[action_num], target, grid)

        try:
            ability_image = ability.image
        except AttributeError:
            print("GUI_ELEMENTS: No image found for {} ability.".format(ability))
            print("GUI_ELEMENTS: Reverting to default image.")
            # TODO: fix the error handling here (change the default image to a test image)
            ability_image = None

        self.update_blit_image()

    @staticmethod
    def remove_corners(surface):
        temp_color = surface.get_at((20, 0))
        width, height = surface.get_width(), surface.get_height()
        pygame.draw.rect(surface, temp_color, (8, 8, 4, 4))
        pygame.draw.rect(surface, temp_color, (width-12, 8, 4, 4))
        pygame.draw.rect(surface, temp_color, (8, height-12, 4, 4))
        pygame.draw.rect(surface, temp_color, (width-12, width-12, 4, 4))

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if self.uses > 0 and self.in_bounds(event.pos):
                self.update_uses()
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]:
                if int(pygame.key.name(event.key))-1 == self.action_kwargs['num']:
                    # The left side is the number that the event represents, adjusted by one because the abilities are 0
                    # indexed but to the users, using the 0th ability is weird.

                    if self.state != DISABLED:
                        self.use_action()
                    else:
                        banner = Banner("[{}] cannot be used".format(self.text))
                        make_event(BANNER, banner=banner)
        if event.type == FIGHT_EVENT:
            self.update_usability()

    def update_blit_image(self):

        if self.state == HOVERED:
            self.blit_image = self.hovered_state_image
        elif self.state == DISABLED:
            self.blit_image = self.disabled_state_image
        else:
            self.blit_image = self.base_state_image

    def prepare_text(self, text):
        text_surf = self.font.render(str(text), False, Color.White)
        text_surf2 = self.font.render(str(text), False, Color.Black)
        temp_surf = pygame.Surface((text_surf.get_width(), text_surf.get_height()))
        temp_surf.fill((255, 0, 128))
        temp_surf.blit(text_surf2, (2, 1))
        temp_surf.blit(text_surf, (0, 0))
        temp_surf.set_colorkey((255, 0, 128))
        return temp_surf

    def update_uses(self, reset=False):
        if not reset:
            self.uses -= 1
            if self.uses == 0:
                self.state = DISABLED
                return

    def update(self, engine):
        if self.state == HOVERED:
            pos = pygame.mouse.get_pos()
            make_event(SURFACE, surf=self.prepare_text(self.text), pos=(pos[0], pos[1]-25), z=2)
        super().update(engine)

    def init_blit_images(self, base_image):

        temp_image = pygame.image.load("graphics//gui_images//ability_icons//icon_set_02.png")
        temp_image.set_colorkey((255, 0, 128))
        temp_surf = pygame.Surface((20, 20))
        temp_surf.blit(temp_image, (0, 0), (289, 487, 20, 20))
        temp_surf = pygame.transform.scale(temp_surf, (80, 80))
        base_image.blit(temp_surf, (8, 8))
        self.remove_corners(base_image)

        # Create all necessary surfaces ahead of time

        self.base_state_image = base_image.copy()
        self.base_state_image.blit(self.prepare_text(self.uses), (self.width - 18, 18))

        self.hovered_state_image = base_image.copy()
        self.hovered_state_image.blit(self.prepare_text(self.uses), (self.width - 18, 18))
        temp_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        temp_surf.fill(Color.with_alpha(50, Color.WhiteSmoke))
        self.hovered_state_image.blit(temp_surf, (0, 0))
        self.hovered_state_image.set_colorkey(self.hovered_state_image.get_at((0, 0)))

        self.disabled_state_image = base_image.copy()
        temp_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        temp_surf.fill(Color.with_alpha(200, (85, 85, 85)))
        self.disabled_state_image.blit(temp_surf, (0, 0))
        self.disabled_state_image.set_colorkey(self.disabled_state_image.get_at((0, 0)))

    def update_usability(self):
        if not self.is_usable():
            self.state = DISABLED


class DisplayBox:

    def __init__(self, gui_elements, title=None, pos=None, file_source="semi_rounded_gui", dimensions=None):

        # Gui objects are stored by as keys to their blit position in the DisplayBox
        self.gui_list = gui_elements

        self.width = 0
        self.height = 0

        self.init_dimensions()

        if dimensions is None:
            dimensions = (self.width, self.height)

        if pos is None:
            screen = pygame.display.get_surface()
            self.position = ((screen.get_width() - self.width) / 2, 100)

        self.blit_image = pygame.Surface(dimensions)

        self.background_image = load_gui_from_image(file_source).render(dimensions)
        self.blit_image.blit(self.background_image, (0, 0))
        self.blit_image.set_colorkey((0, 0, 0))

        if title is not None:
            font = pygame.font.SysFont('lucidaconsole', 18)
            text_image = font.render(title, False, Color.Gray)
            pos = ((self.width - text_image.get_width())/2, 10)
            self.blit_image.blit(text_image, pos)

    def handle_event(self, event):
        # Events are positioned relative to the screen but the buttons are positioned relative to the DisplayBox so they
        # Have to be adjusted to work with the buttons
        if event.type == pygame.MOUSEMOTION:
            pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
            event = make_dummy_event(pygame.MOUSEMOTION, pos=pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
            event = make_dummy_event(pygame.MOUSEBUTTONUP, pos=pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
            event = make_dummy_event(pygame.MOUSEBUTTONDOWN, pos=pos)
        for gui in self.gui_list:
            gui.handle_event(event)

    def update(self, engine):
        for gui in self.gui_list:
            gui.update(engine)

    def render(self):
        return_surface = self.blit_image.copy()
        for gui in self.gui_list:
            return_surface.blit(gui.render(), gui.position)
        return return_surface

    def init_dimensions(self):
        # Save the gui widths
        width_list = []

        for gui in self.gui_list:

            # Set width as total of internal guis widths
            self.width += gui.width
            width_list.append(gui.width)

            # Set height to the height of the tallest gui
            if gui.height > self.height:
                self.height = gui.height

        # Add a little padding to the box
        self.width *= 1.5
        self.height *= 2
        self.width = int(self.width)
        self.height = int(self.height)

        x_padding = (self.width - sum(width_list)) / (len(self.gui_list)+1)
        x_padding = int(x_padding)
        # Store the position of guis
        x_pos_list = []
        counter = x_padding

        for width in width_list:
            x_pos_list.append(counter)
            counter += x_padding + width
        counter = 0
        for gui in self.gui_list:
            gui.position = (x_pos_list[counter], int((self.height - gui.height)/2)+10)
            counter += 1
