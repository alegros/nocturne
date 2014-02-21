from wtforms import Form, validators, StringField, IntegerField, SelectField

class SearchForm(Form):
    race = SelectField(u'Race')
    fire = SelectField(u'Fire')
    ice = SelectField(u'Ice')
    elec = SelectField(u'Electricity')
    force = SelectField(u'Force')
    death = SelectField(u'Death')
    expel = SelectField(u'Expel')
    ailments = SelectField(u'Ailments')
    mind = SelectField(u'Mind')
    phys = SelectField(u'Physical')
    nerve = SelectField(u'Nerve')
    curse = SelectField(u'Curse')
    magic = SelectField(u'Magic')
