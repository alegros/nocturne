#-*- encoding:utf-8 -*-
#from __future__ import unicode_literals
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
#from queries import *
from conf import *
from compendium import Compendium
import memcache

app = Flask(__name__)
app.config.from_object(__name__)

#-------------------Routes--------------------
@app.route('/')
def comp():
    return render_template('index.html')

@app.route('/demonList', methods=['POST', 'GET'])
def show_demon():
    if request.method == 'GET':
        return render_template('demonForm.html', demons=g.cmp.long_names())
    elif request.metod == 'POST':
        name = request.form['demon']
        return render_template('demon.html', demons=g.cmp.get(name))

@app.route('/fusion', methods=['POST', 'GET'])
def fusion_result():
    if request.method == 'GET':
        return render_template('fusionForm.html', demons=g.cmp.long_names())
    elif request.method == 'POST':
        child = g.cmp.fuse(request.form['d1'], request.form['d2'])
        if child != None:
            return render_template('demon.html', demon=child)
        else:
            return u"Impossible fusion"

@app.route('/reverseFusion', methods=['POST', 'GET'])
def reverse_result():
    if request.method == 'GET':
        return render_template('reverseForm.html', demons=g.cmp.long_names())
    elif request.method == 'POST':
        args = (request.form['child'], request.form['parent1']) 
        parents_data = g.cmp.find_parents(*args)
        return render_template('reverseResult.html', parents=parents)

#@app.route('/specialFusion', methods=['POST'])
#def special_fusion():
#    """
#    fsn_type:
#    1 - Special sacrificial fusions
#    2 - Evolutions
#    3 - Fiends
#    """
#    child = query_db(SINGLE, (request.form['demon'],))[0]
#    if child['fs_type'] == 1:
#        data = query_db(SACRIFICIAL, (child['name'],))[0]
#        #TODO : Modifier le template et parser le résultat avec recipe_parser()
#        return render_template('specialFusion.html', data=data)
#    elif child['fs_type'] == 2:
#        #Add the LIKE '%' wild card around the parameter
#        data = query_db(EVOLUTION, ("%%%s%%" % child['name'],))[0]
#        #TODO : Modifier le template et parser le résultat avec evol_parser()
#        return render_template('evolFusion.html', data=data)
#    else: #fs_type==3
#        data = query_db(FIEND, (child['name'],))[0]
#        return render_template('fiendFusion.html', data=data)

#@app.route('/advancedSearchForm')
#def advancedSearchForm():
#    return render_template('advancedSearchForm.html', affinities=query_db(ALL_AFF))

#@app.route('/advancedSearchResult', methods=['POST'])
#def advancedSearchResult():
#    sql, args = parseAdvancedSearch(request.form)
#    data = query_db(sql, args)
#    demons = None
#    if len(data) > 0:
#        demons = data
#    return render_template('advancedSearchResult.html', sql=sql, args=args, demons=demons)


#@app.route('/user/<username>')
#def show_user_profile(username):
#    return u"Comptes utilisateurs non implémentés"
#    return u"User %s" % username

#@app.route('/changelog')
#def changeLog():
#    return render_template('changeLog.html')

#-------------------Code logic--------------------
def parseAdvancedSearch(formData):
    """Create an sql statement using the data of
    the advanced search form
    """
    sql = ADVANCED
    args = []
    affinities = []
#    selSkills = ['selPhysical', 'selFire', 'selIce', 'selElectricity', 'selForce',\
#                'selExpel', 'selDeath', 'selAlmighty', 'selCurse', 'selNerver', 'selMind']
    moreAffs = OR if formData['nbAffs'] == 'one' else AND
    if formData['race'] != u'':
        sql += AND + RACE
        args.append(formData['race'])
    if formData['minlv'] != u'':
        sql += AND + MINLV
        args.append(formData['minlv'])
    if formData['maxlv'] != u'':
        sql += AND + MAXLV
        args.append(formData['maxlv'])
    for aff in query_db(ALL_AFF):
        if str(aff) in formData.keys():
            affinities.append(aff)
    if len(affinities) > 0:
        sql += AND + '('
        i = 0
        for a in affinities:
            sql += AFF if i == 0 else moreAffs + AFF
            args.append("%%%s%%" % a)
            i += 1
        sql+= ')'
#    selectedSkills = [x for x in selSkills if x in formData.keys()]
    return sql, args

@app.context_processor
def utility_processor():
    # Ajoute les fonctions de formattage au contexte des templates
    tools = {}
    tools['len'] = len
    return tools

def build_cmp():
    '''Creates the compendium object'''
    g.db = connect_db()
    t_demons = query_db(\
            'select name, race, lv, stats, affinities, spell, cost, info, fs_type\
            from demons order by race, lv')
    t_fsn_race = query_db(\
            'select result, demon1, demon2 from fsn_race')
    t_fsn_ds = query_db(\
            'select demon, kagutsuhi, race from fsn_ds')
    t_fsn_evo = query_db(\
            'select e from fsn_evo')
    t_fsn_special = query_db(\
            'select demon, recipe from fsn_special')
    t_affinities = query_db(\
            'select name, affinity from affinities')
    return Compendium(t_demons, t_fsn_race, t_fsn_ds,\
                      t_fsn_evo, t_fsn_special, t_affinities)

def query_db(query, args=()):
    '''Execute a query on the sqlite database connection'''
    return g.db.execute(query, args).fetchall()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    if mc.get('cmp') == None:
        mc.set('cmp', build_cmp())
    g.cmp = mc.get('cmp')

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()