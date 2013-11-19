#-*- encoding:utf-8 -*-
import sqlite3
db_path = '' # The database file

conn = sqlite3.connect(db_path)
res = conn.execute('select id, lower(affinities) from demons')
for r in res:
    affs = r[1].split('|')
    for a in affs:
        assoc = a.split(':')
        type_aff = assoc[0]
        els = assoc[1].split('/') #Elements
        for el in els:
            print u"%s %s:%s" % (str(r[0]).encode('utf-8'), type_aff, el)
            id_demon, affinity = str(r[0]).encode('utf-8'), u"%s:%s" % (type_aff, el)
            conn.execute('insert into affinities values (?, ?)', (id_demon, affinity))
conn.commit()
conn.close()
