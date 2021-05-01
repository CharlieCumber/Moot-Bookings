from flask_wtf import FlaskForm
from wtforms import Form, PasswordField
from wtforms.validators import DataRequired

class AdminLoginForm(FlaskForm):
    password = PasswordField(u'Admin Password', validators=[DataRequired()])
