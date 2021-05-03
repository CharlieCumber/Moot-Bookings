from flask_table import Table, Col, LinkCol

class EarlyBookingsTable(Table):
    classes = ['table', 'table-striped']
    thead_classes = ['thead-dark']
    no_items = "No bookings to display"

    reference = Col('reference')
    country = Col('country')
    participants = Col('participants')
    fee_category = Col('category')
    fee_per_participant = Col('Fee')
    booking_value = Col('Value')
    min_participants = Col('Min participants')
    max_participants = Col('Max participants')
    confirmation_sent = Col('confirmation_sent')
    send_confirmation = LinkCol('Send Confimation', 'send_confirmation_email', url_kwargs=dict(row_id='row_id'), anchor_attrs={'class': 'btn btn-danger btn-sm'})
