#-*- encoding:utf-8 -*-
#Common
SINGLE= 'select * from demons where upper(name)=upper(?)'
COUPLE= 'select * from demons where upper(name)=upper(?) or upper(name)=upper(?)'

ORDER_BY_LVL = 'select * from demons order by lv'
DEMONS_BY_RACE = 'select * from demons where upper(race)=upper(?) order by lv'
ALL_BY_RACE = 'select race, name, lv from demons group by race, name'

#Standard fusions
DEMONS_BINARY_FUSION= 'select * from demons where race=(select result from fsn_race where (upper(demon1)=upper(?) and upper(demon2)=upper(?)) or (upper(demon1)=upper(?) and upper(demon2)=upper(?))) and fs_type=0 order by lv'

#Reverse fusions
#argument obtenu par DEMONS_RACE
PARENT_RACE = 'select * from fsn_race where upper(result)=upper(?)'

#Special fusions
SACRIFICIAL = 'select * from fsn_special where upper(demon)=upper(?)'
EVOLUTION = "select * from fsn_evo where upper(e) like upper(?)"
FIEND = 'select * from fsn_ds where upper(demon)=upper(?)'

#Advanced search
ADVANCED = 'select * from demons where 1=1 '
AND = 'and '
OR = 'or '
MAXLV = 'lv <= ? '
MINLV = 'lv >= ? '
RACE = 'upper(race) = upper(?) '
SKILL = 'upper(spell) like upper(?) '
AFF = 'upper(affinities) like upper(?) '

#listAffinitiesDB()
ALL_AFF = 'select distinct affinity from affinities'
