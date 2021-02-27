from flask_wtf import FlaskForm
from wtforms import Form, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, NumberRange, Optional
from moot_app.forms.countries import Countries

class BookingForm(FlaskForm):
    country = SelectField(u'Country', choices=[("", "Select country")] + [(x, x) for x in Countries], validators=[DataRequired()])
    participants = IntegerField(u'Participants', validators=[DataRequired(), NumberRange(1, 500, "Enter a number from 1 to 500")])
