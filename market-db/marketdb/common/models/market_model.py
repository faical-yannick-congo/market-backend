import datetime
from ..core import db
import json
from bson import ObjectId

class Market(db.Document):
    created_at = db.StringField(default=str(datetime.datetime.utcnow()))
    updated_at = db.StringField(default=str(datetime.datetime.utcnow()))
    message = db.StringField(required=True)
    sender = db.StringField(required=True)
    day = db.StringField(required=True)
    country = db.StringField(required=True)
    city = db.StringField(required=True)
    possible_status = ["pulled", "pushing", "pushed"]
    status = db.StringField(default="pulled", choices=possible_status)

    def save(self, *args, **kwargs):
        self.updated_at = str(datetime.datetime.utcnow())
        return super(Market, self).save(*args, **kwargs)

    def info(self):
        data = {'updated-at':self.updated_at, 'id':str(self.id),
        'created_at':self.created_at, 'message':self.message, 'day':self.day,
        'city':self.city, 'country':self.country, 'status':self.status,
        'sender':self.sender}
        return data

    def to_json(self):
        data = self.info()
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
