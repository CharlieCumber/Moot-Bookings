from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, NumberRange, Email, Optional
from moot_app.data.countries import Countries

class BookingForm(FlaskForm):
    contact_first_name = StringField('First name', validators=[DataRequired()])
    contact_last_name = StringField('Last name', validators=[DataRequired()])
    contact_position = StringField('Role', validators=[DataRequired()])
    contact_email = StringField('Email', validators=[DataRequired(), Email()])
    contact_phone = StringField('Phone number', validators=[Optional()])
    org_name = StringField('Organisation name', validators=[DataRequired()])
    org_email = StringField('Organisation email', validators=[Optional(), Email()])
    org_address = TextAreaField('Organisation address (including postal code)', validators=[DataRequired()])
    org_website = StringField('Organisation website', [Optional()])
    org_phone = StringField('Organisation phone number', [Optional()])
    country = SelectField(u'Country', choices=[("", "Select country")] + [(x['name'], x['name']) for x in Countries], validators=[DataRequired()])
    participants = IntegerField(u'Participants', validators=[DataRequired(), NumberRange(1, 500, "Enter a number from 1 to 500")])
