from wtforms import Form, SelectField, IntegerField

# Prefixes for dynamicaly created attributes
# to recognize them and properly lay out the form in the template
AFF_ATTR= 'affinity_'

class SearchForm(Form):
    level = IntegerField('Level')
    pass

#def search_form(elements):
#    class SearchForm(BaseForm):
#        pass
#
#    setattr(SearchForm, u'race', SelectField(u'Race'))
#    for el in elements:
#        setattr(SearchForm, AFF_ATTR+el, SelectField(el))
#
#    return SearchForm()
#
#def init_search_form(form, affinities, races):
#    getattr(form, u'race').choices = [(x,x) for x in races]
#    for attr in dir(form):
#        if attr.startswith(AFF_ATTR):
#            getattr(form, attr).choices = [(x,x) for x in affinities]
