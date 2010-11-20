#!/usr/bin/env python

import Task
# Create a Task to use in unit testing
# Note that <module_name>.<class_name>(args) is used

myTask = Task.Task(['','','','','','','','',''])


import unittest
class TaskTestCase(unittest.TestCase):
    def test_exists(self):
        self.assert_(myTask)
    def test_category(self):
        # Normal test
        myTask.set_category('10')
        self.assertEquals(myTask.get_category(), '10')
        # Filter out non-decimal characters
        myTask.set_category('!@#$%^&*()_-+="\'-1234<>,.?/~`|')
        self.assertEquals(myTask.get_category(), '1234')
    def test_priority(self):
        # Normal test
        myTask.set_priority('11')
        self.assertEquals(myTask.get_priority(), '11')
        # Filter out non-decimal characters
        myTask.set_priority('!@#$%^&*()_-+="\'-2345<>,.?/~`|')
        self.assertEquals(myTask.get_priority(), '2345')
    def test_min_minutes(self):
        # Normal test
        myTask.set_min_minutes('12')
        self.assertEquals(myTask.get_min_minutes(), '12')
        # Filter out non-decimal characters
        myTask.set_min_minutes('!@#$%^&*()_-+="\'-3456<>,.?/~`|')
        self.assertEquals(myTask.get_min_minutes(), '3456')
    def test_max_minutes(self):
        # Normal test
        myTask.set_max_minutes('13')
        self.assertEquals(myTask.get_max_minutes(), '13')
        # Filter out non-decimal characters
        myTask.set_max_minutes('!@#$%^&*()_-+="\'-4567<>,.?/~`|')
        self.assertEquals(myTask.get_max_minutes(), '4567')
    def test_doors_open_time(self):
        # Normal test
        myTask.set_doors_open_time('1')
        self.assertEquals(myTask.get_doors_open_time(), '01:00:00')
        # Funky test
        myTask.set_doors_open_time('_)(*&^^2')
        self.assertEquals(myTask.get_doors_open_time(), '02:00:00')
        # Funky test 2
        myTask.set_doors_open_time('_)(_)_)(*&^12:35_)(*&')
        self.assertEquals(myTask.get_doors_open_time(), '12:35:00')
        # Funky test 3 -- alpha chars not recognized
        myTask.set_doors_open_time('alpha')
        self.assertEquals(myTask.get_doors_open_time(), 'NULL')
    def test_doors_close_time(self):
        # Normal test
        myTask.set_doors_close_time('3')
        self.assertEquals(myTask.get_doors_close_time(), '03:00:00')
        # Funky test
        myTask.set_doors_close_time('_)(*&^^4')
        self.assertEquals(myTask.get_doors_close_time(), '04:00:00')
        # Funky test 2
        myTask.set_doors_close_time('_)(_)_)(*&^05:27_)(*&')
        self.assertEquals(myTask.get_doors_close_time(), '05:27:00')
        # Funky test 3 -- alpha chars not recognized
        myTask.set_doors_close_time('bravo')
        self.assertEquals(myTask.get_doors_close_time(), 'NULL')
    def test_do_at_exactly_time(self):
        # Normal test
        myTask.set_do_at_exactly_time('5')
        self.assertEquals(myTask.get_do_at_exactly_time(), '05:00:00')
        # Funky test
        myTask.set_do_at_exactly_time('_)(*&^^6')
        self.assertEquals(myTask.get_do_at_exactly_time(), '06:00:00')
        # Funky test 2
        myTask.set_do_at_exactly_time('_)(_)_)(*&^23:18_)(*&')
        self.assertEquals(myTask.get_do_at_exactly_time(), '23:18:00')
        # Funky test 3 -- alpha chars not recognized
        myTask.set_do_at_exactly_time('charlie')
        self.assertEquals(myTask.get_do_at_exactly_time(), 'NULL')
    def test_description(self):
        myTask.set_description('Spend quality time with Abigail')
        self.assertEquals(myTask.get_description(), \
        'Spend quality time with Abigail')
        # Test escape characters
        myTask.set_description('<br>High Fives For Everyone!!!</br>')
        self.assertEquals(myTask.get_description(), \
        '&lt;br&gt;High Fives For Everyone!!!&lt;/br&gt;')
    def test_seconds(self):
        # Normal test
        task = Task.Task(['1','2','3','4','5','6','7','8', '0'])
        self.assertEquals(task.get_seconds(), '0')
        task.set_seconds('13')
        self.assertEquals(task.get_seconds(), '13')
        # Filter out non-decimal characters
        task.set_seconds('!@#$%^&*()_-+="\'-45967<>,.?/~`|')
        self.assertEquals(task.get_seconds(), '45967')
        task.add_seconds('tty23yp')
        self.assertEquals(task.get_seconds(), '45990')
    def test_entire_creation(self):
        myTask = Task.Task(['1','2','3','4','5','6','7','8', '9'])
        self.assertEquals(myTask.get_category(), '1')
        self.assertEquals(myTask.get_priority(), '2')
        self.assertEquals(myTask.get_min_minutes(), '3')
        self.assertEquals(myTask.get_max_minutes(), '4')
        self.assertEquals(myTask.get_doors_open_time(), '05:00:00')
        self.assertEquals(myTask.get_doors_close_time(), '06:00:00')
        self.assertEquals(myTask.get_do_at_exactly_time(), '07:00:00')
        self.assertEquals(myTask.get_description(), '8')
        self.assertEquals(myTask.get_seconds(), '9')
    def test_funky_values(self):
        myTask = Task.Task(['1','2','$%','*&','*&','*&^%',')(*&^%%', '^%$#@!','9'])

if __name__ == '__main__':
    unittest.main()
