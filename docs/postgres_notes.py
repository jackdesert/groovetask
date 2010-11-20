# Note that when you first install PostgreSQL, the only user that seems
# to work is 'postgres'. This user will exist but will probably not show
# up in the GUI version of Add Users. So, just change the password on hte
# 'postgres' account so you can use it
# Note: my current 'postgres' password is '123567'

    sudo passwd postgres
# and it will ask you (twice) what you want the new password to be

# Then log in as 'postgres'
    su postgres
# and then you can create a database
    createdb [database_name]

# To start adding data to the database, use the program 'psql'
# Do this while still logged into your console as 'postgres'
    psql [database_name]

Note that your prompt will look like
[database_name=#]

# General observations:
It appears that psql is case-INsensitive

# Be specific!
# 1. While SELECT * is useful for off-the-cuff queries, it is widely
# considered bad style in production code, since adding a
# column to the table would change the results.

'Sorting Order'
# You can return your query sorted in ascending or descending order
ORDER BY first_att ASC
# or
ORDER BY first_att DESC

'Atomic Transactions'
# A transaction is said to be atomic: from the point of view of other
# transactions, it either happens completely or not at all.

'Primary Keys'
# Yes, primary keys can be updated. They must still be unique, even
# inside a transaction. Perhaps setting the first value to a very large
# number and then back again would work;


'Modules'
# Install the module you need -- I Installed the module named pyPgSQL
sudo apt-get install python-pgsql
# Since python2.6 seems to be the one that is offically supported by
# default on Ubunto 9.04, when I run python2.6, the import line works:
from pyPgSQL import libpq  # This is the C library that it runs off of
- pyPgSQL is a package of two modules that provide a Python DB-API 2.0
- compliant interface to PostgreSQL databases. The first module, libpq,
- exports the PostgreSQL C API to Python. This module is written in C and
- can be compiled into Python or can be dynamically loaded on demand. The
- second module, PgSQL, provides the DB-API 2.0 compliant interface.

from pyPgSQL import PgSQL # This is the DB-API2.0 interface
or
from pyPgSQL import PgSQL as dbapi2
'this one works too!'
db = dbapi2.connect (database="mine", user="postgres", password="123567")
cur = db.cursor()

from pyPgSQL import libpq
from pyPgSQL import PgSQL
con = PgSQL.connect(None, "postgres", "123567", "localhost", "mine")

'this one works!'

x = PgSQL.connect(database="mine", client_encoding="utf-8", \
    unicode_results=1, password = '123567', user = 'postgres')
