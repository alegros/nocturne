begin transaction;
drop table demons;
drop table skilltypes;
drop table skills;
drop table affinities;
drop table ds;
drop table da;
drop table fsn_evo;
drop table fsn_ds;
drop table fsn_race;
drop table fsn_special;
create table demons(
    id integer primary key
    ,name text
    ,race text
    ,lv integer
    ,cost integer
    ,info text
    ,fs_type integer
    ,hp integer
    ,mp integer
    ,str integer
    ,mag integer
    ,vit integer
    ,agi integer
    ,lck integer
);
create table skilltypes(
    id integer primary key
    ,lib text
);
create table skills(
    id integer primary key
    ,id_skilltype integer
    ,name text
    ,mpcost integer
    ,hpcost integer
    ,description text
    ,foreign key (id_skilltype) references skilltypes(id)
);
create table affinities(
    id integer primary key
    ,afftype text
    ,affel text
);
create table ds(
    id_demon integer
    ,id_skill integer
    ,lvl integer
    ,foreign key (id_demon) references demons(id)
    ,foreign key (id_skill) references skills(id)
);
create table da(
    id_demon integer
    ,id_aff integer
    ,foreign key (id_demon) references demons(id)
    ,foreign key (id_aff) references affinities(id)
);
create table fsn_ds(demon text, kagutsuhi text, race text);
create table fsn_evo(e text);
create table fsn_race(result text, demon1 text, demon2 text);
create table fsn_special(demon text, recipe text);
COMMIT;
