from models import Entry
from datetime import datetime
from time import sleep
from utils import clear
from modules import Module

class ViewModule(Module):
    """View module"""

    def __init__(self, entries, test=False):
        """Initalizes ViewModule"""
        self.index = 0
        self.entries = [entry for entry in entries] if not entries is None else None
        self.test = test
    
    VIEW_FORMAT = '''Viewing entries
==================
Press \033[4mN\033[0m for next entry
Press \033[4mP\033[0m for previous entry
Press \033[4mE\033[0m to edit entry
Press \033[4mQ\033[0m to return to main menu
==================
Title: {}
Employee: {}
Time spent: {}
Date created/edited: {}
Notes:
{}\n\n'''

    def load_entries(self):
        """Loads entries in ViewModule"""
        # Clear screen
        clear()
        # Handle if we don't have entries
        if self.entries is None:
            return
        if self.entries == []:
            print('No entries were found')
            sleep(1)
            return
        # Get user input
        entry = self.entries[self.index]
        action = input(self.VIEW_FORMAT.format(entry.title, entry.employee, entry.time, entry.created_at, entry.notes)).upper()

        # Act upon input
        if action == 'N':
            if self.index >= len(self.entries) - 1:
                if self.test:
                    raise IndexError
                print('Already viewing last entry')
                sleep(1)
            else:
                self.index += 1
            self.load_entries()
        elif action == 'P':
            if self.index == 0:
                if self.test:
                    raise IndexError
                print('Already viewing first entry')
                sleep(1)
            else:
                self.index -= 1
            self.load_entries()
        elif action == 'E':
            entry = self.entries[self.index]
            self.update_entry(entry)
        elif action == 'Q':
            print('Returning to main menu')
            sleep(1)
            return None
        else:
            print('Invalid option. Restarting')
            sleep(1)
            self.load_entries()
        
    def update_entry(self, entry):
        """Updates an entry"""
        # Clear screen
        clear()
        # Set updated time
        updates = { 'created_at': datetime.utcnow().date() }
        # Get and validate user input
        title = input(
            'Current title is: {}. If you want to edit, give a new title. Otherwise leave this empty\t'.format(
                entry.title
            )
        )
        if not title == '':
            updates['title'] = title
        employee = input(
            'Current employee name is: {}. If you want to edit, give a new employee name. Otherwise leave this empty\t'.format(
                entry.employee
            )
        )
        if not title == '':
            updates['employee'] = employee
        time = input(
            'Current time spent is: {}. If you want to edit, give a new time spent. Otherwise leave this empty\t'.format(
                entry.time
            )
        )
        if not time == '':
            try:
                int(time)
            except ValueError:
                if self.test:
                    raise ValueError
                print('Invalid time provided. Not changing the value')
            else:
                updates['time'] = time
        notes = input(
            'Current notes are: \n{}\nIf you want to edit, give new notes. Otherwise leave this empty\n'.format(
                entry.notes
            )
        )
        if not notes == '':
            updates['notes'] = notes
        # Update entry
        Entry.update(updates).where(Entry.id == entry.id).execute()
        print('Updated entry!')
        sleep(1)
