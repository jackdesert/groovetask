#!/usr/bin/env python

import Task
import Menu
import Key
from fancy_functions import pr
# Create a Task to use in unit testing
# Note that <module_name>.<class_name>(args) is used
myTask = Task.Task(['1','2','3','4','5','6','7','8', '9'])
myTask2 = Task.Task(['1','20','','','','','','',''])
myMenu = Menu.Menu(900)


import unittest
class MenuTestCase(unittest.TestCase):
    def test_00_task_exists(self):
        self.assert_(myTask)
    def test_01_menu_exists(self):
        self.assert_(myMenu)
    def test_02_table_is_empty(self):
        myMenu.reset_table()
        self.assertEquals(myMenu.get_tasks(0), [])
        self.assertEquals(myTask, myTask)
        myMenu.insert_task(myTask)  # Insert once
        self.compare_tasks(myTask, myMenu.get_tasks(0)[0])
        self.assertEquals(myTask, myTask)
        myMenu.insert_task(myTask2) # Insert a different task
    def test_03_funky_values(self):     # Note apostrophe in description
        myTask = Task.Task(['1','2','$%','*&','*&','*&^%',')(*&^%%', "'^%$#'@!", '9'])
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myMenu.insert_task(myTask)
        myTask2 = Task.Task(['1','2','','','','','',"'^%$#'@!", '9'])
        self.compare_tasks(myTask, myTask2)
    def test_04_get_next_priority(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myTask = Task.Task(['1','2','3','4','5','6','7','8', '9'])
        myMenu.insert_task(myTask)
        self.assertEquals(myMenu.get_next_priority(1), 3)
        while (myMenu.get_next_priority(1) < 100):
            myTask.set_priority(myMenu.get_next_priority(1))
            myMenu.insert_task(myTask)
    def test_05_set_priority(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myTask = Task.Task(['1','1','3','4','5','6','7','first', '9'])
        myMenu.insert_task(myTask)
        myMenu.set_priority(1, 1, 15)
        task_list = myMenu.get_tasks(0)
        self.assertEquals(task_list[0].get_priority(), '15')


    def test_06_bump_priority_down(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myTask = Task.Task(['1','1','3','4','5','6','7','was first', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','2','3','4','5','6','7','was second', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','3','3','4','5','6','7','was third', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','4','3','4','5','6','7','was fourth', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','5','3','4','5','6','7','was fifth', '9'])
        myMenu.insert_task(myTask)
        myMenu.bump_priority(1, 4, 2)
        task_list = myMenu.get_tasks(1)
        task_a = task_list[0]
        task_b = task_list[1]
        task_c = task_list[2]
        task_d = task_list[3]
        task_e = task_list[4]
        self.assertEquals(task_b.get_priority(), '2')
        self.assertEquals(task_b.get_description(), 'was fourth')
        self.assertEquals(task_c.get_priority(), '3')
        self.assertEquals(task_c.get_description(), 'was second')
        self.assertEquals(task_d.get_priority(), '4')
        self.assertEquals(task_d.get_description(), 'was third')
    def test_06_bump_priority_up(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myTask = Task.Task(['1','1','3','4','5','6','7','was first', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','2','3','4','5','6','7','was second', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','3','3','4','5','6','7','was third', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','4','3','4','5','6','7','was fourth', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','5','3','4','5','6','7','was fifth', '9'])
        myMenu.insert_task(myTask)
        myMenu.bump_priority(1, 2, 4)
        task_list = myMenu.get_tasks(1)
        task_a = task_list[0]
        task_b = task_list[1]
        task_c = task_list[2]
        task_d = task_list[3]
        task_e = task_list[4]
        self.assertEquals(task_b.get_priority(), '2')
        self.assertEquals(task_b.get_description(), 'was third')
        self.assertEquals(task_c.get_priority(), '3')
        self.assertEquals(task_c.get_description(), 'was fourth')
        self.assertEquals(task_d.get_priority(), '4')
        self.assertEquals(task_d.get_description(), 'was second')

    def test_07_swap_category(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myTask = Task.Task(['1','1','3','4','5','6','7','new riginal desc', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['2','1','3','4','5','6','7','new riginal desc', '9'])
        myMenu.insert_task(myTask)
        my_pri_key = '001_001'
        new_cat = 2
        myMenu.swap_category(my_pri_key, new_cat)
        checkTask = Task.Task(['2','2','3','4','5','6','7','new riginal desc', '9'])
        task_list = myMenu.get_tasks(2)
        self.compare_tasks(task_list[1], checkTask)

    def test_08_update_task(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myTask = Task.Task(['1','1','3','4','5','6','7','new riginal desc', '9'])
        myMenu.insert_task(myTask)
        # Put three tasks in category two
        myTask = Task.Task(['2','1','3','4','5','6','7','new riginal desc', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['2','2','3','4','5','6','7','new riginal desc', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['2','3','3','4','5','6','7','new riginal desc', '9'])
        myMenu.insert_task(myTask)
        # Now change the task from category 1 to have different values and
        # make it go to category 2 with a priority of two
        xerox_Task = Task.Task(['2','2','30','40','05:30','06:30','07:30','new desc', '9'])
        native_cat_pri = '001_001'
        myMenu.update_task(xerox_Task, native_cat_pri)
        # Get the tasks from category 1: should be empty
        task_list = myMenu.get_tasks(1)
        self.assertEquals(len(task_list), 0)
        # Category two should have four entries now
        task_list = myMenu.get_tasks(2)
        self.assertEquals(len(task_list), 4)
        # The task we want should be second in line in category 2
        retrieved_task = task_list[1]
        # Note priority doesn't really bump here because there is only one task in db
        checkTask = Task.Task(['2','2','30','40','05:30','06:30','07:30','new desc', '9'])
        self.compare_tasks(checkTask, retrieved_task)
    def test_09_delete_task(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myTask = Task.Task(['1','1','3','4','5','6','7','a desc', '9'])
        myMenu.insert_task(myTask)
        myTask = Task.Task(['1','2','3','4','5','6','7','a desc', '9'])
        myMenu.insert_task(myTask)
        task_list = myMenu.get_tasks(0)
        self.assertEquals(len(task_list), 2)
        cat_pri = '001_001'
        myMenu.delete_task(cat_pri)
        task_list = myMenu.get_tasks(0)
        self.assertEquals(len(task_list), 1)
        cat_pri = '001_002'
        myMenu.delete_task(cat_pri)
        task_list = myMenu.get_tasks(0)
        self.assertEquals(len(task_list), 0)
    def test_10_multiple_users(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_user_table()
        myMenu.reset_table()    # Only resets for userid=1
        myTask = Task.Task(['1','1','3','4','5','6','7','a desc', '9'])
        myMenu.insert_task(myTask)
        myMenu2 = Menu.Menu(901)
        myMenu2.reset_table()
        myMenu2.insert_task(myTask) # Should not violate primary key constraints
        # Verify that each menu contains the same task under
        self.compare_tasks(myMenu.get_tasks(0)[0], myMenu2.get_tasks(0)[0])

    def test_11_validate(self):
        myMenu = Menu.Menu(900)     # a dummy menu
        myMenu.reset_user_table()
        userid_1 = myMenu.create_user('a_username', 'a_password4578')
        userid_2 = myMenu.validate('a_username', 'a_password4578')
        self.assertNotEquals(userid_1, None)
        self.assertNotEquals(userid_2, None)
        self.assertEquals(userid_1, userid_2)

    def test_11_set_comm_time(self):
        myMenu = Menu.Menu(999)
        userid = myMenu.create_user('some_username', 'some_password')
        myMenu = Menu.Menu(userid)
        myMenu.reset_table()
        task = Task.Task(['1','2','3','4','5','6','7','8', '0'])
        myMenu.insert_task(task)
        time1 = myMenu.set_comm_time('001_002')
        time2 = myMenu.set_comm_time('001_002')
        self.assertTrue(time2 >= time1)
        time3 = myMenu.get_comm_time('001_002')
        self.assertEquals(time2, time3)
        self.assertTrue(time2 > 1.2 * 10 ** 9)  # Epoch time in Oct 2009
        # Test against a nonexistent in_pri_cat_string
        time4 = myMenu.set_comm_time('001_002', 25) # 25 minutes ago
        self.assertTrue(time4 < time1)
        time5 = myMenu.get_comm_time('999_999') # Incorrect string -- output is the current time
        self.assertTrue(time5 >= time1)
        #~ pr("time1 is " + str(time1))
        #~ pr("time2 is " + str(time2))
        #~ pr("time3 is " + str(time3))
        self.assertEquals(task.get_seconds(), '0')
        myMenu.add_seconds_to_task(22, '001_002')
        task_list = myMenu.get_tasks(0)
        task2 = task_list[0]
        self.assertEquals(task2.get_seconds(), '22')

    def test_12_time_expired(self):
        dummyMenu = Menu.Menu(999)
        userid = dummyMenu.create_user('some_username', 'some_password')
        myMenu = Menu.Menu(userid)
        myMenu.reset_table()
        task = Task.Task(['1','2','3','4','5','6','7','8', '0'])
        myMenu.insert_task(task)
        time1 = myMenu.set_comm_time('001_002', 5)  # started 5 seconds ago
        time2 = myMenu.get_comm_time('001_002')
        time3 = myMenu.now_time()
        self.assertEqual(time1, time2)  # both report 5 seconds ago
        self.assertNotEqual(time1, time3)
        self.assertTrue((time1 + 4) <= time3)   # more than 4 min difference
        self.assertTrue((time1 + 6) >= time3)   # more than 4 min difference
        myMenu.update_seconds()
        task2 = myMenu.get_task_from_key('001_002')
        pr(" seconds are " + str(task2.get_seconds()))
        self.assertTrue(int(task2.get_seconds()) <= 6)
        self.assertTrue(int(task2.get_seconds()) >= 4)
        myMenu.clear_cur_task() # Clear currrent task from Users
        myMenu.update_seconds() # Should do nothing
        task = Task.Task(['1','5','5','5','5','6','7','8', '0'])    # min_minutes is 5, max_minutes is 5
        myMenu.insert_task(task)
        time1 = myMenu.set_comm_time('001_005', 301)  # started 301 seconds ago
        myMenu.update_seconds() # transfers at least 301 seconds to Task.__seconds
        task2 = myMenu.get_task_from_key('001_005')
        self.assertTrue(task2.min_time_fulfilled)
        self.assertTrue(task2.max_time_surpassed)



        #~ pr("time1 is " + str(time1))
        #~ pr("time2 is " + str(time2))
        #~ pr("time3 is " + str(time3))

        #~ self.assertEquals(task.get_seconds(), '0')
        #~ myMenu.add_seconds_to_task(22, '001_002')
        #~ task_list = myMenu.get_tasks(0)
        #~ task2 = task_list[0]
        #~ self.assertEquals(task2.get_seconds(), '22')

    def test_get_task_from_key(self):
        task1 = Task.Task(['1','2','3','4','5','6','7','8', '0'])
        menu = Menu.Menu(900)
        menu.insert_task(task1)
        task2 = menu.get_task_from_key('001_002')
        self.compare_tasks(task1, task2)



    def test_10_exists(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_table()
        myTask = Task.Task(['1','1','3','4','5','6','7','a desc', '9'])
        myMenu.insert_task(myTask)
        pri_key = '001_001'
        self.assertEquals(myMenu.exists(pri_key), 1)
        for in_pri_key in ['001_002', '002_001', '569_921', '000_000']:
            self.assertEquals(myMenu.exists(in_pri_key), 0)
        # Note that the syntax is exception, module.function, [arg1], [arg2]
        self.assertRaises(ValueError, myMenu.delete_task, '800_800')
        self.assertRaises(ValueError, myMenu.update_task, myTask, '851_851')
    def test_11_add_user(self):
        myMenu = Menu.Menu(900)
        myMenu.reset_user_table()
        myMenu.create_user('a_username556', 'a_password556')




    def compare_tasks(self, aTask, bTask):
        self.assertEquals(aTask.get_description(), \
        bTask.get_description())
        self.assertEquals(aTask.get_priority(), bTask.get_priority())
        self.assertEquals(aTask.get_min_minutes(), \
        bTask.get_min_minutes())
        self.assertEquals(aTask.get_max_minutes(), \
        bTask.get_max_minutes())
        self.assertEquals(aTask.get_doors_open_time(), \
        bTask.get_doors_open_time())
        self.assertEquals(aTask.get_do_at_exactly_time(), \
        bTask.get_do_at_exactly_time())
        self.assertEquals(aTask.get_category(), bTask.get_category())
        self.assertEquals(aTask.get_doors_close_time(), \
        bTask.get_doors_close_time())
        self.assertEquals(aTask.get_seconds(), \
        bTask.get_seconds())

# What changes when I SELECT?
        # self.assertEquals(myMenu.get_tasks(0), myMenu.get_tasks(0))





if __name__ == '__main__':
    unittest.main()
