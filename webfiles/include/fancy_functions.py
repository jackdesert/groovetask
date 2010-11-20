#!/usr/bin/env python
# fancy_functions.py
import unittest
import Key
import Task
import Menu
import sys
from plain_functions import pr


# Note that technical_form and colloquial_form are interchangeable.
# colloquial_form displays tasks in a human-readable format
def colloquial_form(in_task):
    # Embed a hidden input element which contains the primary
    # key of the task being edited
    key = Key.Key(in_cat = in_task.get_category(), in_pri = in_task.get_priority())
    display = "<form method='post' >\n"
    display += "   <input type='hidden' NAME='pri_key' " + \
        "value='" + key.get_str() + "'>\n"

    d_min_minutes = in_task.get_min_minutes()
    d_max_minutes = in_task.get_max_minutes()
    d_doors_open_time = in_task.get_doors_open_time()
    d_doors_close_time = in_task.get_doors_close_time()
    d_do_at_exactly_time = in_task.get_do_at_exactly_time()
    d_description = in_task.get_description()
    display += "<tr><td colspan = '5' class = 'description'>" + \
        d_description + "</td></tr>\n"
    display += '<tr>\n'
    # if possible, show min and max time
    if ((d_min_minutes != 'NULL') & (d_max_minutes != 'NULL')):
        display += "<td>Duration:" + d_min_minutes + ' - ' + d_max_minutes + \
        " minutes</td>\n"

    elif (d_min_minutes != 'NULL'):
        display += "<td>Duration: at least " + d_min_minutes + " minutes</td>\n"

    elif (d_max_minutes != 'NULL'):
        display += "<td>Duration: up to " + d_max_minutes + " minutes</td>\n"

    else:
        display += "<td> Duration: as long as it takes</td>\n"

    # if exact times exist:
    if (d_do_at_exactly_time != 'NULL'):
        display += "<td>When: at exactly " + d_do_at_exactly_time + " </td>\n"

    elif ((d_doors_open_time != 'NULL') & \
                            (d_doors_close_time != 'NULL')):
        display += "<td>When: between " + d_doors_open_time + " and " + d_doors_close_time + "</td>\n"

    elif (d_doors_open_time != 'NULL'):
        display += "<td>When: after " + d_doors_open_time + "</td>\n"

    elif (d_doors_close_time != 'NULL'):
        display += "<td>When: before " + d_doors_close_time + "</td>\n"

    else:
        display += "<td>When: anytime! </td>\n"

    display += "      <td><input type='submit' name='up_down' value='bump'></td>\n"
    display += "      <td><input type='submit' name='up_down' value='up'></td>\n"
    display += "      <td><input type='submit' name='up_down' value='edit'></td>\n"
    display += "   </tr>\n</form>\n\n"
    return(display)




# Note that technical_form and colloquial_form are interchangeable.
# technical_form displays tasks in a terse format
def technical_form(in_task):
    # Embed a hidden input element which contains the primary
    # key of the task being edited
    key = Key.Key(in_cat = in_task.get_category(), in_pri = in_task.get_priority())
    bit = "<form method='post' >\n"
    bit += "   <input type='hidden' NAME='pri_key' " + \
        "value='" + key.get_str() + "'>\n"
    bit += "   <tr>\n      <td>" + in_task.get_category() + "</td>\n"
    # bit += "<td>" + a_task.get_priority() + "</td>"

    # bit += "<td> + a_task.get_priority() + "</td>"
    bit += "      <td>" + in_task.get_min_minutes() + "</td>\n"
    bit += "      <td>" + in_task.get_max_minutes() + "</td>\n"
    bit += "      <td>" + in_task.get_doors_open_time() + "</td>\n"
    bit += "      <td>" + in_task.get_doors_close_time() + "</td>\n"
    bit += "      <td>" + in_task.get_do_at_exactly_time() + "</td>\n"
    bit += "      <td>" + in_task.get_description() + "</td>\n"
    bit += "      <td><input type='submit' name='up_down' value='up'></td>\n"
    bit += "      <td><input type='submit' name='up_down' value='down'></td>\n"
    bit += "      <td><input type='submit' name='up_down' value='edit'></td>\n"

    bit += "   </tr>\n</form>\n\n"
    return(bit)

