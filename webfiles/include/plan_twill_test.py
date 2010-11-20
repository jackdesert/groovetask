#!/usr/bin/env python
# plan_twill_test.py
# This script uses twill to test the gui framework of plan_your_day.wsgi

from twill.commands import go, follow, showforms, fv, submit, find, notfind, code, save_html, show, info
from twill.commands import showhistory, showlinks, formvalue
from random import sample
from twill import get_browser
from fancy_functions import rand_string

b=get_browser()
b.go("localhost:8051")
code(200)   # Verifieds that the page loaded properly
c = show()
print(c)        # Prints the browser output to the terminal
b.showforms()   # Prints the content of all the forms to the terminal
b.show_cookies()
# Select the second form. Attempt to assign the read-only variable 'pri_key'
# as a dummy select
#~ formvalue(2, 'pri_key', '999_999')    # select the second form
#~ b.submit(4)     # Hit the 5th submit button (should be the 'edit' of first task)
#~ # note that after the submit step, it should tell you which button it clicked.
#~ b.showforms()

#~ find('Category')    # When the page loads, category names display
#~ notfind('parsing_post')     # Make sure the name of the old file is not there
#~ info()          # Tells basic information about the page
#~ showhistory()   # Shows where you've been
#~ showlinks()     # Shows all the links on the page

#~ rand_string = sample(['a','b','c','d','e','f','g','h','i','j'],9)
#~ # Set the values in the first form and submit it
#~ formvalue(1, 'description', rand_string)   # <formnum> <fieldname> <value>
#~ submit(1)   # Click the submit button of the first form
#~ find(rand_string)
