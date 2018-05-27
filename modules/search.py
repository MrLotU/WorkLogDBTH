from datetime import datetime
from time import sleep

from models import Entry, Employee
from modules import Module
from utils import clear, finalize


class SearchModule(Module):
    """Search module"""
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

    def __init__(self, test=False):
        """Initializes Search module"""
        self.test = test

    def setup(self):
        """Setup SearchModule for use"""
        # Clear screen
        clear()
        # Get user input
        option = input(self.SEARCH_MENU)
        try:
            option = self.SEARCH_OPTIONS[int(option)]
        except ValueError:
            pass
        except KeyError:
            option = 'UNDEFINED'
        
        # Act upon user input
        option = option.upper()
        if option == 'Q':
            print('Returning to main menu')
            return None
        query = Entry.select()
        if option == 'C':
            date = self.get_search_date()
            return query.where(Entry.created_at == date).execute()
        elif option == 'A':
            employee = self.get_employee_name()
            return query.where(Entry.employee == employee).execute()
        elif option == 'T':
            time = self.get_time_spent()
            return query.where(Entry.time == time).execute()
        elif option == 'E':
            term = self.get_search_term()
            return query.where(
                (Entry.title.contains(term)) |
                (Entry.notes.contains(term))
            ).execute()
        elif option == 'D':
            start, end = self.get_date_range()
            return query.where(Entry.created_at.between(start, end))
        else:
            print('Undefined option. Restarting')
            sleep(1)
            self.setup()
        

    def get_search_date(self):
        """Get search date from user"""
        date = input('Please give a date in the format MM/DD/YYYY\t')
        if date == 'TODAY':
            return datetime.utcnow().date()
        try:
            date = datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            if self.test:
                raise ValueError
            print('Invalid date!')
            return self.get_search_date()
        return date.date()
    
    def get_employee_name(self):
        """Get employee name from user"""
        # Get imput
        name = input('Please give name of the employee to search for\t')
        employees = Employee.find_by_name(name)
        employees = [employee for employee in employees]
        if employees == []:
            return None
        if len(employees) == 1:
            # Return employee if we only got 1 match
            return employees[0].name
        # Let the user choose an employee if we found more than 1
        print('We found multiple employees with that name. Please choose one from the list below (specify number)\n')
        inp = []
        for x, emp in enumerate(employees):
            inp.append('{}: {}'.format(x, emp.name))
        option = input('\n'.join(inp) + '\n')
        # Validate input
        try:
            emp = employees[int(option)]
        except (IndexError, ValueError) as e:
            if self.test:
                raise e
            print('Invalid option')
            sleep(1)
            return self.get_employee_name()
        # Return employee
        return emp.name
        
    def get_time_spent(self):
        """Get time spent from user"""
        time = input('Please give a time spent in minutes\t')
        try:
            int(time)
        except ValueError:
            if self.test:
                raise ValueError
            print('Invalid time spent. Should be a number')
            return self.get_time_spent()
        return time
    
    def get_search_term(self):
        """Get search term from user"""
        term = input('Please provide a search term\t')
        return term

    def get_date_range(self):
        """Get date range from user"""
        start = input('Please give a start date in format MM/DD/YYYY\t')
        end = input('Please give an end date in format MM/DD/YYYY\t')
        try:
            if start != 'TODAY':
                start = datetime.strptime(start, '%m/%d/%Y').date()
            if end != 'TODAY':
                end = datetime.strptime(end, '%m/%d/%Y').date()
        except ValueError:
            if self.test:
                raise ValueError
            print('Invalid date(s) provided!')
            return self.get_date_range()
        if end == 'TODAY':
            end = datetime.utcnow().date()

        return start, end