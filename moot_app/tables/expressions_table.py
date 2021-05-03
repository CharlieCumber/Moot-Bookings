from flask_table import Table, Col, LinkCol

class ExpressionsTable(Table):
    classes = ['table', 'table-striped']
    thead_classes = ['thead-dark']
    no_items = "No expressions to display"

    country = Col('country')
    participants = Col('participants')
    IST = Col('IST')
    CMT = Col('CMT')
    confirmation_sent = Col('confirmation_sent')
