# First, to get a basic python executable to run on the server:
chmod 711 file_name.py
# Then make sure you can log in using ssh and execute the file.
# If it runs fine in the terminal, and if it has the proper
# carriage returns after text/plain, it should work.
    #! /usr/bin/env python
    print "Content-type: text/plain\n\n"
    print "hello Jack Desert's World!"

##########  EXAMPLE   ##############################
# To get mod_wsgi to run locally, first install mod_wsgi.
# sudo apt-get install libapache2-mod-wsgi
# Then add these two lines to /etc/apache2/httpd.conf:
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
WSGIScriptAlias /myapp /home/jd/py_website/wsgi_examples/mod_wsgi_example.py

################  THE REAL THING  ###################
# Then add these two lines to /etc/apache2/httpd.conf:#
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
WSGIScriptAlias / /home/jd/py/webfiles/index.py
# Add a server name so you don't get warnings about no name
ServerName "Jacks_Server"
# Add the UTF-8 charset so you can type ñ and other symbols.
AddDefaultCharset UTF-8

# Also, add this line to apache2/conf/httpd.conf ON THE SERVER:
AddDefaultCharset UTF-8




LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
WSGIScriptAlias / /home/jd/py/webfiles/index.py

# To get rid of the "no name" warning, give the server a name:
ServerName "Jacks_Server"

#############  INSTALLING PYTHON MODULES  ###################
sudo apt-get install python-setuptools
sudo easy_install pesto
# Then go to proof_of_connectivity.py and install the database modules



# Then a file named mod_wsgi_example.py that looks like this:
def application(environ, start_response):
    status = '200 OK'
    output = 'Hello World! Jack Here!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

# will execute when you go to http://localhost/myapp

# To get mod_wsgi to run on a webfaction.com server, first create the
# application. The type is mod_wsgi 2.5/python2.5
# It will automatically come with index.py which contains the
# def application() call.
# Now create a "website" using the webfaction.com panel.
# The subdomain must be assigned correctly. Tell the
# subdomain jackdesert.webfactional.com to use the application you
# just created, and tell it the path is /path_to_app
# Then go ot jackdesert.webfactional.com/path_to_app and the results
# of index.py will show up.

# To debug locally, simply type
tail -f  /var/log/apache2/error.log
# To debug on the server,
tail -f ~/logs/user/error_groove_log

