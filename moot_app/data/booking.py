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
