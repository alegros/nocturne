drop schema if exists cos cascade;
create schema cos authorization noctcomp;

/*drop table if exists "cos".demons cascade;
drop table if exists "cos".skills cascade;
drop table if exists "cos".affinities cascade;
drop table if exists "cos".fsn_ds;
drop table if exists "cos".fsn_evo;
drop table if exists "cos".fsn_race;
drop table if exists "cos".fsn_special;
drop table if exists "cos".ds;
drop table if exists "cos".da;
drop table if exists "cos".skilltypes;
drop sequence if exists "cos".seq_demons;
drop sequence if exists "cos".seq_skills;
drop sequence if exists "cos".seq_affinities;
drop sequence if exists "cos".seq_skilltypes;*/

-- GAME DATA
create table "cos".demons (
	id int
	,name character varying(50)
	,race character varying(20)
	,lvl int
	,hp int
	,mp int
	,str int
	,mag int
	,vit int
	,agi int
	,lck int
	,cost int
	,info text
	,fs_type int
);
create table "cos".skills(id int, id_skilltype int, name character varying(50), mpcost int, hpcost int);
create table "cos".affinities(id int, afftype character varying(10), affel character varying(15));

-- PRM
create table "cos".skilltypes(id int, lib character varying(15));

-- RELATIONS
create table "cos".ds(id_demon int, id_skill int, lvl int);
create table "cos".da(id_demon int, id_aff int);

-- FUSIONS
create table "cos".fsn_ds (demon character varying(50), kagutsuhi character varying(100), race character varying(20));
create table "cos".fsn_evo (e character varying(200));
create table "cos".fsn_race (result character varying(20), demon1 character varying(20), demon2 character varying(20));
create table "cos".fsn_special (demon character varying(50), recipe character varying(200));

-- CONSTRAINTS
alter table "cos".demons add constraint pk_demons primary key (id);
alter table "cos".skills add constraint pk_skills primary key (id);
alter table "cos".skilltypes add constraint pk_skilltypes primary key (id);
alter table "cos".affinities add constraint pk_affinities primary key (id);
alter table "cos".skills add constraint fk_skills foreign key (id_skilltype) references "cos".skilltypes(id);
alter table "cos".ds add constraint fk_ds foreign key (id_demon) references "cos".skills(id);
alter table "cos".da add constraint fk_da foreign key (id_demon) references "cos".affinities(id);

-- SEQUENCES
create sequence "cos".seq_demons increment 1 start 1 minvalue 1;
create sequence "cos".seq_skills increment 1 start 1 minvalue 1;
create sequence "cos".seq_affinities increment 1 start 1 minvalue 1;
create sequence "cos".seq_skilltypes increment 1 start 1 minvalue 1;
alter table "cos".seq_demons owner to noctcomp;
alter table "cos".seq_skills owner to noctcomp;
alter table "cos".seq_affinities owner to noctcomp;
alter table "cos".seq_skilltypes owner to noctcomp;

-- skillTYPES
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Physical');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Fire');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Ice');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Force');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Electricity');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Expel');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Death');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Curse');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Mind');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Nerve');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Almighty');
insert into "cos".skilltypes values (nextval('cos.seq_skilltypes'), 'Passive');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Physical');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Fire');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Ice');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Force');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Electricity');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Expel');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Death');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Almighty');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Nerve');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Mind');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Weak', 'Curse');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Physical');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Fire');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Ice');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Force');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Electricity');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Expel');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Death');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Almighty');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Nerve');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Mind');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Resist', 'Curse');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Physical');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Fire');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Ice');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Force');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Electricity');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Expel');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Death');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Almighty');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Nerve');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Mind');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Null', 'Curse');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Physical');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Fire');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Ice');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Force');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Electricity');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Expel');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Death');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Almighty');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Nerve');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Mind');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Repel', 'Curse');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Physical');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Fire');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Ice');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Force');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Electricity');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Expel');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Death');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Almighty');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Nerve');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Mind');
insert into "cos".affinities values (nextval('cos.seq_affinities'), 'Drain', 'Curse');
