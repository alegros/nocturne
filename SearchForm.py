from wtforms import Form, IntegerField

# Prefixes for dynamicaly created attributes
# to recognize them and properly lay out the form in the template
AFF_ATTR= 'affinity_'

class SearchForm(Form):
    level = IntegerField('Level')
    pass
