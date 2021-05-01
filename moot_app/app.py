from os import environ
from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from wtforms.validators import Optional
from flask_mobility import Mobility

from moot_app.flask_config import Config
from moot_app.data.booking import Booking
from moot_app.forms.booking_form import BookingForm
from moot_app.data import smartsheet, database

def early_bird_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if environ.get('EARLY_BIRD_OPEN') == "True":
            return f(*args, **kwargs)
        if 'ebpassword' in session and session['ebpassword'] == environ.get('LATE_EARLY_BIRD_PASSWORD'):
            return f(*args, **kwargs)
        return render_template('early_bird_closed.html')
    return decorated_function

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Mobility(app)

    @app.route('/', methods=['GET'])
    @early_bird_route
    def index():
        session.pop('booking', None)
        return render_template('index.html')

    @app.route('/form', methods=['GET', 'POST'])
    @app.route('/form/edit')
    @early_bird_route
    def early_bird_form():
        booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
        form = BookingForm(obj=booking)
        form.terms_acceptance.validators=[Optional()]
        if form.validate_on_submit():
            form.populate_obj(booking)
            session['booking'] = booking.__dict__
            return render_template('standard_booking_estimates.html', form=form, booking=booking)
        return render_template('early_bird_form.html', form=form)

    @app.route('/form/standard', methods=['GET', 'POST'])
    @early_bird_route
    def standard_estimates():
        booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
        form = BookingForm(obj=booking)
        form.terms_acceptance.validators=[Optional()]
        if form.validate_on_submit():
            form.populate_obj(booking)
            session['booking'] = booking.__dict__
            return render_template('submit.html', form=form, booking=booking)
        return render_template('standard_booking_estimates.html', form=form)

    @app.route('/submit', methods=['POST'])
    @early_bird_route
    def submit():
        booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
        form = BookingForm(obj=booking)
        if form.validate_on_submit():
            form.populate_obj(booking)
            smartsheet.create_booking(booking)
            ref = database.insert_booking(booking)
            return render_template('confirmation.html', booking=booking, ref=ref)
        return render_template('submit.html', form=form, booking=booking)

    @app.before_request
    def set_session_vars():
        iframe_url_arg = request.args.get("iframeMode", 'not-set')
        if iframe_url_arg != 'not-set':
            session['iframeMode'] = (iframe_url_arg == "true")

        password_url_arg = request.args.get("ebpassword", 'not-set')
        if password_url_arg != 'not-set':
            session['ebpassword'] = password_url_arg

    @app.errorhandler(500)
    def error(e):
        return render_template('error.html')

    @app.template_filter()
    def numberFormat(value):
        return format(int(value), ',d')

    if __name__ == '__main__':
        app.run()

    return app
