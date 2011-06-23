#!/usr/bin/env python
# Logic.py
# This script contains functions useful for displaying the current task

import Task
import Menu
import unittest
import Key
from plain_functions import pr
from plain_functions import now_string

# First look for any task (cat 1-3) with exact_time_passed
# Note: get_exact_time_tasks returns 'ORDER BY DESC'
# Then go to category, priority selection
def select_task(a_Menu, a_category = 1):
    current_task = None
    exact_time_list = a_Menu.get_exact_time_tasks()
    offset = a_Menu.get_utcoffset()
    for task in exact_time_list:
        if(task.exact_time_passed(offset)):
            current_task = task
            break
    if(current_task == None):
        task_list = a_Menu.get_tasks(a_category)
        for task in task_list:
            if(task.doors_are_open(offset)):
                current_task = task
                break
    return(current_task)

def declare_task_done(in_menu, in_cat_pri):
    # Note that category '4' represents completed tasks
    in_menu.swap_category(in_cat_pri, 4)
    in_menu.update_seconds()
    in_menu.clear_cur_task() # remove it from table users.cur_task

def well_done():
    bit = "<h2>Congratulations on a job well done</h2>"
    bit += "Which groove are you feeling now?"
    bit += display_groove_select()

def work_it(in_menu, in_category = 1):
    msg = ''
    bit = ''
    if (in_category == 1):
        head = "<h1>On Top of Your A-Game Groove?</h1>\n"
    elif (in_category == 2):
        head = "<h1>Feelin' More Like a B-Game Groove?</h1>\n"
    elif (in_category == 3):
        head = "<h1>Ready for some R-Ejuvenation?</h1>\n"
    else:
        head = "<h1>Please select the groove that matches your energy level</h1>\n"

    task = select_task(in_menu, in_category)
    if (task != None):
        desc = task.get_description()
        a_pri = task.get_priority()
        a_cat = task.get_category()
        key = Key.Key(in_cat = a_cat, in_pri = a_pri)
        if(in_menu.cur_task_bumped(key.get_str())):
            old_task = in_menu.get_task_from_key(in_menu.get_cur_task())
            bit += """<script type="text/javascript"><!--
            var bumped = '<h2>Your task has been bumped.</h2>'
            bumped += 'Thank you for your diligent work on your last task, <b><i>%s.  </i></b>'
            bumped += 'Either a task of greater importance has become available, '
            bumped += 'your last task is no longer available, or '
            bumped += 'GrooveTask is open in multiple browser windows.'
            setTimeout("alert(bumped);", 3000)
            // --></script>""" % old_task.get_description().replace("'", "")
        in_menu.update_seconds()
        in_menu.set_comm_time(key.get_str())
        pr(' just set_comm_time  ')
        if(task.max_time_surpassed()):
            notice= "It's time to move on. <br>Please select the done button"
            bit +="<h2>" + notice + "</h2>"
            bit += "Thank you for working on task: " + desc
            bit += """<script type="text/javascript"><!--
            setTimeout("document.title = 'Time is Up!';", 1000);
            var msg = 'Congratulations on a task well done. <br>'
            msg += 'It is time to move on. Please select the done button.'
            setTimeout("alert(msg);", 2000)
            // --></script>"""
        else:
            bit += head
            bit += "<p>Your mission, should you choose to accept it, is to </p>"
            bit += "<h2>" + desc + "</h2>\n"
        bit += display_time_spent(task)
    else:
        desc = 'Sorry, no more tasks in this groove'
        bit += head
        bit += "<h2>" + desc + "</h2>\n"
    if (task != None):
        bit += display_done_button(key.get_str())
    bit += "The time is now " + now_string(in_menu.get_utcoffset())
    bit += ".<br>Your timezone is set to " + str(in_menu.get_utcoffset()) + '.'
    bit += display_groove_select(in_category)
    return(bit)

