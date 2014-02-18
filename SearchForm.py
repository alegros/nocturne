from wtforms import Form, validators, StringField, IntegerField, SelectField

class SearchForm(Form):
    race = SelectField('Raceoo')
