from datetime import datetime
from time import sleep

from models import Entry, Employee
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
        

    def get_search_date(self):
        date = input('Please give a date in the format MM/DD/YYYY\t')
        if date == 'TODAY':
            return datetime.utcnow().date()
        try:
            date = datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            print('Invalid date!')
            return self.get_search_date()
        return date.date()
    
    def get_employee_name(self):
        name = input('Please give name of the employee to search for\t')
        employees = Employee.find_by_name(name)
        employees = [employee for employee in employees]
        if employees == []:
            return None
        if len(employees) == 1:
            return employees[0].name
        print('We found multiple employees with that name. Please choose one from the list below (specify number)\n')
        inp = []
        for x, emp in enumerate(employees):
            inp.append('{}: {}'.format(x, emp.name))
        option = input('\n'.join(inp) + '\n')
        try:
            emp = employees[int(option)]
        except (KeyError, ValueError):
            print('Invalid option')
            sleep(1)
            return self.get_employee_name()
        return emp.name
        
    def get_time_spent(self):
        time = input('Please give a time spent in minutes\t')
        try:
            int(time)
        except ValueError:
            print('Invalid time spent. Should be a number')
            return self.get_time_spent()
        return time
    
    def get_search_term(self):
        term = input('Please provide a search term\t')
        return term

    def get_date_range(self):
        start = input('Please give a start date in format MM/DD/YYYY\t')
        end = input('Please give an end date in format MM/DD/YYYY\t')
        try:
            start = datetime.strptime(start, '%m/%d/%Y').date()
            end = datetime.strptime(end, '%m/%d/%Y').date()
        except ValueError:
            print('Invalid date(s) provided!')
            return self.get_date_range()
        return start, end