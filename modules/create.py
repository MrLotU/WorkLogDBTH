from modules import Module
from models import Entry
from utils import clear

class CreateModule(Module):
    def setup(self):
        clear()
        employee = input('Please enter the name of the employee that worked on the task\t')
        title = input('Give a name for the entry:\t')
        time = input('How many minutes did you spend on this entry:\t')
        notes = input('Please give any other notes:\n')
        try:
            int(time)
        except ValueError:
            print('Invalid time spent. Should be a number')
            self.setup()
        self.create_entry(employee=employee, title=title, time=time, notes=notes)
        print('Created entry')

    def create_entry(self, **kwargs):
        return Entry.create(**kwargs)