# malleable_form displays a form for updating a task
def malleable_form(in_task):
    # Embed a hidden input element which contains the primary
    # key of the task being edited
    key = Key.Key(in_cat = in_task.get_category(), in_pri = in_task.get_priority())
    bit = ''
    bit += "<form method = 'post'><table>\n"
    bit += "   <input type='hidden' NAME='pri_key' " + \
        "value='" + key.get_str() + "'>\n"
    bit += "<tr><!-- The %s is where the SELECT tag comes from -->\n"
    bit += "<td>What groove should you be in to be most productive at this task?<br />"
    bit += cat_select(in_task) + "</td>\n"
    bit += "<td>Describe the task<br />\n"
    bit += "  <input type='text' name='description' size='57' " + \
        "value = \"" + in_task.get_description().replace('"', '\'\'') + "\"><br />\n"
    bit += "</td>\n"
    bit += "<td>Its importance (1 is highest)<br />\n"
    bit += "<input type='text' name='priority' size='1' " + \
        "value = " + in_task.get_priority() + "><br />\n"
    bit += "</td></tr></table>\n"
    bit += "<table><tr>\n"
    bit += "<td>Do for at least <br />\n"
    bit += "   <input type='text' name='min_minutes' size='2' " + \
        "value = " + in_task.get_min_minutes() + "> minutes, <br /></td>\n"
    bit += "<td>but not more than<br />\n"
    bit += "   <input type='text' name='max_minutes' size='2' " + \
        "value = " + in_task.get_max_minutes() + ">minutes.<br /></td>\n"
    bit += "<td>Begin sometime after <br />\n"
    bit += "   <input type='text' name='doors_open_time' size='5' " + \
        "value = " + in_task.get_doors_open_time() + ">, <br /></td>\n"
    bit += "<td>but end sometime before <br />\n"
    bit += "   <input type='text' name='doors_close_time' size='5' " + \
        "value = " + in_task.get_doors_close_time() + "><br /></td>\n"
    bit += "<td>or begin at exactly<br />\n"
    bit += "   <input type='text' name='do_at_exactly_time' size='5' " + \
        "value = " + in_task.get_do_at_exactly_time() + "><br /></td>\n"
    bit += "<td>\n"
    bit += "   this button<input type='submit' name = 'sbutton' value='Update' />\n"
    bit += "   <input type='submit' name = 'sbutton' value='Delete' />\n"
    bit += "</td></tr></table></form>\n"
    return(bit)


def large_form(in_task = None):
    html_data = """
    <form method="post">
        <table>
            <tr><h1>Add a Task to Your Day</h1></tr>
            <tr>
                <td>
                    What groove should you be in to be most productive at this task? <br />
                    %s<!-- This is where the SELECT tag comes from -->
                </td>
                <td>
                    Describe the task <br />
                    <input type="text" name="description" size="57"/><br />
                </td>
                <!--<td>
                    Priority <br />
                    <input type="text" name="priority" size="1"/><br />
                </td>-->
            </tr>
        </table>
        <table>
            <tr>
                <td>
                    Do for at least <br />
                    <input type="text" name="min_minutes" size="2" /> minutes<br />
                </td>
                <td>
                    but no more than <br />
                    <input type="text" name="max_minutes" size="2" />minutes<br />
                </td>
                <td>
                    Starting sometime after <br />
                    <input type="text" name="doors_open_time" size="5"/><br />
                </td>
                <td>
                    but ending before <br />
                    <input type="text" name="doors_close_time" size="5"/><br />
                </td>
                <td>
                    Or must be done at exactly <br />
                    <input type="text" name="do_at_exactly_time" size="5"/><br />
                </td>
                <td>
                    <input type="submit" name = "sbutton" value="Submit" />
                    <input type="submit" name = "sbutton" value = "Delete All Tasks" />
                </td>

            </tr>
        </table>
    </form>""" %(cat_select(in_task))
    return(html_data)

def add_one_task(in_category):
    assert(type(in_category) == type(100))  # type is int
    html_data = """
    <form method="post">
        <table>
            <tr>
                <td>
                    <input type = 'hidden' name = 'category' value = '%s' />

                    Describe the task <br />
                    <input type="text" name="description" size="57"/><br />
                </td>
                <!--<td>
                    Priority <br />
                    <input type="text" name="priority" size="1"/><br />
                </td>-->
            </tr>
        </table>
        <table>
            <tr>
                <td>
                    Do for at least <br />
                    <input type="text" name="min_minutes" size="2" /> minutes<br />
                </td>
                <td>
                    but no more than <br />
                    <input type="text" name="max_minutes" size="2" />minutes<br />
                </td>
                <td>
                    Starting sometime after <br />
                    <input type="text" name="doors_open_time" size="5"/><br />
                </td>
                <td>
                    but ending before <br />
                    <input type="text" name="doors_close_time" size="5"/><br />
                </td>
                <td>
                    Or must be done at exactly <br />
                    <input type="text" name="do_at_exactly_time" size="5"/><br />
                </td>
                <td>
                    <input type="submit" name = "sbutton" value="Submit" />
                </td>

            </tr>
        </table>
    </form>""" % str(in_category)
    return(html_data)

