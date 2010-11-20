#!/usr/bin/env python

# What's on *Your* Menu?
# Obviously there are a million tasks you could do in a day, just like
# the many things you could eat for dinner. But which one will you do?
# And when?
# Menu.py by Jack Desert <jackdesert556@gmail.com>
# Also see www.letseatalready.com
# This script puts data from the class 'Task' into a database
# Note this module has been tested on Python2.6
import Task
import Key
import cgi  # CGI for escape filter
import cgitb
from time import time as unixtime
from plain_functions import pr
cgitb.enable()

# From within python2.6:
# import the C library of pyPgSQL
from pyPgSQL import libpq
# import the DBAPI2.0 intervace of pyPgSQL
from pyPgSQL import PgSQL
# Connect to the database. Make sure you have already created the
# database and that there is a table named 'weather', and that you
# really have at least one row inserted into the table 'weather'

class Menu:
    def __init__(self, in_userid):
        self.__tasks = []
        self.db = PgSQL.connect (database="jackdesert_groove", user="jackdesert_groove", password="123567")
        self.cur = self.db.cursor()
        # self.reset_table(self.cur)
        self.__userid = int(in_userid)
        self.__utcoffset = int(self.retrieve_utcoffset())

    def get_userid(self):
        return(self.__userid)
    def get_utcoffset(self):
        return(self.__utcoffset)
    def retrieve_utcoffset(self):
        query = "SELECT utcoffset FROM users WHERE userid = "
        query += str(self.get_userid())
        self.cur.execute(query)
        result = self.cur.fetchone()
        if(result):
            return(result[0])
        else: return(999)   # Dummy value for when no user exists


    def reset_table(self, in_cat = None):
        query = "DELETE FROM Tasks WHERE userid = "
        query += str(self.get_userid())
        if(in_cat != None):
            query += " AND category = " + str(in_cat)
        self.cur.execute(query)
        self.db.commit()
        #~ pr("All previous tasks deleted")

    def reset_user_table(self):
        self.cur.execute("DELETE FROM Users")
        self.db.commit()
        #~ pr("All previous users deleted")

    def validate(self, in_username, in_password):
        # This can be called from a dummy menu to validate and get a valid userid
        # Output is an int of the userid, or None if none is found
        a_hash = hash(in_password)
        query = "SELECT userid FROM Users WHERE username = '"
        query += in_username + "' AND pass_hash = " + str(a_hash)
        #~ pr("\n\n\nquery is ", query)
        self.cur.execute(query)
        # fetch a result set
        result = self.cur.fetchall()
        found_userid = None
        if (len(result) > 0):
            #~ pr("\n\n\nresult is ", result)
            found_userid = int(result[0][0])
        return(found_userid)


    def create_table(self, cursor):
        cursor.execute ("""CREATE TABLE Tasks(
        category    int,
        priority    int,
        min_minutes int,
        max_minutes int,
        doors_open_time time,
        doors_close_time    time,
        do_at_exactly_time  time,
        description         varchar(250),
        seconds int,
        userid  int,
        PRIMARY KEY (category, priority, userid)
        )""")
        #~ pr("Table Created")
        pr("Remember to 'GRANT ALL PRIVILEGES ON TABLE Tasks TO jackdesert_groove'")
    def create_user_table(self, cursor):
        cursor.execute ("""CREATE TABLE Users(
        userid    int,
        username    varchar(59),
        pass_hash   int,
        cur_task    varchar(7),
        comm_time  int,     --Note comm_time is in seconds
        utcoffset   int,    -- Note this is -7 for Mountain Time
        PRIMARY KEY (userid)
        )""")
        pr("Remember to 'GRANT ALL PRIVILEGES ON TABLE Users TO jackdesert_groove'")

    def create_user(self, in_username, in_password):
        if (self.username_exists(in_username)):
            pr('Username already exists')
            return(None)    #raise(ValueError, 'Username already exists')
        else:
            pass_hash = hash(in_password)
            username = cgi.escape(in_username)
            query = "SELECT MAX(userid) FROM Users"
            self.cur.execute(query)
            result = self.cur.fetchall()
            result_str = result[0][0]
            if (result_str == None):
                userid = 1
            else:
                userid = (int(result_str) + 1)
            query = "INSERT INTO Users (userid, username, pass_hash, utcoffset)" + \
            " VALUES (" + str(userid) + ", '" + username + "', " + str(pass_hash) + ', -5)'
            #~ pr("\n\n About to insert a user")
            #~ pr(query)
            self.cur.execute(query)
            self.db.commit()
            #~ pr("create_user query executed")
            return(userid)

    def set_comm_time(self, in_cat_pri_string, seconds_ago = None):
        if (self.exists(in_cat_pri_string)):
            pass
        else:
            raise ValueError('Cannot set comm_time without pri_key match')
        seconds = int(unixtime())
        if(seconds_ago):    # Set to a time in the past for testing
            assert(type(seconds_ago) == type(100))  # Must be int
            seconds -= seconds_ago
        query = "UPDATE Users SET comm_time = " + str(seconds)
        query += ", cur_task = '" + in_cat_pri_string
        query += "' WHERE userid = " + str(self.get_userid())
        self.cur.execute(query)
        self.db.commit()
        pr('query executed is::::::::  ' + query)
        pr('string is            ::::::::::::::::   ' + in_cat_pri_string)
        return(seconds)

    def clear_cur_task(self):
        query = "UPDATE Users SET cur_task = NULL"
        query += " WHERE userid = " + str(self.get_userid())
        self.cur.execute(query)
        self.db.commit()
        pr('Inside clear_cur_task     query is::::::::' + query)

    def get_comm_time(self, in_cat_pri_string):
        query = "SELECT cur_task, comm_time FROM Users"
        query += " WHERE userid = " + str(self.get_userid())
        self.cur.execute(query)
        result = self.cur.fetchone()
        cur_task = result[0]
        if(cur_task == in_cat_pri_string):
            comm_time = result[1]
            #~ pr(' cur_task == in_cat_pri_string ')
            return(comm_time)
        else:
            now_time = unixtime()
            #~ pr(' cur_task not equal to in_cat_pri_string ')
            return(now_time)

    def get_cur_task(self):
        query = "SELECT cur_task FROM Users"
        query += " WHERE userid = " + str(self.get_userid())
        self.cur.execute(query)
        result = self.cur.fetchone()
        if(len(result) > 0):
            cur_task = result[0]
            return(cur_task)
        else:
            return(None)


    # This function tells us whether the current task got switched
    # without the user telling it to switch. This happens when a new
    # task takes priority because the clock has advanced and opened
    # a door
    def cur_task_bumped(self, in_cat_pri_string):
        query = "SELECT cur_task FROM Users"
        query += " WHERE userid = " + str(self.get_userid())
        self.cur.execute(query)
        result = self.cur.fetchone()
        cur_task = result[0]
        if(cur_task == None):
            return(False)   # No task saved, so not bumped
        elif(cur_task[0:3] != in_cat_pri_string[0:3]):
            return(False)   # Different category selected, so not bumped
        elif(cur_task == in_cat_pri_string):
            return(False)   # Exact same task selected, so not bumped
        else:
            pr('cur_task as a string is ' + cur_task)
            pr('in_cat_pri_string is ' + in_cat_pri_string)
            return(True)    # Same category, different priority, BUMPED!

    def update_seconds(self):
        query = "SELECT cur_task, comm_time FROM Users"
        query += " WHERE userid = " + str(self.get_userid())
        self.cur.execute(query)
        result = self.cur.fetchone()
        cur_task = result[0]
        comm_time = result[1]
        if cur_task == None:
            pass
            #~ pr("No action taken in update_seconds() because no pri_key match")
        elif (self.exists(cur_task)):
            key = Key.Key(cur_task)
            cat = key.get_cat()
            pri = key.get_pri()
            delta_seconds = int(unixtime()) - comm_time
            qu = "UPDATE Tasks SET seconds = seconds + "
            qu += str(delta_seconds)
            qu += " WHERE category = " +  str(cat) + ' AND '
            qu += "priority = " +  str(pri) + ' AND '
            qu += "userid = " + str(self.get_userid())
            self.cur.execute(qu)
            self.db.commit()
        else:
            pass
            #~ pr("No action taken in update_seconds() because no pri_key match")
            #~ pr('did you forget to Menu.clear_cur_task?')
            #~ pr('raise(ValueError, 'cur_task does not match a valid task or None')

    def username_exists(self, a_username):
        query = "SELECT userid FROM Users WHERE username = '"
        query += a_username + "'"
        self.cur.execute(query)
        result = self.cur.fetchall()
        if (len(result) > 0 ):
            return(1)
        else:
            return(0)

    def now_time(self):
        return int(unixtime())

    def get_task_from_key(self, in_cat_pri_string):
        if (self.exists(in_cat_pri_string)):
            pass
        else:
            raise ValueError('Cannot delete task without pri_key match')
        key = Key.Key(in_cat_pri_string)
        cat = key.get_cat()
        pri = key.get_pri()
        query = "SELECT category, priority, min_minutes, max_minutes, \
        doors_open_time, doors_close_time, do_at_exactly_time, \
        description, seconds FROM Tasks"
        query += " WHERE category = " +  str(cat) + ' AND '
        query += "priority = " +  str(pri) + ' AND '
        query += "userid = " + str(self.get_userid())
        self.cur.execute(query)
        result = self.cur.fetchone()
        new_task = Task.Task(result)
        return(new_task)

    # Note that description uses an apostrophe to escape itself
    def insert_task(self, a_Task):
        query = """INSERT INTO Tasks(category, priority, min_minutes,
        max_minutes, doors_open_time, doors_close_time, do_at_exactly_time,
        description, seconds, userid) VALUES (""" + \
        a_Task.get_category() + ', ' + \
        a_Task.get_priority() + ', ' + \
        a_Task.get_min_minutes() + ', ' + \
        a_Task.get_max_minutes() + ', ' + \
        self.tquote(a_Task.get_doors_open_time()) + ', ' + \
        self.tquote(a_Task.get_doors_close_time()) + ', ' + \
        self.tquote(a_Task.get_do_at_exactly_time()) + ', ' + \
        '\'' + a_Task.get_description().replace("'", "''") + '\', ' + \
        a_Task.get_seconds() + ', ' + str(self.get_userid()) + ')'
        #~ pr("\n\nAbout to print query for Menu.self.insert_task")
        #~ pr(query)
        self.cur.execute(query)
        # After you INSERT data into the database, you must commit it before any
        # external transactions can see it
        self.db.commit()
        # cursor.commit()
        #~ pr("query executed")


