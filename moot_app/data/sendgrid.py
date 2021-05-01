from os import environ
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_early_bird_booking_confirmation():
    message = Mail(
        from_email='bookings@moot2021.ie',
        to_emails='charlie.cumber@softwire.com')
    message.dynamic_template_data = {
        "contact_first_name": "booking.contact_first_name",
        "org_name": "booking.org_name",
        "participants": "booking.participants",
        "reference": "booking.reference_number",
        "country": "booking.country",
        "org_address": "booking.org_address",
        "org_postcode": "booking.org_address_postcode",
        "contact_full_name": "booking.contact_full_name",
        "contact_position": "booking.contact_position",
        "contact_email": "booking.contact_email",
        "fee_category": "booking.fee_category",
        "fee_per_participant": "€ booking.fee_per_participant",
        "booking_value": "€ booking.booking_value",
        "min_participants": "booking.min_participants",
        "max_participants": "booking.max_participants"
    }
    message.template_id = 'd-0e4a746abc104424aad1abd0c84fa3b3'
    try:
        sg = SendGridAPIClient(environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
