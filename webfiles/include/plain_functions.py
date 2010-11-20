#!/usr/bin/env python
# plain_functions.py
# some functions are being relegated to this file to prevent the
# possibility of cross-requirements. for example, if Menu.py requires
# fancy_functions.py, and vice-versa-- does it blow up?

import unittest
import sys
from datetime import tzinfo, timedelta, datetime

# Definitions for Timezone usage
ZERO = timedelta(0)
HOUR = timedelta(hours=1)


# Regular old 'print()' is not allowed on mod_wsgi, so we use this hack
# to make it portable. Use 'pr' wherever you would normally use print
def pr(input_string):
    print_string = 'j-' + input_string
    print >> sys.stderr, print_string
    return(0)


# This function makes a timestamp that looks like '23:59:00'
# It takes two arguments: hours and minutes
def time_string(in_hours, in_minutes):
    assert(type(in_hours) == type(100))    # Expects integer inputs
    assert(type(in_minutes) == type(100))    # Expects integer inputs
    minutes = str(in_minutes)
    hours = str(in_hours)
    if(len(minutes) == 1):
        minutes = '0' + minutes
    elif(len(minutes) > 2):
        minutes = minutes[0:2]  # truncate big numbers
    if(len(hours) == 1):
        hours = '0' + hours
    elif(len(minutes) > 2):
        hours = hours[0:2]  # truncate big numbers
    output = hours + ':' + minutes + ':00'
    assert(len(output) == 8)
    return(output)

# This function makes a timestamp that looks like '23:59:00' based
# on the current time, with the appropriate time zone.
# It takes one argument: the timezone offset (in hours)
def now_string(in_tzo = None):    # -5 is for Eastern Standard Time
    tzo = FixedOffset(in_tzo, 'Some Standard Time') # Time Zone Offset
    a = datetime.now(tzo)
    output = time_string(a.hour, a.minute)
    return(output)



# A class building tzinfo objects for fixed-offset time zones.
# Note that FixedOffset(0, "UTC") is a different way to build a
# UTC tzinfo object.

class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, in_utcoffset, name):
	in_utcoffset = in_utcoffset + 0 # The +1 is for daylight savings time
        if(type(in_utcoffset) == type(100)):
            in_utcoffset = bind(in_utcoffset)   # limit values
            self.__offset = timedelta(hours = in_utcoffset)
            pr('inside if type loop')
        else:
            self.__offset = timedelta(hours = 0)
            pr('incorrect data. in_utcoffset is ' + str(in_utcoffset) + 'and type is ' + str(type(in_utcoffset)))

        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
	# return ZERO # No daylight savings offset (use in winter)
        return HOUR # One hour of daylight savings (use in summer)


#~
#~ # A UTC class.
#~ class tzo(tzinfo):
    #~ """tzo"""
    #~ # Return offset of local time from UTC, in minutes east of UTC.
    #~ #If local time is west of UTC, this should be negative. Note that
    #~ #this is intended to be the total offset from UTC;
    #~ in_offset = None
    #~ def utcoffset(self, dt):
        #~ if(type(in_offset) == type(100)):
            #~ return (-5 * HOUR)  # -7 for Mountain Time, -5 for Eastern Time
        #~ else:
            #~ return(-5 * HOUR)
#~
#~
    #~ def tzname(self, dt):
        #~ return "Mountain_Standard_Time"
#~
    #~ def dst(self, dt):
        #~ return ZERO     # No daylight savings offset

# This function makes sure a value is within bounds
def bind(input):
    assert(type(input) == type(100))    #Value must be int
    lower_bound = -11
    upper_bound = 12
    input = min(input, upper_bound)
    input = max(input, lower_bound)
    return(input)




#########    U N I T   T E S T I N G     ###########
class plain_functionsTestCase(unittest.TestCase):
    def test_time_string(self):
        print("Testing plain_functions.py")
        time = time_string(5, 10)
        assert(time == '05:10:00')
        time = time_string(10, 5)
        assert(time == '10:05:00')
        assert(time > time_string(0, 0))
        assert(time < time_string(23, 59))
        assert(time_string(10, 3) < time_string(12, 50))
        assert(time_string(11, 11) == time_string(11, 11))

    def test_FixedOffset(self):
        tz1 = FixedOffset(-7, 'Mountain Standard Time')
        tz2 = FixedOffset(-5, 'Eastern Standard Time')
        a = datetime.now(tz1)
        b = datetime.now(tz2)
        self.assertTrue(a.hour + 2, b.hour)
    def test_now_string(self):
        tz = FixedOffset(5, 'Eastern Standard Time')
        print "right now it's " + now_string()
        assert(now_string() > time_string(0, 0))
        assert(now_string() < time_string(23, 59))
    def test_bind(self):
        self.assertEqual(6, bind(6))
        self.assertEqual(12, bind(300))
        self.assertEqual(-11, bind(-2400))



if (__name__ == '__main__'):
    unittest.main()
