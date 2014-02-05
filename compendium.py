'''This class needs to be initialize with the result of the following
query on the nocturne.db sqlite3 database as shown in testcompendium.py

It contains all the data and operations required by comp.py so that
all the fusion logic is encapsulated here.
'''
from itertools import chain
class Compendium(object):
    def __init__(self, t_demons, t_fsn_race, t_fsn_ds,\
                t_fsn_evo, t_fsn_special, t_affinities):
        self.races = {}
        self.demons = {} # t_demons
        self.rules = {} # t_fsn_race, fusion rules
        self.fiends = [] # t_fsn_ds, fiend fusions
        self.evolutions = [] # t_fsn_evo, evolutions
        self.specials = [] # t_fsn_special, special fusions
        self.affinities = [] # t_affinities, demons' affinities
        
        # races and demons
        for row in t_demons:
            demon = {}
            demon['name'] = row[0]
            demon['race'] = row[1]
            demon['lv'] = row[2]
            demon['stats'] = row[3]
            demon['affinities'] = row[4]
            demon['spell'] = row[5]
            demon['cost'] = row[6]
            demon['info'] = row[7]
            demon['fs_type'] = row[8]
            if demon['race'] not in self.races:
                self.races[demon['race']] = []
            self.races[demon['race']].append(demon['name'])
            self.demons[demon['name']] = demon
        
        # rules
        for row in t_fsn_race:
            if row[0] not in self.rules:
                self.rules[row[0]] = []
            self.rules[row[0]].append([row[1], row[2]])
            
        self.fiends = t_fsn_ds
        self.evolutions = t_fsn_evo
        self.specials = t_fsn_special
        self.affinities = t_affinities

    def fuse(self, x, y):
        '''Finds the child of x and y'''
        fused = None
        raceresult = None
        average = (self.lv(x) + self.lv(y)) / 2
        # Look for the resulting race
        for race in self.rules:
            for fusion in self.rules[race]:
                if (fusion[0]==self.race(x) and fusion[1]==self.race(y))\
                or (fusion[0]==self.race(y) and fusion[1]==self.race(x)):
                    raceresult = race
        for demon in self.races[raceresult]:
            if self.demons[demon]['lv'] > average:
                fused = demon
                break
        return fused
        
    def find_parents(self, child, parent=None):
        '''Returns a list of the child's parents couples. 
        If parent is not empty, only return couples that include parent.
        '''
        child = self.demons[child]
        parents = []
        previousRankLv=0

        for demon in self.races[child['race']]:
            if self.lv(demon) == child['lv']:
                break
            previousRankLv = self.lv(demon)
        rules = self.rules[child['race']]
        for rule in rules:
            race1 = self.races[rule[0]]
            race2 = self.races[rule[1]]
            for x in race1:
                for y in race2:
                    if parent != None\
                    and self.demons[x]['name'] != parent\
                    and self.demons[y]['name'] != parent:
                        continue
                    average = (self.lv(x) + self.lv(y)) / 2
                    if average < child['lv'] and average >= previousRankLv:
                        couple = (x, y)
                        parents.append(couple)
                        break
        return parents
            
    def race(self, demon):
        '''Returns the demon's race. Demon must be a string'''
        return self.demons[demon]['race']
        
    def lv(self, demon):
        '''Returns the demon's level. Demon must be a string'''
        return self.demons[demon]['lv']
