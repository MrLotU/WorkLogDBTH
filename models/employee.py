from models import BaseModel
from peewee import CharField, IntegrityError

@BaseModel.register
class Employee(BaseModel):
    first = CharField()
    last = CharField(default='')

    @property
    def name(self):
        return self.first + ' ' + self.last

    @classmethod
    def with_name(cls, name):
        employees_with_name = cls.find_by_name(name)
        if len(employees_with_name) > 0:
            raise IntegrityError # User already exists
        if not ' ' in name:
            return cls.create(first=name)
        (first, last) = name.split(' ')
        return cls.create(first=first, last=last)

    @classmethod
    def find_by_name(cls, name):
        if not ' ' in name:
            first = name
            employees = Employee.select().where(
                (Employee.first == first)
            )
        else:
            first, last = name.split(' ')
            employees = Employee.select().where(
                (Employee.first == first) &
                (Employee.last == last)
            )
        return employees

    class Meta:
        db_table = 'employees'