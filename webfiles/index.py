#!/usr/bin/env python
# Note that this script now uses mod_wsgi. You must install mod_wsgi and
# configure apache2 to load it as a module. you must also put the
# following line:
# WSGIScriptAlias /groove /home/jd/py_website/cgi-bin/plan_your_day.wsgi
# in httpd.conf. Restart apache using
# sudo apache2ctl restart
# then to view the output, go to http://localhost/groove

import sys
sys.path = ['/home/jd/py/webfiles/include',
            '/home/jackdesert/webapps/groove/lib/include',
            '/usr/local/lib/python2.5/site-packages/MySQL_python-1.2.2-py2.5-linux-i686.egg'] + sys.path
from cgi import parse_qs, escape
from pesto.cookie import Cookie
from pesto.request import Request
from pesto.response import Response
import Menu
import Task
import Key
from plain_functions import pr
from fancy_functions import technical_form
from fancy_functions import colloquial_form
from fancy_functions import large_form
from fancy_functions import display_tasks_from_database
from Logic import display_groove_select
from Logic import work_it
from Logic import declare_task_done
from Logic import display_login
from Logic import display_greeting
from text import introduction


import cgitb
cgitb.enable()


basic_html = "<html><head>\n"
basic_html += "<title>GrooveTask - A Better Way to Plan Your Day</title>\n"
basic_html += "<link rel='stylesheet' type='text/css' href='styles.css\n'>"
basic_html += "</head><body>\n"

def application(environ, start_response):
    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
       request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
       request_body_size = 0

    # When the method is POST the query string will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)

    in_category = d.get('category', [''])[0] # Returns the first age value.
    if ((in_category == None) | (in_category == '')):
        in_category = 1

    # hobbies = d.get('hobbies', []) # Returns a list of hobbies.
    # in_priority = d.get('priority', [''])[0] # Returns the first age value.
    in_priority = d.get('priority', [''])[0] # Returns the first age value.
    in_min_minutes = d.get('min_minutes', [''])[0] # Returns the first age value.
    in_max_minutes = d.get('max_minutes', ['NULL'])[0] # Returns the first age value.
    in_doors_open_time = d.get('doors_open_time', [''])[0] # Returns the first age value.
    in_doors_close_time = d.get('doors_close_time', [''])[0] # Returns the first age value.
    in_do_at_exactly_time = d.get('do_at_exactly_time', [''])[0] # Returns the first age value.
    in_description = d.get('description', [''])[0] # Returns the first age value.
    in_username = d.get('username', [''])[0]
    in_username = escape(in_username).replace(';', '')  # No semicolons
    in_password = d.get('password', [''])[0]
    in_password = escape(in_password).replace(';', '')  # No semicolons
    in_seconds = '0'
    in_add_to_cat = d.get('add_to_cat', [''])[0] # Add a task to this category

    new_Task = Task.Task([in_category, in_priority, in_min_minutes,
            in_max_minutes, in_doors_open_time, in_doors_close_time,
            in_do_at_exactly_time, in_description, in_seconds])


   # If the Submit Button was clicked, insert the new task
    in_sbutton = d.get('sbutton', [''])[0]
    in_gbutton = d.get('gbutton', [''])[0]
    in_Lbutton = d.get('Lbutton', [''])[0]
    in_up_down = d.get('up_down', [''])[0]
    in_pri_key_string = d.get('pri_key', [''])[0]
    if (in_pri_key_string != ''):
        in_key = Key.Key(in_pri_key_string)
    #~ pr('in_pri_key_string is ' + in_pri_key_string)
    task_to_edit = '999_999' # Dummy value that won't match


    request = Request(environ)
    username_cookie = request.cookies.get('username_cookie')
    password_cookie = request.cookies.get('password_cookie')
    #~ pr("username_cookie is " + str(username_cookie))
    #~ pr("password_cookie is " + str(password_cookie))
    #~ pr("in_username is " + in_username)
    #~ pr("in_password is " + in_password)
    val_menu = Menu.Menu(999)
    cookies = []

    if(in_Lbutton == 'register'):
        userid = val_menu.create_user(in_username, in_password)
        if(in_username == ''):
            message = "<p style='color: blue;'>Enter your desired username and password, then click <i>Register</i> again.</p>"
        elif(userid):
            message = """Thank you for creating an account with us. Please
                    enjoy GrooveTask.com<br>"""
            cookies = [('Set-Cookie', 'username_cookie = ' + in_username),
                    ('Set-Cookie', 'password_cookie = ' + in_password)]
        else:
            message = """Great Taste! But someone already chose that
                    username. Please try your next-favorite name"""
    elif(in_Lbutton == 'logout'):
        if ((username_cookie) and (password_cookie)):
            in_username = username_cookie.value
            in_password = password_cookie.value
            logout_userid = val_menu.validate(in_username, in_password)
            #~ pr('logging out, so clearing cur_task')
            if(logout_userid):
                logout_Menu = Menu.Menu(logout_userid)
                logout_Menu.update_seconds()
                logout_Menu.clear_cur_task()
        # Now clear everything out
        userid = None
        cookies = [('Set-Cookie', 'username_cookie = none'),
                ('Set-Cookie', 'password_cookie = none')]
        message = """You are successfully logged out. Thank you for
                using GrooveTask. Please come again."""
    elif(in_username != ''):
        userid = val_menu.validate(in_username, in_password)
        cookies = [('Set-Cookie', 'username_cookie = ' + in_username),
                ('Set-Cookie', 'password_cookie = ' + in_password)]
        #~ pr ('logging in through form data')
        if(userid):
            message = ''    #"You are logged in! Enjoy Grooves!"
        else:
            message = """I'm sorry. The username/password you entered
                        failed. Please try again"""
    elif ((username_cookie) and (password_cookie)):
        in_username = username_cookie.value
        in_password = password_cookie.value
        userid = val_menu.validate(in_username, in_password)
        pr ('cookie access by user: ' + in_username)
        message = 'Please Log In'
        if(userid):
            message = ''
    else:
        userid = None
        message = """First-Timers are always welcome here!"""

