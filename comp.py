#-*- encoding:utf-8 -*-
#from __future__ import unicode_literals
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from queries import *
from conf import *

app = Flask(__name__)
app.config.from_object(__name__)

#-------------------Routes--------------------
@app.route('/')
def comp():
    return render_template('index.html')

@app.route('/demonForm')
def demon_form():
    data = query_db(ALL_BY_RACE)
    return render_template('demonForm.html', demons=data)

@app.route('/demon', methods=['POST'])
def show_demon():
    demonname = request.form['demon']
    demon = query_db(SINGLE, (demonname,))[0]
    return render_template('demon.html', demon=demon)

@app.route('/fusionForm')
def fusion_form():
    data = query_db(ALL_BY_RACE)
    return render_template('fusionForm.html', demons=data)

@app.route('/fusionResult', methods=['POST'])
def fusion_result():
    fusres = fuse(request.form['d1'], request.form['d2'])
    if fusres is not None:
        return render_template('fusionResult.html', demon=fusres)
    return u"Fusion sans résultat"
            
@app.route('/reverseForm')
def reverse_form():
    data = query_db(ALL_BY_RACE)
    return render_template('reverseForm.html', demons=data)

@app.route('/reverseResult', methods=['POST'])
def reverse_result():
    childname = request.form['demon']
    parent1 = request.form['parent1']
    child = query_db(SINGLE, (childname,))[0]
    if child['fs_type'] != 0:
        #Code 307 ensures the redirection uses a post request
        return redirect(url_for('special_fusion'), code=307)
    parents = find_parents(childname, parent1)
    return render_template('reverseResult.html', parents=parents)

@app.route('/specialFusion', methods=['POST'])
def special_fusion():
    """
    fsn_type:
    1 - Special sacrificial fusions
    2 - Evolutions
    3 - Fiends
    """
    child = query_db(SINGLE, (request.form['demon'],))[0]
    if child['fs_type'] == 1:
        data = query_db(SACRIFICIAL, (child['name'],))[0]
        #TODO : Modifier le template et parser le résultat avec recipe_parser()
        return render_template('specialFusion.html', data=data)
    elif child['fs_type'] == 2:
        #Add the LIKE '%' wild card around the parameter
        data = query_db(EVOLUTION, ("%%%s%%" % child['name'],))[0]
        #TODO : Modifier le template et parser le résultat avec evol_parser()
        return render_template('evolFusion.html', data=data)
    else: #fs_type==3
        data = query_db(FIEND, (child['name'],))[0]
        return render_template('fiendFusion.html', data=data)

@app.route('/advancedSearchForm')
def advancedSearchForm():
    return render_template('advancedSearchForm.html', affinities=query_db(ALL_AFF))

@app.route('/advancedSearchResult', methods=['POST'])
def advancedSearchResult():
    sql, args = parseAdvancedSearch(request.form)
    data = query_db(sql, args)
    demons = None
    if len(data) > 0:
        demons = data
    return render_template('advancedSearchResult.html', sql=sql, args=args, demons=demons)


@app.route('/user/<username>')
def show_user_profile(username):
    return u"Comptes utilisateurs non implémentés"
    return u"User %s" % username

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

def fuse(d1, d2):
    """Finds the child of d1 and d2"""
    fused = None
    data = query_db(SINGLE, (d1,))
    r1, l1 = data[0]['race'], data[0]['lv']
    data = query_db(SINGLE, (d2,))
    r2, l2 = data[0]['race'], data[0]['lv']
    average = (l1+l2)/2
    data = query_db(DEMONS_BINARY_FUSION, (r1, r2, r2, r1))
    for demon in data:
        if demon['lv'] > average:
            fused = demon
            break
    return fused

def find_parents(child, parent1=""):
    """Returns a list of the child's parents couples. 
    If parent1 is not empty, only return couples that include parent1.

    Retrieves the level of the demon juste below the child in that family.
    Retrieve the list of race couples that fuse to the race of the child.
    Get a list of all demons for each parent race. Iterate over them to 
    test all couple combinations ; if their average level is <= to the child's
    and > to that of the demon preceding the child in their family then add
    the parents to the list of couples.

    Parameters :
        child - String, the child's name
        parent1 - String, the name of one of the parents to use as a filter
    """
    data = query_db(SINGLE, (child,))
    child = data[0]
    parents = []
    previousRankLv = 0 #Will be changed if child is not the lowest in his family
    data = query_db(DEMONS_BY_RACE, (child['race'],))
    for demon in data:
        if demon['lv'] == child['lv']:
            break
        previousRankLv = demon['lv']
    data = query_db(PARENT_RACE, (child['race'],))
    for couple in data:
        r1 = query_db(DEMONS_BY_RACE, (couple['demon1'],))
        r2 = query_db(DEMONS_BY_RACE, (couple['demon2'],))
        for d1 in r1:
            for d2 in r2:
                if parent1 != "" and d1['name'] != parent1 and d2['name'] != parent1:
                    continue
                av = average_lv(d1, d2)
                if av <= child['lv']\
                and av > previousRankLv:
                    couple = (d1, d2)
                    parents.append(couple)
                    break
    return parents

def average_lv(d1, d2):
    """Computes the average level of 2 demons"""
    return float(d1['lv'] + d2['lv']) / 2

def recipe_parser(recipe):
    """Parse the text in fsn_special.recipe
    to return all 3 demons as demon1, demon2 and sacrifice
    """
    pass

def evol_parser(evol):
    """Parse the text in fsn_evo.e """
    pass

def listAffinities():
    """Extract the list of possible affinities from demons.affinities"""
    return query_db(ALL_AFF)

#-------------------Formats--------------------
def demon_full_name(demon):
    return u"%s : %s (%d)" % (demon['race'], demon['name'], demon['lv'])

def affinity(aff):
    return aff.replace(':', ' ')

@app.context_processor
def utility_processor():
    #Ajoute les fonctions de formattage au contexte des templates
    tools = dict()
    tools['demon_full_name'] = demon_full_name
    tools['affinity'] = affinity
    return tools

#-------------------DB functions--------------------
def query_db(query, args=()):
    return g.db.execute(query, args).fetchall()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()
    g.db.row_factory = sqlite3.Row

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run()
