from flask_table import Table, Col, LinkCol

class EarlyBookingsTable(Table):
    classes = ['table', 'table-striped']
    thead_classes = ['thead-dark']
    no_items = "No bookings to display"

    reference = Col('reference')
    ip_address = Col('ip_address')
    contact_first_name = Col('contact_first_name')
    contact_last_name = Col('contact_last_name')
    contact_position = Col('contact_position')
    contact_email = Col('contact_email')
    contact_phone = Col('contact_phone')
    country = Col('country')
    org_name = Col('org_name')
    org_address = Col('org_address')
    org_address_postcode = Col('org_address_postcode')
    participants = Col('participants')
    standard_participants = Col('standard_participants')
    standard_IST = Col('standard_IST')
    standard_CMT = Col('standard_CMT')
