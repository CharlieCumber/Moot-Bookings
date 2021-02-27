from flask import Flask, render_template, request, redirect, session

from moot_app.flask_config import Config
from moot_app.data.booking import Booking
from moot_app.forms.booking_form import BookingForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET', 'POST'])
def index():
    session.pop('booking', None)
    booking = Booking()
    form = BookingForm(obj=booking)
    if form.validate_on_submit():
        form.populate_obj(booking)
        session['booking'] = booking.__dict__
        return render_template('submit.html', form=form)
    return render_template('index.html', form=form)

@app.route('/edit', methods=['POST'])
def edit():
    booking = Booking.fromDictionary(session.get('booking', None))
    form = BookingForm(obj=booking)
    return render_template('index.html', form=form)

@app.route('/submit', methods=['POST'])
def submit():
    booking = Booking.fromDictionary(session.get('booking', None))
    form = BookingForm(obj=booking)
    if form.validate_on_submit():
        form.populate_obj(booking)
        # send booking to smartsheet
        return render_template('confirmation.html', booking=booking)
    return render_template('submit.html', form=form)

if __name__ == '__main__':
    app.run()
