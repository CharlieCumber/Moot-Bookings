from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, SelectField, IntegerField, BooleanField, validators
from wtforms.validators import DataRequired, InputRequired, NumberRange, Email, Optional
from moot_app.data.countries import Countries

class BookingForm(FlaskForm):
    contact_first_name = StringField(u'First name', validators=[DataRequired()])
    contact_last_name = StringField(u'Last name', validators=[DataRequired()])
    contact_position = StringField(u'Role', validators=[DataRequired()])
    contact_email = StringField(u'Email', validators=[DataRequired(), Email()])
    contact_phone = StringField(u'Phone number', validators=[Optional()])
    org_name = StringField(u'Organisation name', validators=[DataRequired()])
    org_address = TextAreaField(u'Organisation address', validators=[DataRequired()])
    org_address_postcode = StringField(u'Postal code', validators=[Optional()])
    country = SelectField(u'Country', choices=[("", "Select country")] + [(x['name'], x['name']) for x in Countries], validators=[DataRequired()])
    participants = IntegerField(u'Participants', validators=[DataRequired(), NumberRange(min=1, message="Enter a number from 1 to 500"), NumberRange(max=500, message="Bookings are limited to 500.")])
    standard_participants = IntegerField(u'Additional participants', validators=[Optional()])
    standard_IST = IntegerField(u'IST', validators=[Optional()])
    standard_CMT = IntegerField(u'CMT', validators=[Optional()])
    terms_acceptance = BooleanField(u'Terms and Conditions acceptance', validators=[InputRequired()])
