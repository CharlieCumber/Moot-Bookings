from flask import Flask, render_template, request, redirect, session
import smartsheet

from moot_app.flask_config import Config
from moot_app.data.booking import Booking
from moot_app.forms.booking_form import BookingForm
from moot_app.data import smartsheet

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET', 'POST'])
def index():
    session.pop('booking', None)
    booking = Booking(request.remote_addr)
    form = BookingForm(obj=booking)
    if form.validate_on_submit():
        form.populate_obj(booking)
        session['booking'] = booking.__dict__
        return render_template('submit.html', form=form)
    return render_template('index.html', form=form)

@app.route('/edit', methods=['POST'])
def edit():
    booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
    form = BookingForm(obj=booking)
    return render_template('index.html', form=form)

@app.route('/submit', methods=['POST'])
def submit():
    booking = Booking.fromDictionary(request.remote_addr, session.get('booking', None))
    form = BookingForm(obj=booking)
    if form.validate_on_submit():
        form.populate_obj(booking)
        response = smartsheet.create_booking(booking)
        return render_template('confirmation.html', booking=booking)
    return render_template('submit.html', form=form)

@app.errorhandler(500)
def error(e):
    return render_template('error.html')

if __name__ == '__main__':
    app.run()
