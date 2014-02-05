import sqlite3
from compendium import Compendium

cnx = sqlite3.connect('nocturne.db')
t_demons = cnx.execute('select name, race, lv, stats, affinities, spell, cost, info, fs_type from demons order by race, lv').fetchall()
t_fsn_race = cnx.execute('select result, demon1, demon2 from fsn_race').fetchall()
t_fsn_ds = cnx.execute('select demon, kagutsuhi, race from fsn_ds').fetchall()
t_fsn_evo = cnx.execute('select e from fsn_evo').fetchall()
t_fsn_special = cnx.execute('select demon, recipe from fsn_special').fetchall()
t_affinities = cnx.execute('select name, affinity from affinities').fetchall()
compendium = Compendium(t_demons, t_fsn_race, t_fsn_ds, t_fsn_evo, t_fsn_special, t_affinities)
#print compendium.fuse('Angel', 'Oberon')
