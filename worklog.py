import sys
import os
from time import sleep
from utils import clear, finalize
from models import init_db
from modules import CreateModule, ViewModule, SearchModule

MAIN_MENU = '''Worklog
==================
Please choose an option from the list below:
    1. \033[4mC\033[0mreate a new entry
    2. \033[4mS\033[0mearch an existing entry
    3. \033[4mQ\033[0muit the application
'''

OPTIONS = {
    1: 'C',
    2: 'S',
    3: 'Q'
}

def menu():
    """Displays the menu and redirects to underlaying options"""
    clear()
    ### Get desired option
    option = input(MAIN_MENU)
    try:
        option = OPTIONS[int(option)]
    except ValueError:
        pass
    except KeyError:
        option = 'UNDEFINED'

    if option.upper() == 'C':
        ### Create
        cm = CreateModule()
        cm.setup()
        sleep(1)
        menu()
    elif option.upper() == 'S':
        ### Search
        sm = SearchModule()
        entries = sm.setup()
        vm = ViewModule(entries)
        vm.load_entries()
        menu()
    elif option.upper() == 'Q':
        ### Quit
        finalize()
    else:
        ### Undefined option
        print('Undefined option. Restarting!')
        sleep(1)
        menu()

if __name__ == '__main__':
    init_db()
    ### Clean exits
    try:
        menu()
    except KeyboardInterrupt:
        finalize()
