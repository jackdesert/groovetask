# This is how you change your mac adddress
sudo macchanger wlan0 -r


# Invaluable Tips in the MySql path

# Start by designing and creating your database using phpmyadmin.

# The following commands will start the mysql client, which is installed as a part of XAMPP, but it's not in the system path so but not placed in the 'path' of the linux machine
  cd /opt/lampp/bin
  ./mysql -u root

# note that I logged in as root. That's because when you create a database with phymyadmin, it is owned by root. So log in as root (there's no password required by default in XAMPP), and you will be able to select the database you created.

# Which mysql module?
# http://www.nabble.com/I-updated-DBD-and-broke-some-scripts-td15799789.html explains the outdated 'use Mysql' and the new 'use DBD::Mysql'

# here is a working tutorial:
# http://perl.about.com/od/perltutorials/a/perlmysql_3.htm
# which uses 'use DBI' instead.

#Here's how to change your mac address
# Disable the wifi by right clicking on the library connection -- uncheck "enable wireless"
# sudo macchanger -r wlan0
# and it will give you a new mac address. Reenable wireless, and you're off and running!

# Regular expressions: Want to Win!
=~  apply a regular expression
m/  match
^   beginning of string
$   end of string
/i  case insensitive
/g  global-- (search for all instances -- useful in substitutions)
/gi global and case insensitive
\b is an assertion that the current position is located at a word boundary

my $field = shift;  takes argument #1 and assigns it to the var $field

A energy
B energy
ending time (available until)
for example,
A energy --> writing time (avail until 8am
