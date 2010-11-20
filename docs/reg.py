#!/usr/bin/env python
# reg.py
# A test script for learning regular expressions
# When repeating a regular expression, as in a*, the default action is to consume as much of the pattern as possible
import re
string = "hi the\nre hi where"
ex = '(hi.*?hi)'
# Note that '.' will not find across a newline character
c = re.compile(ex)
found = c.findall(string)
if(found):
    print found
    # print found.groups()
    print("len of found is ", len(found))
else:
    print("Not found.")


a = "Abby drools while Jack slurps up her pools"
# If we want to search for the string
search_string = "while.*"
# there are many possible matches for this, including
result1 = "while  "
result2 = "while J"
result3 = "while Ja"
result4 = "while Jac"
# ... and so on.
# However, regular expressions only have two modes: you can either
# find the longest match possible or find the shortest match possible.
result_greedy = "while Jack slurps up her pools"
result_non_greedy = "while"
# note that regular expressions are greedy by nature, but just add
# a question mark after a repeating qualifier to make them non-greedy

