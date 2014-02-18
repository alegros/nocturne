#-*- encoding:utf-8 -*-
#from __future__ import unicode_literals
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from conf import *
from compendium import Compendium
from SearchForm import SearchForm
import memcache

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def comp():
    return render_template('index.html')

@app.route('/demonList', methods=['POST', 'GET'])
def show_demon():
    if request.method == 'GET':
        return render_template('demonForm.html', demons=g.cmp.long_names())
    elif request.method == 'POST':
        name = request.form['demon']
        return render_template('demon.html', demon=g.cmp.get(name))

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
        recipes, fs_type = g.cmp.find_parents(request.form['child'], request.form['parent1'])
        return render_template('reverseResult.html', recipes=recipes, fs_type=fs_type)

@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    form.race.choices = [(x,x) for x in g.cmp.get_races()]
    if request.method == 'GET':
        print 'search get'
        return render_template('search.html', form=form)
    elif request.method == 'POST':
        searchform = SearchForm(request.form)
        results= None
        print 'SearchForm.race = ', searchform.race
        return render_template('searchResult.html', results=results)

@app.context_processor
def utility_processor():
    # Ajoute les fonctions de formattage au contexte des templates
    tools = {}
    tools['len'] = len
    return tools

@app.before_request
def before_request():
    # retrieves the Compendium object
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    # either creates it or get it from the cache
    if mc.get('cmp') == None:
        mc.set('cmp', Compendium())
    g.cmp = mc.get('cmp')

if __name__ == '__main__':
    app.run()
