from scripts.variables.localvars import *


class FightManager:

    def __init__(self, system):
        self.attacker = None
        self.defender = None

        self.player = None
        self.monster = None

        self.GameLogic = system
        self.Engine = self.GameLogic.Engine

        self.turn_counter = 1

        self.AbilityAnalyzer = AbilityAnalyzer()

    def set_engine(self, engine):
        self.Engine = engine

    def handle_event(self, event):
        if event.subtype == FIGHT_BEGIN:
            self.player = event.player
            self.monster = event.monster

            self.attacker = self.GameLogic.get_active_sprite()
            self.defender = self.GameLogic.get_active_target()

            self.attacker.prepare_for_fight()
            self.defender.prepare_for_fight()

            self.turn_counter = 1

        if event.subtype == ACTION:

            self.attacker.prepare_for_turn()
            self.defender.prepare_for_turn()

            player_attack = self.player.get_attack(self.monster, event.num, self.GameLogic.grid)
            monster_attack = self.monster.get_attack(self.player, self.turn_counter, self.GameLogic.grid)

            print("FIGHT: {} used {}, {} used {}".format(self.player, player_attack, self.monster, monster_attack))

            player_outcome, monster_outcome = self.AbilityAnalyzer.get_outcome(self.player, player_attack,
                                                                               self.monster, monster_attack)

            # TODO: Is this redundant given that the results are calculated order agnostic in the AbilityAnalyzer?
            if self.attacker == self.player:
                self.player.use(player_attack, self.monster, player_outcome, self.Engine)
                self.monster.use(monster_attack, self.player, monster_outcome, self.Engine)
            else:
                self.monster.use(monster_attack, self.player, monster_outcome, self.Engine)
                self.player.use(player_attack, self.monster, player_outcome, self.Engine)

            if not self.player.fightable or not self.monster.fightable:
                make_event(FIGHT_EVENT, subtype=FIGHT_END)
                return

            self.turn_counter += 1

            if not self.can_continue(self.player, self.monster, self.Engine.Logic.grid):
                make_event(FIGHT_EVENT, subtype=FIGHT_END)

        if event.subtype == FIGHT_END:
            self.Engine.game_vars[GAME_STATE] = TURN_RESET
            self.turn_counter = 1
            self.monster = None
            self.player = None
            self.attacker = None
            self.defender = None

    def can_continue(self, player, monster, grid):
        if self.turn_counter > 3:
            return False
        if not self.player.can_make_attack(monster, grid) and not monster.can_make_attack(player, grid):
            print("FIGHT: Exiting early because {} and {} have no more available abilities.".format(self.player, self.monster))
            return False
        return True


class AbilityAnalyzer:

    def __init__(self):
        pass

    def get_outcome(self, player, player_ability, monster, monster_ability):
        """
        Generates a dict of possible results that the various scripts involved in the attacking process can use to
        decide what animations/sounds/attacks to do
        "blocked" signifies that the respective attack was blocked
        "blocking" signifies that the respective block successfully blocked an attack
        """

        player_outcome = {"blocked": False, "blocking": False, "counter": False, "death_blocked": False,
                          "opposite_ability": monster_ability, "out_of_range": False}
        monster_outcome = {"blocked": False, "blocking": False, "counter": False, "death_blocked": False,
                           "opposite_ability": player_ability, "out_of_range": False}

        if not player.fightable:
            player_outcome["death_blocked"] = True
        if monster_ability.type == "block":
            is_player_blocked = self.resolve_block(player_ability, monster_ability)
            player_outcome["blocked"] = is_player_blocked
            monster_outcome["blocking"] = is_player_blocked

        if not monster.fightable:
            monster_outcome["death_blocked"] = True
        if player_ability.type == "block":
            is_monster_blocked = self.resolve_block(monster_ability, player_ability)
            monster_outcome["blocked"] = is_monster_blocked
            player_outcome["blocking"] = is_monster_blocked

        return player_outcome, monster_outcome

    @staticmethod
    def resolve_block(base_ability, blocking_ability):
        if base_ability.type == blocking_ability.type:
            return False
        return blocking_ability.can_block(base_ability)