# Note this function definition is here only to facilitate unit testing
# It adds however many seconds you tell it to add, regardless of
# how long a task has been active.
    def add_seconds_to_task(self, minutes_to_add, in_cat_pri_string):
        assert(type(minutes_to_add) == type(100))   # Integer type
        if (self.exists(in_cat_pri_string)):
            pass
        else:
            raise ValueError('Cannot delete task without pri_key match')
        key = Key.Key(in_cat_pri_string)
        cat = key.get_cat()
        pri = key.get_pri()
        query = "UPDATE Tasks SET "
        query += 'seconds = seconds + ' + str(minutes_to_add)
        query += ' WHERE category = ' + str(cat) + ' AND '
        query += 'priority = ' + str(pri) + ' AND '
        query += 'userid = ' + str(self.get_userid())
        self.cur.execute(query)
        self.db.commit()
        #~ pr("cat is " + str(cat))
        #~ pr("pri is " + str(pri))

    def update_task(self, a_Task, in_cat_pri_string):
        if (self.exists(in_cat_pri_string)):
            pass
        else:
            raise ValueError('Cannot delete task without pri_key match')
        orig_key = Key.Key(in_cat_pri_string)
        orig_cat = orig_key.get_cat()
        orig_pri = orig_key.get_pri()
        new_cat = a_Task.get_category()
        new_pri = a_Task.get_priority()
        # First set everything but cat and pri
        query = "UPDATE Tasks SET "
        query += 'min_minutes = ' + a_Task.get_min_minutes() + ', '
        query += 'max_minutes = ' + a_Task.get_max_minutes() + ', '
        query += 'doors_open_time = '
        query += self.tquote(a_Task.get_doors_open_time()) + ', '
        query += 'doors_close_time = '
        query += self.tquote(a_Task.get_doors_close_time()) + ', '
        query += 'do_at_exactly_time = '
        query += self.tquote(a_Task.get_do_at_exactly_time()) + ', '
        query += 'description = '
        query += self.tquote(a_Task.get_description().replace("'", "''")) + ', '
        query += 'seconds = ' + a_Task.get_seconds()
        query += ' WHERE category = ' + str(orig_cat) + ' AND '
        query += 'priority = ' + str(orig_pri) + ' AND '
        query += 'userid = ' + str(self.get_userid())
        #~ pr("\n\nAbout to print query for Menu.self.update_task")
        #~ pr(query)
        self.cur.execute(query)
        # After you INSERT data into the database, you must commit it before any
        # external transactions can see it
        self.db.commit()
        #~ pr("\nx\nx\nx\nx\nxOutside orig_pri")
        # Now set category to new category
        if (orig_cat != int(new_cat)):
            #~ pr("\nb\nb\nb\nb\nbinside orig_cat")
            ch_cat_pri_string = self.swap_category(in_cat_pri_string, new_cat)
            ch_key = Key.Key(ch_cat_pri_string)
            orig_cat = ch_key.get_cat()
            orig_pri = ch_key.get_pri()

        if (orig_pri != int(new_pri)):
            #~ pr("\ng\ng\ng\ng\ng\ng\nginside orig_pri")
            self.bump_priority(orig_cat, orig_pri, int(new_pri))



    # Note that once this completes, the priority will be reset to
    # the next available priority
    def swap_category(self, in_cat_pri_string, new_cat):
        if (self.exists(in_cat_pri_string)):
            pass
        else:
            raise ValueError('Cannot swap task category without pri_key match')
        orig_key = Key.Key(in_cat_pri_string)
        orig_cat = orig_key.get_cat()
        orig_pri = orig_key.get_pri()
        new_pri = str(self.get_next_priority(new_cat))
        #~ pr("\n\nInside origcat != new_cat")
        query = "UPDATE tasks SET category = " + str(new_cat)
        query += ", priority = " + new_pri
        query += ' WHERE category = ' + str(orig_cat) + ' AND '
        query += 'priority = ' + str(orig_pri) + ' AND '
        query += 'userid = ' + str(self.get_userid())
        #~ pr("\n\nAbout to print query for Menu.self.update_task")
        #~ pr(query)
        self.cur.execute(query)
        # After you INSERT data into the database, you must commit it before any
        # external transactions can see it
        self.db.commit()
        #~ pr("query executed")
        # Return new cat_pri for use later
        new_key = Key.Key(in_cat = new_cat, in_pri = new_pri)
        return(new_key.get_str())

    def delete_task(self, in_cat_pri_string):
        if (self.exists(in_cat_pri_string)):
            pass
        else:
            raise ValueError('Cannot delete task without pri_key match')
        key = Key.Key(in_cat_pri_string)
        in_cat = key.get_cat()
        in_pri = key.get_pri()
        query = "DELETE FROM Tasks WHERE "
        query += 'category = ' + str(in_cat) + ' AND '
        query += 'priority = ' + str(in_pri) + ' AND '
        query += 'userid = ' + str(self.get_userid())
        #~ pr("\n\nAbout to print query for Menu.self.delete_task")
        #~ pr(query)
        self.cur.execute(query)
        # After you INSERT data into the database, you must commit it before any
        # external transactions can see it
        self.db.commit()
        # cursor.commit()
        #~ pr("query executed.")

    def exists(self, in_cat_pri_string):
        key = Key.Key(in_cat_pri_string)
        in_cat = key.get_cat()
        in_pri = key.get_pri()
        query = "SELECT category FROM Tasks WHERE "
        query += 'category = ' + str(in_cat) + ' AND '
        query += 'priority = ' + str(in_pri) + ' AND '
        query += 'userid = ' + str(self.get_userid())
        #~ pr("\n\nAbout to print query for Menu.self.delete_task")
        #~ pr(query)
        self.cur.execute(query)
        result = self.cur.fetchall()
        if (len(result) == 1):
            return(1)
        elif (len(result) == 0):
            return(0)
        else:
            raise ValueError('More than 1 match when 0 or 1 expected')



    def get_tasks(self, category):
        # Note that if category == 0, all results will be printed
        query = "SELECT category, priority, min_minutes, max_minutes, \
        doors_open_time, doors_close_time, do_at_exactly_time, \
        description, seconds FROM Tasks"
        if (category != 0):
            query += (" WHERE category = " +  str(category)) + ' AND '
        else:
            query += " WHERE "
        query += 'userid = ' + str(self.get_userid())
        query += (" ORDER BY priority ASC")
        #~ print query
        self.cur.execute(query)
        # fetch a result set
        result = self.cur.fetchall()
        # Create a set of Tasks to return
        returned_tasks = []
        for result_row in result:
            a_Task = Task.Task(result_row)
            # pr("Displaying a task pulled back from the database")
            # a_Task.display()
            returned_tasks += [a_Task]
        #~ pr(" There were " + str(len(result)) + " rows.")
        return(returned_tasks)

    def get_exact_time_tasks(self):
        # Note that if category == 0, all results will be printed
        query = "SELECT category, priority, min_minutes, max_minutes, \
        doors_open_time, doors_close_time, do_at_exactly_time, \
        description, seconds FROM Tasks"
        query += " WHERE category <= 3 AND "
        query += "do_at_exactly_time IS NOT NULL AND "
        query += 'userid = ' + str(self.get_userid())
        query += " ORDER BY do_at_exactly_time DESC"
        #~ print query
        self.cur.execute(query)
        # fetch a result set
        result = self.cur.fetchall()
        # Create a set of Tasks to return
        returned_tasks = []
        for result_row in result:
            a_Task = Task.Task(result_row)
            # pr("Displaying a task pulled back from the database")
            # a_Task.display()
            returned_tasks += [a_Task]
        #~ pr(" There were " + str(len(result)) + " rows.")
        return(returned_tasks)


    def get_next_priority(self, category):
        # Note that if category == 0, all results will be printed
        query = "SELECT max(priority) FROM Tasks"
        query += (" WHERE category = " +  str(category)) + ' AND '
        query += 'userid = ' + str(self.get_userid())
        #~ print query
        self.cur.execute(query)
        # fetch a result set
        result = self.cur.fetchall()
        # Create a set of Tasks to return
        # pr("\n\nAbout to print result from Menu.py\n")
        # pr(result)
        result_str = result[0][0]
        if (result_str == None):
            output = 1
        else:
            output = (int(result_str) + 1)
        #~ pr("output is ", output)
        return(output)

    # inputs are ints
    def set_priority(self, category, current_priority, new_priority):
        query = "UPDATE tasks SET priority = " + str(new_priority)
        query += " WHERE priority = " + str(current_priority)
        query += " AND category = " + str(category) + ' AND '
        query += 'userid = ' + str(self.get_userid())
        self.cur.execute(query)
        # After you INSERT data into the database, you must commit it before any
        # external transactions can see it
        self.db.commit()

    # This function bumps the priority of a task up or down, and
    # shifts everything else to accommodate
    # inputs are ints
    # Note that if it's already the highest or lowest priority,
    # The value will not change moreso
    def bump_priority(self, in_cat, current_priority, new_priority):
        task_list = self.get_tasks(in_cat)
        # if priority is going down, increment everything in between
        if (new_priority == current_priority):
            pass
            #~ raise ValueError('New Priority is the same as Current')

        elif (new_priority < current_priority):
            # get tasks where category matches, priority is between
            # curent_priority and new_priority, inclusive
            query = "SELECT priority FROM tasks WHERE "
            query += "priority <= " + str(current_priority)
            query += " AND priority >= " + str(new_priority) + ' AND '
            query += 'userid = ' + str(self.get_userid())
            query += " ORDER BY priority DESC"
            self.cur.execute(query)
            pri_list = self.cur.fetchall()
            # Set the highest pri to 1000000
            big_number = 1000000
            self.set_priority(in_cat, pri_list[0][0], big_number)
            # Bump all the others up just one notch
            for pri in pri_list[1:]:
                #~ pr("in pri_list[1:], pri is ", pri)
                self.set_priority(in_cat, pri[0], (pri[0] + 1))
            # Now set the one with the highest priority to the lowest
            #~ pr("\n\nAbout to set last line\n\n")
            #~ pr("pri_list before changing pri is ", pri_list)
            # Set the priority of the highest pri after change (big_num)
            # to the original lowest pri
            self.set_priority(in_cat, big_number, pri_list[-1][0])
        else:
            # The only difference here is the <= and >= are swapped
            # in the query, ORDER BY ASC instead of DESC,
            # and set_priority to 'x-1' instead of 'x+1'
            query = "SELECT priority FROM tasks WHERE "
            query += "priority >= " + str(current_priority)
            query += " AND priority <= " + str(new_priority) + ' AND '
            query += 'userid = ' + str(self.get_userid())
            query += " ORDER BY priority ASC"
            self.cur.execute(query)
            pri_list = self.cur.fetchall()
            # Set the highest pri to 1000000
            big_number = 1000000
            self.set_priority(in_cat, pri_list[0][0], big_number)
            # Bump all the others up just one notch
            for pri in pri_list[1:]:
                #~ pr("in pri_list[1:], pri is ", pri)
                self.set_priority(in_cat, pri[0], (pri[0] - 1))
            # Now set the one with the highest priority to the lowest
            #~ pr("\n\nAbout to set last line\n\n")
            #~ pr("pri_list before changing pri is ", pri_list)
            # Set the priority of the highest pri after change (big_num)
            # to the original lowest pri
            self.set_priority(in_cat, big_number, pri_list[-1][0])


    # If time is entered into SQL as 'NULL' instead of simply NULL,
    # It throws an exception. So we will only put quotes around actual
    # times
    def tquote (self, in_string):
        if ((in_string == 'NULL') | (in_string == 'null')):
            out_string = 'NULL'   # No escaped quotes
        else:
            out_string = '\'' + in_string + '\''  # quote
        return out_string


if __name__ == '__main__':
    print("Please use the file MenuTestCase.py to test this code")
