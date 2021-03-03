from flask import Flask, render_template, request, redirect, session
from wtforms.validators import Optional

from moot_app.flask_config import Config
from moot_app.data.booking import Booking
from moot_app.forms.booking_form import BookingForm
from moot_app.data import smartsheet

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/', methods=['GET'])
    def index():
        session.pop('booking', None)
        return render_template('index.html')

    @app.route('/form', methods=['GET', 'POST'])
    def early_bird_form():
        booking = Booking(request.remote_addr)
        form = BookingForm(obj=booking)
        form.terms_acceptance.validators=[Optional()]
        if form.validate_on_submit():
            form.populate_obj(booking)
            session['booking'] = booking.__dict__
            return render_template('submit.html', form=form, booking=booking)
        return render_template('early_bird_form.html', form=form)

    @app.route('/edit')
    def edit():
        booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
        form = BookingForm(obj=booking)
        return render_template('early_bird_form.html', form=form)

    @app.route('/submit', methods=['POST'])
    def submit():
        booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
        form = BookingForm(obj=booking)
        if form.validate_on_submit():
            form.populate_obj(booking)
            response = smartsheet.create_booking(booking)
            return render_template('confirmation.html', booking=booking)
        return render_template('submit.html', form=form, booking=booking)

    @app.errorhandler(500)
    def error(e):
        return render_template('error.html')

    @app.template_filter()
    def numberFormat(value):
        return format(int(value), ',d')

    if __name__ == '__main__':
        app.run()

    return app