# Create the <select> tag with the current value selected.
def cat_select(a_task = None):
    if (a_task != None):
        cat = int(a_task.get_category())
    else:
        cat = None

    if (cat == 2):
        output = """<select name="category">
                       <option value="1">A-Energy</option>
                       <option SELECTED value="2">B-Energy</option>
                       <option value="3">R-ejuvenate</option>
                    </select>"""
    elif (cat == 3):
        output = """<select name="category">
                       <option value="1">A-Energy</option>
                       <option value="2">B-Energy</option>
                       <option SELECTED value="3">R-ejuvenate</option>
                    </select>"""
    else:
        output = """<select name="category">
                       <option value="1">A-Energy</option>
                       <option value="2">B-Energy</option>
                       <option value="3">R-ejuvenate</option>
                    </select>"""
    return(output)

def display_tasks_from_database(a_Menu, in_task_to_edit, in_add_to_cat):
    if(in_add_to_cat == ''):
        add_to_cat = 0
    else:
        add_to_cat = int(in_add_to_cat)
    del in_add_to_cat
    #~ pr('right after entry in display_tasks(), add_to_cat is ' + str(add_to_cat))
    key = Key.Key(in_task_to_edit)
    hot_cat = key.get_cat()
    #~ pr("hot_cat is " + str(hot_cat))
    hot_pri = key.get_pri()
    #~ pr("hot_pri is " + str(hot_pri))
    data = ''
    for cat in [1, 2, 3, 4]:
        task_list = a_Menu.get_tasks(cat)
        #~ pr("cur_cat is " + str(cat))

        # Generate html
        wideness = "width = '600'"
        if (cat == 1):
            category_data = """   <div id = '1'><table>
            <tr>\n      <td colspan='8' %s> <h2>A-Energy Tasks</h2>
            You're on top of your game, mentally sharp, fearless. This is where your most
            challenging, daunting tasks go. </td>\n   </tr>""" % wideness
        elif(cat == 2):
            category_data = """   <div id = '2'><table>
            <tr>\n      <td colspan='8' %s> <h2>B-Energy Tasks</h2>
            This is where you put all your tasks that are so easy-peasy that you can
            practically do them without thinking. No sense wasting your A-energy on these, so
            wait till you're burned out a little. Brain going a little slower than usual,
            so B-it-up!</td>\n   </tr>""" % wideness
        elif(cat == 3):
            category_data = """   <div id = '3'><table>
            <tr>\n      <td colspan='8' %s > <h2>R-Ejuvenate "Tasks"</h2>
            This is what you do when you really need to recharge. Put tasks here that don't
            feel like tasks at all. Take a walk. Eat a bite. Get some exercise.  </td>\n   </tr>""" % wideness
        elif(cat == 4):
            category_data = """   <div id = '4'><table>
            <tr>\n      <td colspan='8' %s> <h2>Completed Tasks</h2>
                        That's right, you did it! These are all the tasks that you finished
                        in style!</td>\n   </tr>""" % wideness
        else:
            raise ValueError('Category Out of Bounds')

        for a_task in task_list:
            #~ print("cur_pri is ", a_task.get_priority())
            cur_pri = int(a_task.get_priority())
            if ((hot_cat == cat) & (hot_pri == cur_pri)):
                one_row = malleable_form(a_task)
                #~ print("Made it inside the call to malleable_form")
            else:
                # one_row = technical_form(a_task)
                one_row = colloquial_form(a_task)
            category_data += one_row

        #~ pr('right before equals sign, and ')
        assert(type(cat) == type(add_to_cat))
        #~ pr('cat is ' + str(cat))
        #~ pr('add_to_cat is ' + str(add_to_cat))
        if(cat == add_to_cat):
            #~ pr('inside if cat == add_to_cat')
            category_data += add_one_task(add_to_cat)

        category_data += '</table>'

        if (cat == 1):
            category_data += "<form method = 'post'><input type = 'hidden' name = 'add_to_cat' value = '1'>"
            category_data += "<input type = 'submit' name = 'sbutton' value = 'Clean Slate'>"
            category_data += "<input type = 'submit' name = 'add' value = 'Add a Task'></form>"

        elif(cat == 2):
            category_data += "<form method = 'post'><input type = 'hidden' name = 'add_to_cat' value = '2'>"
            category_data += "<input type = 'submit' name = 'sbutton' value = 'Clean Slate'>"
            category_data += "<input type = 'submit' name = 'add' value = 'Add a Task'></form>"
        elif(cat == 3):
            category_data += "<form method = 'post'><input type = 'hidden' name = 'add_to_cat' value = '3'>"
            category_data += "<input type = 'submit' name = 'sbutton' value = 'Clean Slate'>"
            category_data += "<input type = 'submit' name = 'add' value = 'Add a Task'></form>"
        elif(cat == 4):
            category_data += "<form method = 'post'><input type = 'hidden' name = 'add_to_cat' value = '4'>"
            category_data += "<input type = 'submit' name = 'sbutton' value = 'Clean Slate'></form>"

        else:
            raise ValueError('Category Out of Bounds')


        data += category_data + '</div>'

    return(data)

