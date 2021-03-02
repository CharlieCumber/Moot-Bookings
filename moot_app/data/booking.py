import math

from moot_app.data import smartsheet
from moot_app.data.countries import Countries

class Booking:
    def __init__(self, ip_address, contact_first_name="", contact_last_name="", contact_position="", contact_email="", contact_phone="", country="", org_name="", org_email="", org_address="", org_website="", org_phone="", participants=None):
        self.ip_address = ip_address
        self.contact_first_name = contact_first_name
        self.contact_last_name = contact_last_name
        self.contact_position = contact_position
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.country = country
        self.org_name = org_name
        self.org_email = org_email
        self.org_address = org_address
        self.org_website = org_website
        self.org_phone = org_phone
        self.participants = participants

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
            dict['org_email'],
            dict['org_address'],
            dict['org_website'],
            dict['org_phone'],
            dict['participants'])

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
            'Organisation - Email': self.org_email,
            'Organisation - Address': self.org_address,
            'Organisation - Website': self.org_website,
            'Organisation - Phone': self.org_phone,
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
        return self.participants * self.fee_per_participant

    @property
    def min_participants(self):
        if self.participants == 1:
            return 1
        return math.floor(self.participants*.9)

    @property
    def min_value(self):
        return self.min_participants*self.fee_per_participant
