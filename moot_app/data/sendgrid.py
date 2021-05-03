from os import environ
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_early_bird_booking_confirmation(booking):
    if environ.get('SENDGRID_OVERIDE') == 'True':
        to_email = environ.get('SENDGRID_OVERRIDE_RECIPIENT')
    else:
        to_email = booking.contact_email

    message = Mail(
        from_email='bookings@moot2021.ie',
        to_emails=to_email)
    message.dynamic_template_data = {
        "contact_first_name": booking.contact_first_name,
        "org_name": booking.org_name,
        "participants": booking.participants,
        "reference": booking.reference,
        "country": booking.country,
        "org_address": booking.org_address,
        "org_postcode": booking.org_address_postcode,
        "contact_full_name": booking.contact_full_name,
        "contact_position": booking.contact_position,
        "contact_email": booking.contact_email,
        "fee_category": booking.fee_category,
        "fee_per_participant": f"€ {booking.fee_per_participant}",
        "booking_value": f"€ {booking.booking_value}",
        "min_participants": booking.min_participants,
        "max_participants": booking.max_participants
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

def send_expression_confirmation(expression):
    if environ.get('SENDGRID_OVERIDE') == 'True':
        to_email = environ.get('SENDGRID_OVERRIDE_RECIPIENT')
    else:
        to_email = expression.contact_email

    message = Mail(
        from_email='bookings@moot2021.ie',
        to_emails=to_email)
    message.dynamic_template_data = {
        "contact_first_name": expression.contact_first_name,
        "org_name": expression.org_name,
        "participants": expression.participants,
        "IST": expression.IST,
        "CMT": expression.CMT,
        "country": expression.country,
        "contact_full_name": expression.contact_full_name,
        "contact_position": expression.contact_position,
        "contact_email": expression.contact_email,
    }
    message.template_id = 'd-bfe3dabe28004a9188685d14bb752b12'
    try:
        sg = SendGridAPIClient(environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
