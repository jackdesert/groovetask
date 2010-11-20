########################################################################
#### A    S H O R T    P R O O F    O F    C O N N E C T I V I T Y #####
########################################################################
############ INSIDE BASH #############
# Set 'python' to point to '/usr/in/python2.6
cd /usr/bin/
sudo ln-s python2.6 python
# Install postgresql
sudo apt-get install postgresql
# Install the python-postgreql driver, named pyPgSQL
sudo apt-get install python-pgsql
# When you installed postgresql, a user was created on your Linux system
# with the username 'postgres'. However, you don't know what the
# password is, so change it to something you know.
sudo passwd postgres
# It will ask you to put in the new password twice.
# From Command prompt (bash) , login as this new user 'postgres'
su postgres
# provide the password, which is currently set to '123567'
# Create a database
createdb [database_name]    # database_name is jackdesert_groove
# While still logged into the console as 'postgres', run the pgsql
# program, which will return a prompt with the name of your database
psql [database_name]

############ INSIDE PSQL ###############
# While in psql, create a table named weather and put some data in it
# (Menu.py has the real version of this)
CREATE TABLE weather(
f1 int, -- a number
f2 int  -- another number
);
INSERT INTO weather VALUES (150,2);
# Hit <ctrl> -d to exit out of psql

############# INSIDE BASH ##############
# Note that by default, postgresql only allows connections from users
# who log into postgresql with the same-named login as their Linux-box
# login. In order to allow any Linux user to log in as any other
# postgres user, here is what you need to do:
#Edit the PostgreSQL client authentication configuration file
sudo gedit /etc/postgresql/8.4/main/pg_hba.conf
# Change the line that reads:
local   all     all     ident

# so that it reads
local   all     all     md5
# Now restart the server. On Ubuntu instead of the usual pg_ctl, we
# must log in as user 'postgres
su postgres
# and run
/etc/init.d/postgresql-8.4 restart
# I still don't know what the process is called ;)
# Now you can execute 'psql' from whatever Linux user name you want,
# using the -U option to specify your PostgreSQL login
# note that to change a password, user "ALTER ROLE username WITH PASSWORD 'new_password'"
# Make sure your user can log in manually using
# psql -U USERNAME DATABASENAME before you try using scripts to do the same thing

# See chapter 20 of the PostgreSQL8.4 user guide
# Now to grant a few privileges to 'test_user' so he can actually
# manipulate a little data
su postgres
psql mine
############# INSIDE PSQL
CREATE USER test_user WITH PASSWORD '123567';
GRANT CONNECT ON DATABASE mine TO test_user
GRANT ALL [PRIVILEGES] ON [TABLE] weather TO test_user
# note tha the words within the [brackets] are optional-- you must take
# out the brackets.

# While still logged into the console as 'postgres',
# Run python2.6 (the version of python for which the pyPgSQL is compiled)
python2.6

############# INSIDE PYTHON2.6 #########
# From within python2.6:
# import the C library of pyPgSQL
from pyPgSQL import libpq
# import the DBAPI2.0 intervace of pyPgSQL
from pyPgSQL import PgSQL
# Connect to the database. Make sure you have already created the
# database and that there is a table named 'weather', and that you
# really have at least one row inserted into the table 'weather'
db = PgSQL.connect (database="mine", user="test_user", password="123567")
cur = db.cursor()
# Okay, I changed my mind. This actually has code in it to create the
# table named 'weather' and put some data into it. Note that if
# 'weather' already exists, it WILL overwrite it
# cur.execute ("""CREATE TABLE weather(f1 int, f2 int)""")
cur.execute("INSERT INTO weather VALUES (150,4)")
cur.execute("INSERT INTO weather VALUES (150,4)")
cur.execute("INSERT INTO weather VALUES (150,4)")
cur.execute("INSERT INTO weather VALUES (160,10)")
# After you INSERT data into the database, you must commit it before any
# external transactions can see it
db.commit()
cur.execute("SELECT * FROM weather")
# fetch a result set
result = cur.fetchmany(10)
print(result)
######################## END PROOF OF CONNECTIVITY######################
########################################################################