# This function provides a random string of length N
# N is an integer
def rand_string(N = None):
    from random import sample
    seq = ['a','b','c','d','e','f','g','h','i','j', 'k', 'l', 'm']
    # limit length of output
    if ((N > len(seq)) | (N == None)):
        N = len(seq)
    rand_seq = sample(seq, N)
    rand_string = ''    # Empty string
    for entry in rand_seq:
        rand_string += str(entry)
    # assert_(len(rand_string) > 0)
    return(rand_string)


class fancy_functionsTestCase(unittest.TestCase):
    def test_01_rand_string(self):
        a = rand_string(1200)
        b = rand_string(1200)
        self.assertNotEquals(len(a), 1200)  # lentgh should be shorter
        self.assertEquals(len(a), 13)
        self.assertEquals(len(a), len(b))   # Lengths should  be same
        self.assertNotEquals(a, b)  # Contents should differ
        a = rand_string(5)
        b = rand_string(5)
        self.assertEquals(len(a), 5)  #
        self.assertEquals(len(a), len(b))   # Lengths should  be same
        self.assertNotEquals(a, b)  # Contents should differ
        a = rand_string()
        b = rand_string()
        self.assertEquals(len(a), 13)  #
        self.assertEquals(len(a), len(b))   # Lengths should  be same
        self.assertNotEquals(a, b)  # Contents should differ
    def test_02_technical_form(self):
        import Task
        import re
        A = rand_string(None)
        aTask = Task.Task(['1','2','3','4','5','6','7', A, '0'])
        B = technical_form(aTask)
        pr(B)
        self.assert_('<form' in B)
        # Use a dictionary to store key-value pairs. The key is the
        # search string. The value is how many times it should show up
        expr_dict = {r'<form': 1, r'</form>': 1,
        r"<input type='hidden' NAME='pri_key' value=": 1,
        r"(<td>[^<>]*?</td>)": 7, r"(<td>.*?</td>)": 10}
        for a_str, a_val in expr_dict.items():
            found = re.findall(a_str, B)
            print ("the string '" + a_str + "' was found " + str(len(found)) + " times")
            for res in found:
                print ("the string '" + a_str + "' was found as " + res)
            self.assertEquals(len(found), a_val)

    def test_03_malleable_form(self):
        import Task
        import re
        A = rand_string(None)
        aTask = Task.Task(['1','2','3','4','5','6','7', A, '0'])
        B = malleable_form(aTask)
        print B
        self.assert_('<form' in B)

    def test_04_large_form(self):
        import Task
        import re
        A = rand_string(None)
        aTask = Task.Task(['1','2','3','4','5','6','7', A, '0'])
        B = large_form(aTask)
        print B
        self.assert_('<form' in B)

    def test_05_colloquial_form(self):
        import Task
        import re
        A = rand_string(None)
        aTask = Task.Task(['1','2','3','4','5','6','7', A, '0'])
        B = colloquial_form(aTask)
        print B
        self.assert_('<form' in B)

    def test_06_cat_select(self):
        task1 = Task.Task(['1','2','3','4','5','6','7','8', '0'])
        task2 = Task.Task(['2','2','3','4','5','6','7','8', '0'])
        task3 = Task.Task(['3','2','3','4','5','6','7','8', '0'])
        task4 = Task.Task(['0','2','3','4','5','6','7','8', '0'])
        task_list = [task1, task2, task3, task4]
        for task in task_list:
            html = cat_select(task)
            self.assertTrue('<select' in html)
            self.assertTrue(len(html) > 200)
    def test_07_display_tasks_from_database(self):
        menu = Menu.Menu(900)
        menu.reset_table()
        task1 = Task.Task(['1','2','3','4','5','6','7','8', '0'])
        task2 = Task.Task(['2','2','3','4','5','6','7','8', '0'])
        task3 = Task.Task(['3','2','3','4','5','6','7','8', '0'])
        task4 = Task.Task(['0','2','3','4','5','6','7','8', '0'])
        task_list = [task1, task2, task3, task4]
        for task in task_list:
            menu.insert_task(task)
        html = display_tasks_from_database(menu, '999_999', '1')
        self.assertTrue(len(html) > 1500) # It's  big
    def test_08_add_one_task(self):
        html = add_one_task(2)
        self.assertTrue(len(html) > 1500) # It's  big



#~ match()  Determine if the RE matches at the beginning of the string.
#~ search() Scan through a string, looking for any location where this RE matches.
#~ findall()    Find all substrings where the RE matches, and returns them as a list.
#~ finditer()   Find all substrings where the RE matches, and returns them as an iterator.


if __name__ == '__main__':
    unittest.main()