def display_time_spent(in_task):
    tt = int(in_task.get_seconds())
    time_spent = tt / 60.0
    time_string = "%1.1f" % time_spent
    time_string.replace(' ', '')
    output = "You have invested %s minutes in this task.<br>" % time_string
    if(in_task.get_do_at_exactly_time() != 'NULL'):
        # if(in_task.exact_time_passed(offset)):
        output += 'This task may be here because it has an exact "do" time.<br>\n'
    if((in_task.get_min_minutes() != 'NULL') and (in_task.get_max_minutes() != 'NULL')):
        output += """You promised to spend between %s and %s minutes
        on this task.""" % (in_task.get_min_minutes(), in_task.get_max_minutes())
    elif(in_task.get_min_minutes() != 'NULL'):
        output += "You promised to work this task at least %s minutes." % in_task.get_min_minutes()
    elif(in_task.get_max_minutes() != 'NULL'):
        output += "You allowed yourself up to %s minutes for this task." % in_task.get_max_minutes()
    else:
        output += "Take as long as you need."
    return(output)

def display_groove_select(in_cat = None):
    bit = "<div align='center'><form method='post' >\n"
    if (in_cat == None):
        bit += "<h2>Go to Work</h2>\n"
    else:
        bit += """<br><br>Not feeling up to the assigned task? Perhaps you're
        feeling a different groove that you thought you should. """
        bit += "<h3>Switch Grooves</h3>\n"
        bit += """<script type="text/javascript"><!--
        setTimeout("document.getElementById('%s').click();",30000);
        // --></script>""" % str(in_cat)
    bit += "<input type='submit' id = '1' name = 'gbutton' value='A-Energy' />\n"
    bit += "<input type='submit' id = '2' name = 'gbutton' value='B-Energy' />\n"
    bit += "<input type='submit' id = '3' name = 'gbutton' value='R-Ejuvenate' />\n"
    bit += "<br><input type='submit' name = 'gbutton' value='Plan Your Day' />\n"
    bit += "</form></div>\n"
    return(bit)

def display_done_button(in_key_string):
    bit = "<div align='center'><form method='post' >\n"
    bit += "<input type = 'hidden' name = 'pri_key' value = '" + in_key_string + "'>\n"
    bit += "<input type='submit' name = 'gbutton' value='task_done' />\n"
    bit += "</form></div>\n"
    return(bit)

def display_login(in_message):
    assert(type(in_message) == type('some_string'))  # type is string
    bit = "<div align='center'><form method='post' >\n"
    bit += "<h1>Welcome to GrooveTask</h1>"
    bit += "<h3>" + in_message + "</h3><br>\n"
    bit += "<table><tr><td>Username:</td><td><input type = 'text' name = 'username'><br></td>\n"
    bit += "<td><input type='submit' name = 'Lbutton' value='login' /><br></td></tr>\n"
    bit += "<tr><td>Password:</td><td><input type = 'password' name = 'password'</td>\n"
    bit += "<td><input type='submit' name = 'Lbutton' value='register' /></td></tr></table>\n"
    bit += "</form></div>\n"
    return(bit)

def display_greeting(in_username):
    bit = "<form method='post' >\n"
    bit += "<div align='right'>Hello, " + in_username + "\n"
    bit += "<input type='submit' name = 'Lbutton' value='logout' />\n"
    bit += "</div>"
    return(bit)




