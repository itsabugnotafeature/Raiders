from scripts.variables.localvars import *
from scripts import animations


class FightManager:

    def __init__(self, system):
        self.attacker = None
        self.defender = None

        self.player = None
        self.monster = None

        self.GameLogic = system
        self.Engine = self.GameLogic.Engine

        self.turn_counter = 1

    def set_engine(self, engine):
        self.Engine = engine

    def handle_event(self, event):
        if event.subtype == FIGHT_BEGIN:
            self.player = event.player
            self.monster = event.monster

            self.attacker = self.GameLogic.get_active_sprite()
            self.defender = self.GameLogic.get_active_target()

            self.turn_counter = 1

        if event.subtype == ACTION:
            if self.player == self.attacker:
                self.player.use(event.num, self.monster, self.Engine)
                self.monster.use(self.turn_counter, self.player, self.Engine)
            else:
                self.monster.use(self.turn_counter, self.player, self.Engine)
                self.player.use(event.num, self.monster, self.Engine)

            if not self.player.fightable or not self.monster.fightable:
                make_event(FIGHT_EVENT, subtype=FIGHT_END)
                return

            self.turn_counter += 1

            if self.turn_counter > 3:
                make_event(FIGHT_EVENT, subtype=FIGHT_END)

        if event.subtype == FIGHT_END:
            self.Engine.game_vars[GAME_STATE] = TURN_RESET
            self.turn_counter = 1
            self.monster = None
            self.player = None
            self.attacker = None
            self.defender = None
