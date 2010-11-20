#!/usr/bin/env python

# import cgitb
# cgitb.enable()

import re   # Regular Expressions
import cgi  # CGI for escape filter
import Key
from plain_functions import time_string
from plain_functions import now_string

# Note all values in Task are stored as strings.
# while in the database, they are stored as either ints or times
class Task:
    def __init__(self, input):
        # pr("lenth of input is", len(input))
        # define 'private' variables
        self.__category = ''
        self.__priority = ''
        self.__min_minutes = ''
        self.__max_minutes = ''
        self.__doors_open_time = ''
        self.__doors_close_time = ''
        self.__do_at_exactly_time = ''
        self.__description = ''
        self.__seconds = ''
        # Assign values to 'private' variables
        if len(input) == 9:
            self.set_category(input[0])
            self.set_priority(input[1])
            self.set_min_minutes(input[2])
            self.set_max_minutes(input[3])
            self.set_doors_open_time(input[4])
            self.set_doors_close_time(input[5])
            self.set_do_at_exactly_time(input[6])
            self.set_description(input[7])
            self.set_seconds(input[8])
        else:
            raise Exception("Input list has wrong length")
    def display(self):
        print("category is", self.get_category())
        print("priority is", self.get_priority())
        print("min_minutes is", self.get_min_minutes())
        print("max_minutes is", self.get_max_minutes())
        print("doors_open_time is", self.get_doors_open_time())
        print("doors_close_time is", self.get_doors_close_time())
        print("do_at_exactly_time is", self.get_do_at_exactly_time())
        print("And finally, description is", self.get_description())
        print("But then again, seconds are ", self.get_seconds())

    def min_time_fulfilled(self):
        min_minutes = self.get_min_minutes()
        seconds = self.get_seconds()
        if(min_minutes == 'NULL'):
            return(0)
        elif (int(seconds) >= 60 * int(min_minutes)):
            return(1)
        else:
            return(0)

    def max_time_surpassed(self):
        max_minutes = self.get_max_minutes()
        seconds = self.get_seconds()
        if(max_minutes == 'NULL'):
            return(0)
        elif(int(seconds) >= 60 * int(max_minutes)):
            return(1)
        else:
            return(0)

    # returns true if between doors open and doors close, if listed
    def doors_are_open(self, in_offset):
        open_time_pass, close_time_pass = 0, 0

        open_time = self.get_doors_open_time()
        if(open_time == 'NULL'):
            open_time_pass = 1
        elif(open_time <= now_string(in_offset)):
            open_time_pass = 1

        close_time = self.get_doors_close_time()
        if(close_time == 'NULL'):
            close_time_pass = 1
        elif(close_time > now_string(in_offset)):
            close_time_pass = 1
        if((open_time_pass) and (close_time_pass)):
            return(1)
        else:
            return(0)

    # returns true if do_at_exactly_time has been passed
    def exact_time_passed(self, in_offset):
        exact_time = self.get_do_at_exactly_time()
        if(exact_time == 'NULL'):
            raise(ValueError, 'Should not be null if checking exact')
        elif(exact_time <= now_string(in_offset)):
            return(True)
        else:
            return(False)

    def get_key_string(self):
        cat = self.get_category()
        pri = self.get_priority()
        key = Key.Key(in_cat = cat, in_pri = pri)
        return(key.get_str())

    def set_category(self, a):
        self.__category = self.decimal_filter(a)
    def get_category(self):
        return self.__category


    def set_priority(self, a):
        self.__priority = self.decimal_filter(a)
    def get_priority(self):
        return self.__priority


    def set_min_minutes(self, a):
        self.__min_minutes = self.decimal_filter(a)
    def get_min_minutes(self):
        return self.__min_minutes


    def set_max_minutes(self, a):
        # pr("\n\nprinting a from set_max_minutes")

        self.__max_minutes = self.decimal_filter(a)
    def get_max_minutes(self):
        return self.__max_minutes

    def set_doors_open_time(self, a):
        self.__doors_open_time = self.time_filter(a)
    def get_doors_open_time(self):
        return self.__doors_open_time

    def set_doors_close_time(self, a):
        self.__doors_close_time = self.time_filter(a)
    def get_doors_close_time(self):
        return self.__doors_close_time

    def set_do_at_exactly_time(self, a):
        self.__do_at_exactly_time = self.time_filter(a)
    def get_do_at_exactly_time(self):
        return self.__do_at_exactly_time

    def set_description(self, a):
        if ((a == 'null') | (a == 'NULL') | (a == '')):
            return('NULL')
        else:
            a = cgi.escape(a)
            a = a.replace("\\", '/') # No escape chars in SQL
            a = a[0:250]    # SQL field is only 250 long
            self.__description = a
    def get_description(self):
        return self.__description

    def set_seconds(self, a):
        self.__seconds = self.decimal_filter(a)
    def add_seconds(self, a):
        orig_seconds = int(self.__seconds)
        delta = orig_seconds + int(self.decimal_filter(a))
        self.__seconds = self.decimal_filter(delta)
    def get_seconds(self):
        return self.__seconds

    # This filter removes anything that is not a decimal value
    # If no value is given, outputs 'NULL'
    def decimal_filter(self, a):
        if (a == None):
            output_string = 'NULL'
        elif ((a == 'null') | (a == 'NULL') | (a == '')):
            output_string = 'NULL'
            # pr("a is '', so skipping the regular expression")
        else:
            # Let 'a' strip to only digits 0-9
            # pr("Before the regex, a is ", a)
            # This returns an object
            a = str(a)  # Just in case it comes in as an integer
            compiled_obj = re.compile(r"[0-9]+")
            result_obj = compiled_obj.search(a)
            if (result_obj):
                # pr("match!")
                output_string = result_obj.group()
            else:
                # pr("Sorry, no match this time")
                output_string = 'NULL'

            # return the whole object as a string
            # pr("After the regex, output_string is ", output_string)
            # pr("Decimal filter value set to", output_string)
        return output_string

    def time_filter(self, a):
        if (a == None):
            output_string = 'NULL'
        elif ((a == 'null') | (a == 'NULL') | (a == '')):
            output_string = 'NULL'
            # pr("a is '', so skipping the regular expression")
        else:
            a = str(a)  # Just in case it comes in as an integer
            # Let 'a' strip to only digits 0-9 and maybe a colon
            compiled_obj = re.compile(r"[0-9]{1,2}(:\d\d){0,1}")
            result_obj = compiled_obj.search(a)
            if (result_obj):
                # pr("match!")
                # return the whole object as a tring
                intermediate_string = result_obj.group()
                # pr("Match found is ", intermediate_string)

                # Create a timestamp from string
                # Did the user indicate minutes as part of the timestamp?
                compiled_obj2 = re.compile(r"(:\d\d)+")
                result_obj2 = compiled_obj2.search(a)
                if (result_obj2):
                    # pr("Minutes detected. Adding seconds to timestamp")
                    output_string = intermediate_string + ':00'
                else:
                    # pr("Minutes not detected. Adding both minutes and seconds to timestamp")
                    output_string = intermediate_string + ':00:00'
                if(len(output_string) == 7):    # add leading zero
                    output_string = '0' + output_string
                assert(len(output_string) == 8)
            else:
                # pr("Sorry, no match this time-- returning an empty string")
                output_string = 'NULL'
        # pr("time filter data set to", output_string)
        return output_string






if __name__ == '__main__':
    print("Please use the file TaskTestCase.py to test this code")

