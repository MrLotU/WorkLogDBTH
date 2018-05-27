from modules import Module
from models import Entry
from utils import clear
from time import sleep

class CreateModule(Module):
    """Create module"""
    def __init__(self, test=False):
        """Initializes create module"""
        # Make CreateModule testable
        self.test = test

    def setup(self):
        """Setup CreateModule for use"""
        # Clear screen
        clear()
        # Get user input
        employee = input('Please enter the name of the employee that worked on the task\t')
        title = input('Give a name for the entry:\t')
        time = input('How many minutes did you spend on this entry:\t')
        notes = input('Please give any other notes:\n')
        # Validate input
        try:
            int(time)
        except ValueError:
            if self.test:
                raise ValueError
            print('Invalid time spent. Should be a number')
            sleep(1)
            self.setup()
        # Create entry
        self.create_entry(employee=employee, title=title, time=time, notes=notes)
        print('Created entry')

    def create_entry(self, **kwargs):
        """Creates new entry"""
        return Entry.new(**kwargs)