'''This class needs to be initialize with the result of the following
query on the nocturne.db sqlite3 database as shown in testcompendium.py

It contains all the data and operations required by web.py so that
all the fusion logic is encapsulated here.
'''
from string import join
from collections import OrderedDict

class Compendium(object):
    def __init__(self, t_demons, t_fsn_race, t_fsn_ds,\
                t_fsn_evo, t_fsn_special, t_affinities):

        self.races = {}
        # We want the demons to stay in the order in which
        # they were selected : by race and level.
        self.demons = OrderedDict() # t_demons
        self.rules = {} # t_fsn_race, fusion rules
        self.fiends = {} # t_fsn_ds, fiend fusions
        self.evolutions = [] # t_fsn_evo, evolutions
        self.specials = {} # t_fsn_special, special fusions
        self.affinities = {} # t_affinities, demons' affinities
        # Affinities
        for aff in t_affinities:
            if aff[0] not in self.affinities:
                self.affinities[aff[0]] = []
            self.affinities[aff[0]].append(aff[1])
        # races and demons
        for row in t_demons:
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
        for row in t_fsn_race:
            if row[0] not in self.rules:
                self.rules[row[0]] = []
            self.rules[row[0]].append([row[1], row[2]])
        # special fusions
        #for row in t_fsn_special:
        #    self.specials[row[0]] = row[1]
        self.specials = {row[0]:row[1] for row in t_fsn_special}
        # Fiend fusions
        #for fiend in t_fsn_ds:
        #    self.fiends[fiend[0]] = fiend
        self.fiends = {fiend[0]:fiend for fiend in t_fsn_ds}
        # Evolutions
        self.evolutions = t_fsn_evo
            

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
