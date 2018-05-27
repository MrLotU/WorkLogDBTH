from datetime import datetime
from time import sleep

from models import Entry
from modules import Module
from utils import clear, finalize


class SearchModule(Module):
    SEARCH_MENU = '''Search
==================
Please choose a search option from the list below:
    1. \033[4mC\033[0mreation date
    2. \033[4mA\033[0mssigned employee
    3. \033[4mT\033[0mime Spent
    4. \033[4mE\033[0mxact search
    5. \033[4mD\033[0mate range
Or press \033[4mQ\033[0m to go back to the main menu]\n\n'''

    SEARCH_OPTIONS = {
        1: 'C',
        2: 'A',
        3: 'T',
        4: 'E',
        5: 'D'
    }

    def setup(self):
        clear()
        option = input(self.SEARCH_MENU)
        try:
            option = self.SEARCH_OPTIONS[int(option)]
        except ValueError:
            pass
        except KeyError:
            option = 'UNDEFINED'
        
        option = option.upper()
        if option == 'Q':
            print('Returning to main menu')
            return None
        query = Entry.select()
        if option == 'C':
            date = self.get_search_date()
            return query.where(Entry.created_at == date).execute()
        

    def get_search_date(self):
        date = input('Please give a date in the format MM/DD/YYYY\t')
        ### Validate user input
        try:
            date = datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            print('Invalid date!')
            return self.get_search_date()
        return date