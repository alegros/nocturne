class Demon():
    """ Represents a demon with its data retrieved from the database"""
    def __init__(self, row=None):
        if row is not None:
            self.from_db_row(self, row)

    def from_db_row(self, row):
        """ Uses an sqlite3.Row to fill the Demon object"""
        self.name = row['name']
        self.race = row['race']
        self.lv = row['lv']
        self.cost = row['cost']
        self.stats = {}
        for stat in row['stats'].split('|'):
            key, value = stat.split(':')
            self.stats[key] = value
        self.affs = []
        self.affs = [aff for aff in row['affinities'].split('|')]
        self.affs.sort()
        self.spells = []
        self.spells = [s for s in row['spell'].split(', ')]
        self.info = row['info']
