from flask_wtf import FlaskForm
from wtforms import SelectField,StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    id = StringField('ID',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class PatientSearchForm(FlaskForm):
    choices = [('Name','Name'),
    ('Age','Age'),
    ('Phone','Phone'),
    ('TCKN','TCKN'),
    ('Insurance','Insurance'),
    ('cur_complaint','Current Complaint'),
    ]
    select = SelectField('Filter Patients:',choices=choices)
    search = StringField('')
    submit = SubmitField('Filter')


class G_PharmacySearchForm(FlaskForm):
    c = [('name','Name'),
    ('location','Location'),
    ]
    select = RadioField('Search for Pharmacies' , choices = c)
    search = StringField('')
    submit = SubmitField('Search') 

class inventory_change_form(FlaskForm):
    sold = SubmitField('Sold a Drug')
    bought = SubmitField('Bought a Drug')