from os import environ
from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from wtforms.validators import Optional
from flask_mobility import Mobility

from moot_app.flask_config import Config
from moot_app.data.booking import Booking
from moot_app.data.expression import Expression
from moot_app.forms.admin_login_form import AdminLoginForm
from moot_app.forms.booking_form import BookingForm
from moot_app.forms.expression_form import ExpressionForm
from moot_app.data import smartsheet, database, sendgrid
from moot_app.tables.early_bookings_table import EarlyBookingsTable
from moot_app.tables.expressions_table import ExpressionsTable

def early_bird_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if environ.get('EARLY_BIRD_OPEN') == "True":
            return f(*args, **kwargs)
        if 'ebpassword' in session and session['ebpassword'] == environ.get('LATE_EARLY_BIRD_PASSWORD'):
            return f(*args, **kwargs)
        return render_template('early_bird_closed.html')
    return decorated_function

def admin_rights_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'adminpassword' in session and session['adminpassword'] == environ.get('ADMIN_PASSWORD'):
            return f(*args, **kwargs)
        return redirect(url_for('admin_login', redirect_url=request.url))
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

    @app.route('/admin-login', methods=['GET', 'POST'])
    def admin_login():
        form = AdminLoginForm()
        redirect_url = request.args.get("redirect_url", '/form/edit')
        if form.validate_on_submit():
            session['adminpassword'] = form.password.data
            return redirect(redirect_url)
        return render_template('admin_login.html', form=form, redirect_url=redirect_url)

    @app.route('/early-bird-list')
    @admin_rights_required
    def early_bird_list():
        bookings = smartsheet.get_all_bookings()
        table = EarlyBookingsTable(bookings)
        return render_template('early_bird_list.html', table=table)

    @app.route('/early-bird-list/<row_id>/send-confirmation-email')
    @admin_rights_required
    def send_confirmation_email(row_id):
        booking = smartsheet.get_booking(row_id)
        sendgrid.send_early_bird_booking_confirmation(booking)
        smartsheet.set_booking_confirmation_sent_time(row_id)
        return redirect(url_for('early_bird_list'))

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

    @app.route('/early-bird/change')
    def change_early_bird_start():
        return render_template('early_bird_changes_start.html')

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


    @app.route('/expression-of-intrest')
    def expression_of_intrest_start():
        return render_template('expression_start.html')

    @app.route('/expression-of-intrest/form', methods=['GET','POST'])
    def expression_of_intrest_form():
        expression = Expression()
        form = ExpressionForm(obj=expression)
        if form.validate_on_submit():
            form.populate_obj(expression)
            smartsheet.create_expression(expression)
            sendgrid.send_expression_confirmation(expression)
            return render_template('expression_confirmation.html')
        return render_template('expression_form.html', form=form)

    @app.route('/expressions-list')
    @admin_rights_required
    def expressions_list():
        expressions = smartsheet.get_all_expressions()
        table = ExpressionsTable(expressions)
        return render_template('expressions_list.html', table=table)

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
