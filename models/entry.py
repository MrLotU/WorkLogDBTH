from models import BaseModel, Employee
from peewee import TextField, CharField, DateField
from datetime import datetime
from peewee import IntegrityError

@BaseModel.register
class Entry(BaseModel):
    title = CharField()
    employee = CharField()
    time = CharField()
    notes = TextField()
    created_at = DateField(default=datetime.utcnow().date())

    @classmethod
    def new(cls, title, employee, time, notes):
        try:
            emp = Employee.with_name(employee)
        except IntegrityError:
            emp = Employee.find_by_name(employee)[0]
        employee = emp.name
        return cls.create(title=title, employee=employee, time=time, notes=notes)

    class Meta:
        db_table = 'entries'
