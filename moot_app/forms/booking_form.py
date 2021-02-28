from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, NumberRange, Optional
from moot_app.data.countries import Countries

class BookingForm(FlaskForm):
    contact_first_name = StringField('First name')
    contact_last_name = StringField('Last name')
    contact_position = StringField('Role')
    contact_email = StringField('Email')
    contact_phone = StringField('Phone number')
    org_name = StringField('Organisation name')
    org_email = StringField('Organisation email')
    org_address = TextAreaField('Organisation address (including postal code)',)
    org_website = StringField('Organisation website')
    org_phone = StringField('Organisation phone number')
    country = SelectField(u'Country', choices=[("", "Select country")] + [(x['name'], x['name']) for x in Countries], validators=[DataRequired()])
    participants = IntegerField(u'Participants', validators=[DataRequired(), NumberRange(1, 500, "Enter a number from 1 to 500")])
