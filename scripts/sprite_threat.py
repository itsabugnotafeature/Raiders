
class ThreatManager:

    def __init__(self, monster, threat_table={None: 0}):
        self.monster = monster
        self.threat_table = threat_table

    def do_threat_update(self, source, value):
        if source not in self.threat_table:
            self.threat_table[source] = value
        else:
            self.threat_table[source] = self.threat_table[source] + value

        if self.threat_table[source] > self.threat_table[self.monster.get_target()]:
            return source
        else:
            return self.get_target()

    def get_threat_table(self):
        return self.threat_table

    def get_target(self):
        self.threat_table_clean_up()

        target = list(self.threat_table.keys())[0]
        for source in self.threat_table.keys():
            if self.threat_table[source] > self.threat_table[target]:
                target = source
        return target

    def threat_table_clean_up(self):
        pop_list = []
        for source in self.threat_table.keys():
            if source is not None and not source.fightable:
                pop_list.append(source)
        for source in pop_list:
            self.threat_table.pop(source)
