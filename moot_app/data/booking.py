from moot_app.data import smartsheet
from moot_app.data.countries import Countries

class Booking:
    def __init__(self, country="", participants=None):
        self.country = country
        self.participants = participants

    @classmethod
    def fromDictionary(cls, dict=None):
        if dict == None:
            return cls()
        return cls(dict['country'], dict['participants'])

    @property
    def toSheetColumnDict(self):
        return {'Country': self.country, 'Participants': self.participants}

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