####################################################################
###########   S T A R T    S E C O N D    B I G    L O O P  ########
    if(userid != None):
        #~ pr('inside userid!=None sequence')
        #~ pr('in_sbutton is  ' + in_sbutton)
        new_Menu = Menu.Menu(userid)
        if (in_sbutton == 'Clean Slate'):
            try:
                new_Menu.reset_table(in_add_to_cat)
            except:
                pr('ERROR: wrong in_add_to_cat passed to reset_table()')
                pr('in_add_to_cat is ' + in_add_to_cat)
            in_add_to_cat = ''  # clear this so input form not displayed
        elif (in_sbutton == 'Submit'):
            new_Task.set_priority(new_Menu.get_next_priority(int(in_category)))
            new_Menu.insert_task(new_Task)  # Insert once
            #~ pr('inside submit sequence')
        elif (in_sbutton == 'Update'):
            new_Menu.update_task(new_Task, in_pri_key_string)
            #~ pr('inside update_task sequence')
        elif(in_sbutton == 'Delete'):
            #~ pr('inside delete sequence')
            new_Menu.delete_task(in_pri_key_string)
        elif (in_up_down == 'up'):
            #~ pr('inside up sequence')
            new_Menu.bump_priority(in_key.get_cat(),
                in_key.get_pri(), in_key.get_pri() -1)
        elif (in_up_down == 'bump'):
            #~ pr('inside down sequence')
            new_Menu.bump_priority(in_key.get_cat(),
                in_key.get_pri(), 1)
        elif (in_up_down == 'edit'):
            #~ pr('inside edit sequence')
            task_to_edit = in_pri_key_string
        else:
            pass
            #~ pr('No options matched')

        title = "<h1>Plan Your Day!</h1>"
        greeting =  title + display_greeting(in_username)
        go_to_work = display_groove_select()
        add_a_task =  large_form(None)
        task_data = display_tasks_from_database(new_Menu, task_to_edit, in_add_to_cat)
        response_body = basic_html + greeting + message + task_data + go_to_work
    else:
        response_body = basic_html + display_login(message) + introduction()
    title = "<h1>Go to Work!</h1>"
    greeting = basic_html + title + display_greeting(in_username)
    if(in_gbutton == 'A-Energy'):
        response_body = greeting + work_it(new_Menu, 1)
        pr('hello from A')
    elif(in_gbutton == 'B-Energy'):
        response_body = greeting + work_it(new_Menu, 2)
        pr('hello from B')
    elif(in_gbutton == 'R-Ejuvenate'):
        response_body = greeting + work_it(new_Menu, 3)
        pr('hello from R')
    elif(in_gbutton == 'task_done'):
        declare_task_done(new_Menu, in_pri_key_string)
        response_body = greeting + work_it(new_Menu, in_key.get_cat())
        pr('hello from task_done')
    elif(userid != None):   # make sure you account for time and clear cur_task when you 'Plan Your Day'
        new_Menu.update_seconds()
        pr(' line 210    For some reason this entire script is running twice. ')
        new_Menu.clear_cur_task()
        pr(' line 212    And the second time through it clears cur_task and then it cant do shit. Why?')
        # Note this runs any time you are still logged in

    status = '200 OK'
    response_headers = cookies + [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]


if __name__ == '__main__':
    pr('a helluva lotta love coming from that abbers ;)')
