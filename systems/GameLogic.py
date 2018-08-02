import sys
from scripts.Colors import Color
from scripts.variables.localvars import *
from scripts.variables.events import *
import scripts.animations
from scripts import Astar as Astar
from scripts import tools
from systems.BaseSystem import BaseSystem
from scripts import pathing
from scripts import fighting
from scripts import banners


class Logic(BaseSystem):

    def __init__(self, *args, **kwargs):
        self.Engine = None
        self.game_vars = {}
        self.sprite_counter = 0
        self.movable_list = []
        blocked_spots = [(3, 0), (4, 0), (3, 1), (4, 1), (4, 2), (6, 3), (5, 4), (6, 4), (7, 4)]
        for i in range(8):
            blocked_spots.append((-1, i))
            blocked_spots.append((8, i))
            blocked_spots.append((i, -1))
            blocked_spots.append((i, 8))

        self.grid = Astar.Grid(8, 8, blocked_spots)
        self.path = []
        self.path_index = 0
        self.vector_dic = {}

        self.active_sprite = None
        self.active_target = None

        # These are set to the player and monster of any engagement after the active_sprite has finished his ATTACKING
        # state. They are reset to None at the end of the fight and are completely independent of active_sprite and
        # active_target
        self.player = None
        self.monster = None

        self.turn_counter = 1

        self.PathManager = pathing.PathManager(self.grid)
        self.FightManager = fighting.FightManager(self)

    def set_engine(self, new_engine):
        self.Engine = new_engine
        self.game_vars = new_engine.game_vars
        return True

    def set_up(self):
        for sprite in self.game_vars[SPRITE_LIST]:
            self.grid.wpush(sprite.pos)

    def init(self, engine):
        self.set_engine(engine)
        self.FightManager.set_engine(engine)
        self.set_up()

    def player_loop(self):
        if self.game_vars[GAME_STATE] == PATHING:
            if self.game_vars[SKIP_SEQUENCE] and not self.game_vars[TYPING]:
                make_event(PRINT_LINE, message=self.active_sprite.name + " does not move.")
                self.game_vars[SKIP_SEQUENCE] = False
                self.game_vars[GAME_STATE] = ATTACKING

            if self.game_vars[MOUSE_CLICKED]:

                # To ensure their are no double inputs on the first click
                self.game_vars[MOUSE_CLICKED] = False

                # Gets the board position of the mouse from the game_vars dict
                goal = (int((self.game_vars[RMOUSE_POS][0] - self.game_vars[BOARD_OFFSET][0]) / 80),
                        int((self.game_vars[RMOUSE_POS][1] - self.game_vars[BOARD_OFFSET][1]) / 80))
                if goal in self.game_vars[MOVABLE_LIST]:

                    if goal != self.active_sprite.pos:
                        make_event(PRINT_LINE, message=self.active_sprite.name + " moved to " + str(goal))
                    else:
                        make_event(PRINT_LINE, message=self.active_sprite.name + " stands in place.")

                    # Returns a list of tuples starting at the start,
                    # ending at the goal, that represents a path between them
                    self.path = Astar.a_star(self.active_sprite.pos, goal, self.grid)

                    self.vector_dic = {self.active_sprite.pos: (0, 0)}  # For paths of no distance
                    for i in range(len(self.path) - 1):  # Minus 1 ensures that we never get an IndexError
                        # Calculates the direction each sprite has to travel from the spots on the path
                        self.vector_dic[self.path[i]] = (self.path[i + 1][0] - self.path[i][0],
                                                         self.path[i + 1][1] - self.path[i][1])
                    if len(self.path) == 1:
                        self.game_vars[GAME_STATE] = ATTACKING  # Skips if players move to their own spot
                    else:
                        self.game_vars[GAME_STATE] = MOVING
                        self.Engine.Animator.set_animation(self.active_sprite, scripts.animations.run())
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    if tools.is_in_bounds(mouse_pos, (self.game_vars[BOARD_OFFSET][0],
                                                      self.game_vars[BOARD_OFFSET][1],
                                                      self.game_vars[TILE_SIZE]*8,
                                                      self.game_vars[TILE_SIZE]*8)):
                        if not self.Engine.GUI.is_mouse_on_gui():
                            banner = banners.Banner("That is not a valid spot, try again.")
                            make_event(BANNER, banner=banner)

        if self.game_vars[GAME_STATE] == MOVING:

            if self.active_sprite.ticked():
                # Gets the direction to go from its current spot and then adds a fifth of it for lifelike steps
                self.active_sprite.pos = (
                    self.active_sprite.pos[0] + self.vector_dic[self.path[self.path_index]][0] / 5,
                    self.active_sprite.pos[1] + self.vector_dic[self.path[self.path_index]][1] / 5
                )

                # This runs every time the sprite is about to change direction and adjusts their facing variable
                # 0: South(Down), 1: East(Right), 2: North(Up), 3: West(Left)

                if self.vector_dic[self.path[self.path_index]] == (-1, 0):
                    self.active_sprite.facing = 3
                elif self.vector_dic[self.path[self.path_index]] == (1, 0):
                    self.active_sprite.facing = 1
                elif self.vector_dic[self.path[self.path_index]] == (0, 1):
                    self.active_sprite.facing = 0
                elif self.vector_dic[self.path[self.path_index]] == (0, -1):
                    self.active_sprite.facing = 2

                # Round here to make sure numbers don't do strange float things
                self.active_sprite.pos = tools.tup_round(self.active_sprite.pos, 4)

                # Check if the sprite has reached the next spot in the path, if so, is it the last spot, then terminate,
                #  else increase path_index by 1, and repeat process
                if self.active_sprite.pos == self.path[self.path_index + 1]:

                    if self.path[-1] == self.path[self.path_index + 1]:
                        self.Engine.Animator.set_animation(self.active_sprite, scripts.animations.standby())

                        # Remove old player position from grid
                        self.grid.wpop(self.active_sprite.last_pos)
                        self.active_sprite.pos = (round(self.active_sprite.pos[0]), round(self.active_sprite.pos[1]))
                        # Add new player position to grid
                        self.grid.wpush(self.active_sprite.pos)
                        self.active_sprite.last_pos = self.active_sprite.pos
                        self.game_vars[GAME_STATE] = ATTACKING
                        self.path_index = 0
                    else:
                        self.path_index += 1

        if self.game_vars[GAME_STATE] == ATTACKING:
            if self.game_vars[SKIP_SEQUENCE] and not self.game_vars[TYPING] and not self.game_vars[PAUSE]:
                make_event(PRINT_LINE, message=self.active_sprite.name + " does not attack.")
                self.game_vars[GAME_STATE] = TURN_RESET
                self.game_vars[SKIP_SEQUENCE] = False

            if self.game_vars[MOUSE_CLICKED]:
                for sprite in self.game_vars[SPRITE_LIST]:
                    if sprite.pos == self.game_vars[ADJUSTED_RMOUSE_POS]:
                        if sprite != self.active_sprite:
                            sprite.face(self.active_sprite.pos)
                            # TODO: check if the target is in range for any of the players abilities, if so which ones?
                            if sprite.type == "monster" or self.game_vars[FRIENDLY_FIRE]:
                                make_event(PRINT_LINE, message=self.active_sprite.name + " attacks " + sprite.name)
                                make_event(FIGHT_EVENT, subtype=FIGHT_BEGIN, player=self.active_sprite, monster=sprite)
                                self.active_target = sprite
                                self.player = self.active_sprite
                                self.monster = self.active_target

                                self.game_vars[GAME_STATE] = IN_FIGHT
                                break
                        elif self.game_vars[FRIENDLY_FIRE]:
                            make_event(PRINT_LINE, message=self.active_sprite.name + " attacks themselves!")
                            make_event(FIGHT_EVENT, subtype=FIGHT_BEGIN, player=self.active_sprite)
                            self.active_target = sprite
                            self.player = self.active_sprite
                            self.monster = self.active_target

                            self.game_vars[GAME_STATE] = IN_FIGHT
                            break
                self.active_sprite.face(self.game_vars[ADJUSTED_RMOUSE_POS])

        if self.game_vars[GAME_STATE] == IN_FIGHT:
            pass

    def monster_loop(self):
        if self.game_vars[GAME_STATE] == PATHING:
            self.path = self.active_sprite.get_move(self.grid, self.PathManager)

            make_event(PRINT_LINE, message=self.active_sprite.name + " moves to " + str(self.path[-1]))

            self.vector_dic = {self.active_sprite.pos: (0, 0)}  # For paths of no distance
            for i in range(len(self.path) - 1):  # Minus 1 ensures that we never get an IndexError
                # Calculates the direction each sprite has to travel from the spots on the path
                self.vector_dic[self.path[i]] = (self.path[i + 1][0] - self.path[i][0],
                                                 self.path[i + 1][1] - self.path[i][1])
            if len(self.path) == 1:
                self.game_vars[GAME_STATE] = ATTACKING  # Skips if players move to their own spot
            else:
                self.game_vars[GAME_STATE] = MOVING
                self.Engine.Animator.set_animation(self.active_sprite, scripts.animations.run())

        if self.game_vars[GAME_STATE] == MOVING:
            if self.active_sprite.ticked():
                # Gets the direction to go from its current spot and then adds a fifth of it for lifelike steps
                self.active_sprite.pos = (
                    self.active_sprite.pos[0] + self.vector_dic[self.path[self.path_index]][0] / 5,
                    self.active_sprite.pos[1] + self.vector_dic[self.path[self.path_index]][1] / 5
                )

                # This runs every time the sprite is about to change direction and adjusts their facing variable
                # 0: South(Down), 1: East(Right), 2: North(Up), 3: West(Left)

                if self.vector_dic[self.path[self.path_index]] == (-1, 0):
                    self.active_sprite.facing = WEST
                elif self.vector_dic[self.path[self.path_index]] == (1, 0):
                    self.active_sprite.facing = EAST
                elif self.vector_dic[self.path[self.path_index]] == (0, 1):
                    self.active_sprite.facing = SOUTH
                elif self.vector_dic[self.path[self.path_index]] == (0, -1):
                    self.active_sprite.facing = NORTH

                # Round here to make sure numbers don't do strange float things
                self.active_sprite.pos = tools.tup_round(self.active_sprite.pos, 4)

                # Check if the sprite has reached the next spot in the path, if so, is it the last spot, then terminate,
                #  else increase path_index by 1, and repeat process
                if self.active_sprite.pos == self.path[self.path_index + 1]:

                    if self.path[-1] == self.path[self.path_index + 1]:
                        self.Engine.Animator.set_animation(self.active_sprite, scripts.animations.standby())
                        self.grid.wpop(self.active_sprite.last_pos)
                        self.active_sprite.pos = (round(self.active_sprite.pos[0]), round(self.active_sprite.pos[1]))
                        self.grid.wpush(self.active_sprite.pos)
                        self.active_sprite.last_pos = self.active_sprite.pos
                        self.game_vars[GAME_STATE] = ATTACKING
                        self.path_index = 0
                    else:
                        self.path_index += 1

        if self.game_vars[GAME_STATE] == ATTACKING:
            if self.active_sprite.get_target() is not None:
                self.active_target = self.active_sprite.get_target()
                self.player = self.active_target
                self.monster = self.active_sprite

                self.active_sprite.face(self.active_target.pos)
                self.active_target.face(self.active_sprite.pos)

                make_event(PRINT_LINE, message=self.active_sprite.name + " attacks " + self.active_target.name)
                make_event(FIGHT_EVENT, subtype=FIGHT_BEGIN, player=self.active_target, monster=self.active_sprite)

                self.game_vars[GAME_STATE] = IN_FIGHT
            else:
                make_event(PRINT_LINE, message=scripts.tools.gen_idle_text().format(self.active_sprite.name))
                self.game_vars[GAME_STATE] = TURN_RESET

        if self.game_vars[GAME_STATE] == IN_FIGHT:
            # GAME_STATE reset to TURN_RESET in FightManager
            pass

    def handle_event(self, event):
        if event.type == FIGHT_EVENT:
            self.FightManager.handle_event(event)

    def main_loop(self):

        if self.game_vars[QUIT_SEQUENCE]:
            pygame.quit()
            sys.exit()

        if not self.game_vars[PAUSE]:
            if self.game_vars[GAME_STATE] == TURN_RESET:
                self.game_vars[ACTIVE_SPRITE] = self.game_vars[SPRITE_LIST][self.sprite_counter]
                if not self.game_vars[ACTIVE_SPRITE].fightable:
                    self.sprite_counter = (self.sprite_counter + 1) % len(self.game_vars[SPRITE_LIST])
                    self.game_vars[GAME_STATE] = TURN_RESET
                    return
                self.active_sprite = self.game_vars[ACTIVE_SPRITE]
                self.sprite_counter = (self.sprite_counter + 1) % len(self.game_vars[SPRITE_LIST])
                self.movable_list = [self.active_sprite.pos]

                buf_list = []
                for i in range(self.active_sprite.speed):
                    for spot in self.movable_list:
                        for sub_spot in self.grid.neighbors(spot):
                            if sub_spot not in buf_list:
                                buf_list.append(sub_spot)
                    for neighboring_spot in buf_list:
                        if neighboring_spot not in self.movable_list:
                            self.movable_list.append(neighboring_spot)
                self.movable_list.remove(self.active_sprite.pos)
                self.game_vars[MOVABLE_LIST] = self.movable_list

                if self.movable_list:
                    self.game_vars[GAME_STATE] = PATHING
                else:
                    self.game_vars[GAME_STATE] = ATTACKING
                    make_event(PRINT_LINE, message=self.active_sprite.name + " can't go anywhere, they begin fighting.")

            if self.active_sprite.type == "player":
                self.player_loop()
            elif self.active_sprite.type == "monster":
                self.monster_loop()

    def get_active_sprite(self):
        return self.active_sprite

    def get_active_target(self):
        return self.active_target
