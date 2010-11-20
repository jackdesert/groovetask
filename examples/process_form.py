#!/usr/bin/env python

import cgitb
cgitb.enable()

import cgi
form = cgi.FieldStorage() # instantiate only once!
name = form.getfirst('name', 'empty')

# Avoid script injection escaping the user input
name = cgi.escape(name)

#~ # Original Python 2.6 code
#~ print """\
#~ Content-Type: text/html\n
#~ <html><body>
#~ <p>The submitted name was "%s"</p>
#~ </body></html>
#~ """, % name

# Working Python 2.6 code
print """\
Content-Type: text/html\n
<html><body>
<p>The submitted name was </p>
</body></html>
""", name

# Python 3.1 code in single-line fashion. (How does 3.1 do multi?)
#~ print("Content-Type: text/html\n")
#~ print("<html><body>\n")
#~ print("<p>The submitted name was \"", name, " </p>")
#~ print("</body></html>")
