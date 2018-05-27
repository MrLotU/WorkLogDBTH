from models.db import BaseModel
from peewee import TextField, CharField, IntegerField, DateTimeField
from datetime import datetime

@BaseModel.register
class Entry(BaseModel):
    title = CharField()
    employee = CharField()
    time_spent = IntegerField
    notes = TextField()
    created_at = DateTimeField(default=datetime.utcnow())

    class Meta:
        db_table = 'entries'