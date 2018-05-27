from models import BaseModel
from peewee import CharField

@BaseModel.register
class Employee(BaseModel):
    first = CharField()
    last = CharField(default='')

    @property
    def name(self):
        return self.first + ' ' + self.last

    @classmethod
    def with_name(cls, name):
        if not ' ' in name:
            return cls.create(first=name)
        (first, last) = name.split(' ')
        return cls.create(first=first, last=last)

    @classmethod
    def find_by_name(cls, name):
        form = '{}'
        for emp in Employee.select():
            print(emp.name)
            print(form.format(emp.name).lower())
        employees = Employee.select().where(
            (Employee.first.contains(name)) |
            (Employee.last.contains(name))
        )
        return employees

    class Meta:
        db_table = 'employees'