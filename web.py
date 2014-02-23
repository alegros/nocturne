#-*- encoding:utf-8 -*-
#from __future__ import unicode_literals
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from conf import *
from compendium import Compendium
from SearchForm import SearchForm, AFF_ATTR
import memcache
from wtforms import SelectField

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
        return render_template('reverseForm.html', demons=g.cmp.long_names(), races=g.cmp.get_races())
    elif request.method == 'POST':
        if 'parentdemon' in request.form:
            recipes, fs_type = g.cmp.find_parents(request.form['child'], request.form['parentdemon'])
        else: #race
            recipes = g.cmp.find_parents_races(request.form['childrace'], request.form['parentrace'])
            return render_template('reverseRace.html', recipes=recipes)
        return render_template('reverseResult.html', recipes=recipes, fs_type=fs_type)

@app.route('/search', methods=['POST', 'GET'])
def search():
    # Only way to dynamicaly add attributes to a wtforms.Form
    class DynamicSearchForm(SearchForm):
        pass

    # Create form widgets attributes for DynamicSearchForm
    setattr(DynamicSearchForm, u'race', SelectField(u'Race'))
    for el in g.cmp.elements:
        setattr(DynamicSearchForm, AFF_ATTR+el, SelectField(el))

    # Now let's make an instance to use
    form = DynamicSearchForm(request.form)
    # Assign values to multiple choice widgets
    getattr(form, u'race').choices = [(x,x) for x in g.cmp.get_races()]
    for attribute in dir(form):
        if attribute.startswith(AFF_ATTR):
            getattr(form, attribute).choices = [(x,x) for x in g.cmp.affinities_set]

    if request.method == 'GET':
        metadata = searchform_metadata(form)
        return render_template('search.html', form=form, metadata=metadata)
    elif request.method == 'POST':
        # Process search and query the compendium here...
        results = ['Search processing not implemented.']
        return render_template('searchResult.html', results=results)

def searchform_metadata(form):
    '''Retrieve and organize dynamicaly created attributes in form.'''
    class SearchformMetadata(object):
        affinities = []
        def __init__(self, form):
            for attr in dir(form):
                if attr.startswith(AFF_ATTR):
                    self.affinities.append(attr)
    return SearchformMetadata(form)

@app.context_processor
def utility_processor():
    # Ajoute les fonctions de formattage au contexte des templates
    tools = {}
    tools['len'] = len
    tools['getattr'] = getattr
    return tools

@app.before_request
def before_request():
    # Connect to the cache
    mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    # retrieves the Compendium object
    # either creates it or get it from the cache
    if mc.get('cmp') == None:
        mc.set('cmp', Compendium(), 5)
    g.cmp = mc.get('cmp')

if __name__ == '__main__':
    app.run()
