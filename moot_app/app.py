from flask import Flask, render_template, request, redirect, session, url_for
from wtforms.validators import Optional

from moot_app.flask_config import Config
from moot_app.data.booking import Booking
from moot_app.forms.booking_form import BookingForm
from moot_app.data import smartsheet, database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/', methods=['GET'])
    def index():
        session.pop('booking', None)
        return render_template('index.html')

    @app.route('/form', methods=['GET', 'POST'])
    @app.route('/form/step/<int:step>', methods=['GET', 'POST'])
    def early_bird_form(step=1):
        booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
        form = BookingForm(obj=booking)
        if step == 1:
            form.org_name.validators = [Optional()]
            form.org_email.validators = [Optional()]
            form.org_address.validators = [Optional()]
            form.country.validators = [Optional()]
        if step <= 2:
            form.participants.validators = [Optional()]
        form.terms_acceptance.validators=[Optional()]
        if form.validate_on_submit():
            form.populate_obj(booking)
            session['booking'] = booking.__dict__
            if step == 3:
                return redirect(url_for('submit'))
            return redirect(url_for('early_bird_form', step=step+1))
        return render_template('early_bird_form.html', form=form, step=step)

    @app.route('/submit', methods=['GET','POST'])
    def submit():
        booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
        form = BookingForm(obj=booking)
        if form.validate_on_submit():
            form.populate_obj(booking)
            smartsheet.create_booking(booking)
            database.insert_booking(booking)
            return render_template('confirmation.html', booking=booking)
        return render_template('submit.html', form=form, booking=booking)

    @app.before_request
    def set_iframe_session_var():
        url_arg = request.args.get("iframeMode", 'not-set')
        if url_arg != 'not-set':
            session['iframeMode'] = (url_arg == "true")

    @app.errorhandler(500)
    def error(e):
        return render_template('error.html')

    @app.template_filter()
    def numberFormat(value):
        return format(int(value), ',d')

    if __name__ == '__main__':
        app.run()

    return app