class MenuTestCase(unittest.TestCase):

    def setUp(self):
        task1 = Task.Task(['1','1','3','4','','','','001_001', '0'])
        task2 = Task.Task(['1','2','3','4','','','','001_002', '0'])
        task3 = Task.Task(['1','3','3','4','','','','001_003', '0'])
        task4 = Task.Task(['2','1','3','4','','','','002_001', '0'])
        task5 = Task.Task(['2','2','3','4','','','','002_002', '0'])
        task6 = Task.Task(['2','3','3','4','','','','002_003', '0'])
        task7 = Task.Task(['3','1','3','4','','','','003_001', '0'])
        task8 = Task.Task(['3','2','3','4','','','','003_002', '0'])
        task9 = Task.Task(['3','3','3','4','','','','003_003', '0'])
        self.task_list = [task1, task2, task3, task4, task5, task6,
            task7, task8, task9]
        self.a_menu = Menu.Menu(1)
        self.a_menu.reset_table()
        for a_task in self.task_list:
            self.a_menu.insert_task(a_task)

    def test_menu_exists(self):
        self.assertEquals(len(self.task_list), 9)
        new_list = self.a_menu.get_tasks(0)
        self.assertEquals(len(new_list), 9)

    def test_select_task(self):
        task = select_task(self.a_menu)
        desc = task.get_description()
        self.assertEquals(desc, '001_001', 'default cat is 1')
        task = select_task(self.a_menu, 1)
        desc = task.get_description()
        self.assertEquals(desc, '001_001')
        task = select_task(self.a_menu, 2)
        desc = task.get_description()
        self.assertEquals(desc, '002_001')
        task = select_task(self.a_menu, 3)
        desc = task.get_description()
        self.assertEquals(desc, '003_001')

        ## The following has been commented out since the functionality has been moved to a different function.
        # If you want to test it, test to make sure that go_to_work tells you a task has been completed.
        # But really, the crux of the matter is it's better to test units than wholes. ;)
        #~ # set max_time and seconds in the first one, then make sure
        #~ # the second one gets selected
        #~ print("starting new code here\n\n")
        #~ updated_task = Task.Task(['1','1','3','4','5','6','7','001_001', '0'])
        #~ updated_task.set_max_minutes(5)
        #~ updated_task.set_seconds(301)
        #~ self.a_menu.update_task(updated_task, '001_001')
        #~ print("just inserted updated_task into menu")
        #~ task = select_task(self.a_menu, 1)
        #~ print("just ran select_task")
        #~ desc = task.get_description()
        #~ print("description found is", desc)
        #~ print("max_minutes is " + task.get_max_minutes())
        #~ print("seconds are " + task.get_seconds())
        #~ self.assertEquals(desc, '001_002')
    def test_select_task_with_doors_are_open(self):
        task1 = Task.Task(['1','1','3','4','9:30','10:00','','001_001', '0'])
        task2 = Task.Task(['1','2','3','4','6:00','9:59','','001_002', '0'])
        task3 = Task.Task(['1','3','3','4','10:00','14:00','','001_003', '0'])
        task4 = Task.Task(['1','4','3','4','','','','001_004', '0'])
        # Pay particular attention to the doors_open and _close times
        task_list = [task1, task2, task3, task4]
        menu = Menu.Menu(1)
        menu.reset_table()
        for task in task_list:
            self.a_menu.insert_task(task)
        import os
        os.system('sudo date -s  12:05:16 +%T')     # set system time
        new_task = select_task(menu)
        self.assertEquals(new_task.get_description(), '001_003')
        os.system('sudo ntpdate -b pool.ntp.org')    # resets time to normal


    def test_declare_task_done(self):
        new_list = self.a_menu.get_tasks(4)
        self.assertEquals(len(new_list), 0, 'Should be none completed')
        declare_task_done(self.a_menu, '001_001')
        new_list = self.a_menu.get_tasks(4)
        self.assertEquals(len(new_list), 1, 'Should be one completed')
        declare_task_done(self.a_menu, '003_001')
        new_list = self.a_menu.get_tasks(4)
        self.assertEquals(len(new_list), 2, 'Should be two completed')

    def test_work_it(self):
        html = work_it(self.a_menu,1)
        self.assertNotEqual(len(html), 0)
        self.assertTrue('001_001' in html, 'description found in html')

    def test_display_groove_select(self):
        html = display_groove_select()
        self.assertNotEqual(len(html), 0)
        self.assertTrue('input' in html, '_input_ found in html')
    def test_display_done_button(self):
        html = display_done_button('002_003')
        self.assertNotEqual(len(html), 0)
        self.assertTrue('hidden' in html, '_hidden_ found in html')
    def test_display_login(self):
        html = display_login('hi there')
        self.assertTrue('input' in html)
        self.assertTrue('hi there' in html)
        self.assertTrue(len(html) > 50)
    def test_display_greeting(self):
        html = display_greeting('my really long username')
        self.assertTrue('my really' in html)
        self.assertTrue(len(html) > 20)
    def test_display_time_spent(self):
        task = Task.Task(['1','1','3','4','5','6','7','001_001', '700'])
        html = display_time_spent(task)
        print('html is', html)
        self.assertTrue(' 11.7 ' in html)



if __name__ == '__main__':
    unittest.main()
