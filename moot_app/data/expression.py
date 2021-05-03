class Expression:
    def __init__(self, contact_first_name="", contact_last_name="", contact_position="", contact_email="", contact_phone="", country="", org_name="", participants="0", IST="0", CMT="0", confirmation_sent="", row_id=""):
        self.contact_first_name = contact_first_name
        self.contact_last_name = contact_last_name
        self.contact_position = contact_position
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.country = country
        self.org_name = org_name
        self.participants = participants
        self.IST = IST
        self.CMT = CMT
        self.confirmation_sent = confirmation_sent
        self.row_id = str(row_id)


    @classmethod
    def fromDictionary(cls, dict=None):
        if dict == None:
            return cls()
        return cls(
            dict['contact_first_name'],
            dict['contact_last_name'],
            dict['contact_position'],
            dict['contact_email'],
            dict['contact_phone'],
            dict['country'],
            dict['org_name'],
            dict['org_address'],
            dict['org_address_postcode'],
            dict['participants'],
            dict['IST'],
            dict['CMT'])

    @property
    def toSheetColumnDict(self):
        return {
            'Country': self.country,
            'Contact - First Name': self.contact_first_name,
            'Contact - Last Name': self.contact_last_name,
            'Contact - Position': self.contact_position,
            'Contact - Email': self.contact_email,
            'Contact - Phone': self.contact_phone,
            'Organisation - Name': self.org_name,
            'Participants': self.participants,
            'IST': self.IST,
            'CMT': self.CMT,
            }

    @property
    def contact_full_name(self):
        return f'{self.contact_first_name} {self.contact_last_name}'
