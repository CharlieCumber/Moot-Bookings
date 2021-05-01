import math

from moot_app.data.countries import Countries

class Booking:
    def __init__(self, ip_address, contact_first_name="", contact_last_name="", contact_position="", contact_email="", contact_phone="", country="", org_name="", org_address="", org_address_postcode="", participants=None, standard_participants=None, standard_IST=None, standard_CMT=None):
        self.ip_address = ip_address
        self.contact_first_name = contact_first_name
        self.contact_last_name = contact_last_name
        self.contact_position = contact_position
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.country = country
        self.org_name = org_name
        self.org_address = org_address
        self.org_address_postcode = org_address_postcode
        self.participants = participants
        self.standard_participants = standard_participants
        self.standard_IST = standard_IST
        self.standard_CMT = standard_CMT


    @classmethod
    def fromDictionary(cls, ip_address, dict=None):
        if dict == None:
            return cls(ip_address)
        return cls(
            ip_address,
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
            dict['standard_participants'],
            dict['standard_IST'],
            dict['standard_CMT'])

    @property
    def toSheetColumnDict(self):
        return {
            'Country': self.country,
            'Participants': self.participants,
            'Contact - First Name': self.contact_first_name,
            'Contact - Last Name': self.contact_last_name,
            'Contact - Position': self.contact_position,
            'Contact - Email': self.contact_email,
            'Contact - Phone': self.contact_phone,
            'Organisation - Name': self.org_name,
            'Organisation - Address': self.org_address,
            'Organisation - Postcode': self.org_address_postcode,
            'Standard Participants Estimate': self.standard_participants,
            'Standard IST Estimate': self.standard_IST,
            'Standard CMT Estimate': self.standard_CMT,
            'IP Address': self.ip_address
            }

    @property
    def contact_full_name(self):
        return f'{self.contact_first_name} {self.contact_last_name}'

    @property
    def fee_category(self):
        return next((country['fee_category'] for country in Countries if country['name'] == self.country), None)

    @property
    def fee_per_participant(self):
        if self.fee_category == 'A':
            return 225
        if self.fee_category == 'B':
            return 450
        if self.fee_category == 'C':
            return 675
        return 900

    @property
    def booking_value(self):
        if self.participants == None:
            return 0
        return self.participants * self.fee_per_participant

    @property
    def min_participants(self):
        if self.participants == None:
            return 0
        if self.participants == 1:
            return 1
        return math.floor(self.participants*.9)

    @property
    def max_participants(self):
        if self.participants == None:
            return 0
        if self.participants >= 454:
            return 500
        return math.ceil(self.participants*1.1)

    @property
    def min_value(self):
        return self.min_participants*self.fee_per_participant
