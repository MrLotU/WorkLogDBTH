import unittest
from unittest.mock import patch
from models import *
from modules import *
from peewee import IntegrityError

class TestCreationMethods(unittest.TestCase):
    def setUp(self):
        # Reset the DB so we know we're working with an empty one
        reset_db()

    def test_creation(self):
        ### Basic entry creation
        # Create new entry
        entry = Entry.new(title='SomeTitle', employee='John Appleseed', time='10', notes='')
        # Grab all entries in the DB
        entries = Entry.select()
        # Make sure only our previously created entry exists
        self.assertEqual(len(entries), 1)
        # Make sure the entry in the array and our entry match
        self.assertEqual(entries[0].title, 'SomeTitle')
        self.assertEqual(entries[0], entry)

        ### Employee tests
        employees = Employee.select()
        # Make sure only the employee created as part of above entry creation exists
        self.assertEqual(len(employees), 1)
        # Make sure the employees match
        self.assertEqual(employees[0].name, 'John Appleseed')

        # Test find_by_name and with_name methods
        john = employees[0]
        self.assertEqual(john.name, john.first + ' ' + john.last)
        self.assertEqual(len(Employee.find_by_name('John Appleseed')), 1)
        with self.assertRaises(IntegrityError):
            Employee.with_name('John Appleseed')
        
        create_module = CreateModule(test=True)
        mock_input = ['Kate Bell', 'Prepared BBQ', '10', 'Also prepared the salads']
        failing_input = ['Kate Bell', 'Prepared BBQ', 'not_a_number', 'Also prepared the salads']

        with patch('builtins.input', side_effect=mock_input):
            create_module.setup()
            self.assertEqual(len(Employee.select()), 2)
        with self.assertRaises(ValueError):
            with patch('builtins.input', side_effect=failing_input):
                create_module.setup()

class TestSearchModule(unittest.TestCase):
    def setUp(self):
        ### Setup the DB with some plug values we can test against
        reset_db()
        Entry.new(title='Title 1', employee='John Appleseed', time='10', notes='')
        Entry.new(title='Title 2', employee='Kate Bell', time='5', notes='No notes')
        Entry.new(title='Let the dogs out', employee='Kate Appleseed', time='5', notes='Bananas')
        Entry.new(title='Entry 4', employee='John Appleseed', time='9', notes='Some notes')

    def test_search(self):
        search_module = SearchModule(test=True)

        ### POSITIVE TESTS

        ### Date search tests
        inputs = ['C', 'TODAY'] # TODAY is a hack I built in so we don't have to change the program every other day :)
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(len(search_module.setup()), 4) # Should return all 4 entries we created earlier
        
        ### Employee search tests
        inputs = ['A', 'Kate', '0'] # The 0 is there because we have to chose one of the two kates available
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(len(search_module.setup()), 1) # Both kates had only 1 entries
        inputs = ['A', 'John'] # We only have one john
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(len(search_module.setup()), 2) # John has 2 entries
        
        ### Quit option
        inputs = ['Q']
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(search_module.setup(), None)
        
        ### Undefined option
        inputs = ['9', 'Q']
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(search_module.setup(), None)
        
        ### Time spent tests
        inputs = ['T', '10']
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(len(search_module.setup()), 1) # One post with 10 minutes of time spent
        inputs = ['T', '5']
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(len(search_module.setup()), 2) # Two posts with 5 minutes of time spent
        
        ### Exact search tests
        inputs = ['E', 'Title']
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(len(search_module.setup()), 2) # Two posts with Title in notes or title field
        inputs = ['E', 'Bananas']
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(len(search_module.setup()), 1) # One post with Bananas in notes of title field
        
        ### Date range search tests
        inputs = ['D', '01/01/2018', 'TODAY'] # Same today hack as used above
        with patch('builtins.input', side_effect=inputs):
            self.assertEqual(len(search_module.setup()), 4) # All posts are between 1/1/18 and today

        ### NEGATIVE TESTS

        ### Date search tests
        inputs = ['C', 'notADate']
        with self.assertRaises(ValueError):
            with patch('builtins.input', side_effect=inputs):
                search_module.setup() # Raises value error for wrong date
        
        ### Employee search tests
        inputs = ['A', 'Kate', '5']
        with self.assertRaises(IndexError):
            with patch('builtins.input', side_effect=inputs):
                search_module.setup() # Raises index error because we only have 2 kates to choose from
        
        ### Time spent tests
        inputs = ['T', 'notANumber']
        with self.assertRaises(ValueError):
            with patch('builtins.input', side_effect=inputs):
                search_module.setup() # Raises value error for not providing an int for time spent
                
        ### Date range search tests
        inputs = ['D', 'NotADate', 'TODAY'] # Same today hack as used above
        with self.assertRaises(ValueError):
            with patch('builtins.input', side_effect=inputs):
                search_module.setup() # Raises value error for wrong date

class TestViewModule(unittest.TestCase):
    def setUp(self):
        ### Setup the DB with some plug values we can test against
        reset_db()
        Entry.new(title='Title 1', employee='John Appleseed', time='10', notes='')
        Entry.new(title='Title 2', employee='Kate Bell', time='5', notes='No notes')
        Entry.new(title='Let the dogs out', employee='Kate Appleseed', time='5', notes='Bananas')
        Entry.new(title='Entry 4', employee='John Appleseed', time='9', notes='Some notes')

    def test_view(self):
        view_module = ViewModule(Entry.select(), test=True)

        inputs = ['N', 'N', 'N', 'N'] # Pressing next one time too many
        with self.assertRaises(IndexError):
            with patch('builtins.input', side_effect=inputs):
                view_module.load_entries()
        
        inputs = ['P', 'P', 'P', 'P'] # Pressing previous one time too many
        with self.assertRaises(IndexError):
            with patch('builtins.input', side_effect=inputs):
                view_module.load_entries()
        
        inputs = ['E', 'Edited title 1', '', '11', 'Edited notes'] # Editing
        with patch('builtins.input', side_effect=inputs):
            view_module.load_entries()
            edited_entry = Entry.select().where(Entry.title == 'Edited title 1').execute()
            self.assertIsNotNone(edited_entry)

        inputs = ['E', 'Edited title 1', '', 'notANumber', 'Edited notes'] # Editing
        with self.assertRaises(ValueError):
            with patch('builtins.input', side_effect=inputs):
                view_module.load_entries()
        
        inputs = ['Q'] # Quit & Invalid option
        with patch('builtins.input', side_effect=inputs):
            self.assertIsNone(view_module.load_entries())
        inputs = ['Z', 'Q']
        with patch('builtins.input', side_effect=inputs):
            self.assertIsNone(view_module.load_entries())



if __name__ == '__main__':
    unittest.main()