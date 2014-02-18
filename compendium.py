from string import join
from collections import OrderedDict
import sqlite3

class Compendium(object):
    def __init__(self):
        self.sqlinit()
        self.races = {}
        # We want the demons to stay in the order in which
        # they were selected : by race and level.
        self.demons = OrderedDict()
        self.rules = {}
        self.fiends = {}
        self.evolutions = []
        self.specials = {}
        self.affinities = {}
        # Affinities
        for aff in self.t_affinities:
            if aff[0] not in self.affinities:
                self.affinities[aff[0]] = []
            self.affinities[aff[0]].append(aff[1])
        # races and demons
        for row in self.t_demons:
            demon = Demon(row)
            self.demons[demon.name] = demon
            for aff in self.affinities[demon.name]:
                demon.add_affinity(aff)
            if demon.race not in self.races:
                self.races[demon.race] = []
            self.races[demon.race].append(demon)
        # Affinities is not needed anymore
        self.affinities = None
        # fusion rules
        for row in self.t_fsn_race:
            if row[0] not in self.rules:
                self.rules[row[0]] = []
            self.rules[row[0]].append([row[1], row[2]])
        # special fusions
        self.specials = {row[0]:row[1] for row in self.t_fsn_special}
        # Fiend fusions
        self.fiends = {fiend[0]:fiend for fiend in self.t_fsn_ds}
        # Evolutions
        self.evolutions = self.t_fsn_evo
        self.sqldestroy()
            
    def sqlinit(self):
        cnx = sqlite3.connect('nocturne.db')
        self.t_demons = cnx.execute('select name, race, lv, stats, affinities, spell, cost, info, fs_type from demons order by race, lv').fetchall()
        self.t_fsn_race = cnx.execute('select result, demon1, demon2 from fsn_race').fetchall()
        self.t_fsn_ds = cnx.execute('select demon, kagutsuhi, race from fsn_ds').fetchall()
        self.t_fsn_evo = cnx.execute('select e from fsn_evo').fetchall()
        self.t_fsn_special = cnx.execute('select demon, recipe from fsn_special').fetchall()
        self.t_affinities = cnx.execute('select name, affinity from affinities').fetchall()
        cnx.close()

    def sqldestroy(self):
        self.t_demons = None
        self.t_fsn_race = None
        self.t_fan_ds = None
        self.t_fsn_ds = None
        self.t_fsn_evo = None
        self.t_fsn_special = None
        self.t_affinities = None

    def fuse(self, x, y):
        '''Finds the child of x and y'''
        fused = None
        raceresult = None
        demonx = self.demons[x]
        demony = self.demons[y]
        average = (demonx.lv + demony.lv) / 2
        # Look for the resulting race
        for race in self.rules:
            for fusion in self.rules[race]:
                if (fusion[0]==demonx.race and fusion[1]==demony.race)\
                or (fusion[0]==demony.race and fusion[1]==demonx.race):
                    raceresult = race
        if raceresult == None:
            return None
        else:
            for demon in self.races[raceresult]:
                if demon.lv > average:
                    fused = demon
                    break
            return fused
        
    def find_parents(self, child, parent):
        return_data = None
        child = self.get(child)
        if child.fs_type == 1:
            return_data = self.myth_fusion(child.name)
        elif child.fs_type == 2:
            return_data = self.evolution(child.name)
        elif child.fs_type == 3:
            return_data = self.fiend_fusion(child.name)
        else:
            parents = []
            previousRankLv=0
            for demon in self.races[child.race]:
                if demon.lv == child.lv:
                    break
                previousRankLv = demon.lv
            rules = self.rules[child.race]
            for rule in rules:
                race1 = self.races[rule[0]]
                race2 = self.races[rule[1]]
                for x in race1:
                    for y in race2:
                        if ((parent != None and parent != '')
                            and x.name != parent
                            and y.name != parent):
                            continue
                        average = (x.lv + y.lv) / 2
                        if average < child.lv and average >= previousRankLv:
                            couple = (x.long_name(), y.long_name())
                            parents.append(couple)
                            break
            return_data = parents
        return return_data, child.fs_type

    def myth_fusion(self, child):
        child = self.get(child)
        return "Myth fusions for %s" % child.name
    
    def evolution(self, child):
        child = self.get(child)
        return "Evolutions for %s" % child.name

    def fiend_fusion(self, child):
        child = self.get(child)
        return "Fiend fusions for %s" % child.name

    '''Functions for retrieving data in the collections'''            
    def get_races(self):
        return self.races.keys()

    def names(self):
        ''' Returns names as : "Pixie"'''
        return self.demons.keys()

    def long_names(self):
        '''Returns tuples such as : ("Pixie", "Fairy Pixie")'''
        return [(d.name, '%s %s' % (d.race, d.name))
                for d in self.demons.values()]

    def full_names(self):
        '''Returns tuples such as : ("Pixie", "Fairy Pixie (Level 2, 2400 maccas)")'''
        return [(d.name, '%s %s (Level %s, %s maccas)' % (d.race, d.name, d.lv, d.cost))
                for d in self.demons.values()]

    def get(self, name):
        return self.demons[name]

class Demon(object):
    '''A class used exclusively by the Compendium class'''
    def __init__(self, row):
        self.name = row[0]
        self.race = row[1]
        self.lv = row[2]
        self.parse_stats(row[3])
        self.affinities= []
        self.spells = row[5]
        self.cost= row[6]
        self.info= row[7]
        self.fs_type= row[8]

    def add_affinity(self, aff):
        aff_split = aff.split(':')
        self.affinities.append('%s %s' % (aff_split[0], aff_split[1]))

    def parse_stats(self, stats):
        stats_split = stats.split('|')
        stats_dict = {}
        for stat in stats_split:
            key, value = stat.split(':')
            stats_dict[key] = value
        self.hp = stats_dict['hp']
        self.mp = stats_dict['mp']
        self.stg = stats_dict['str']
        self.vit = stats_dict['vit']
        self.agi = stats_dict['agi']
        self.lck = stats_dict['lck']
        self.mag = stats_dict['mag']

    def long_name(self):
        return '%s %s' % (self.race, self.name)

    def __str__(self):
        affinities = join(self.affinities, ', ')
        return '''
%s %s (level %s, %s maccas)

- Affinities -
%s

- Stats -
hp : %s  mp : %s
strength : %s
magic : %s
vitality : %s
agility : %s
luck : %s

- Spells -
%s


%s
''' % (self.race, self.name, self.lv, self.cost, affinities, self.hp, self.mp, self.stg, self.mag, self.vit, self.agi, self.lck, self.spells, self.info)
