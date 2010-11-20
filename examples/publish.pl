#!/opt/lampp/bin/perl

#This script publishes the files to their respective homes on the web. This is even if their homes are "local". Note that this script should be run from the directory which contains both files to be published in one place, and a cgi-bin directory containing files to put in the cgi bin.

# For XAMPP installation
#~ my $dest_dir = "/opt/lampp/htdocs/jack/optimal_website";
#~ my $cgi_dest_dir = "/opt/lampp/cgi-bin";

# For manual Apache2 installation
my $dest_dir = "/var/www";
my $cgi_dest_dir = "/usr/lib/cgi-bin";

# make a system call to copy the files (directories are ignored by this)


if($dest_dir){
    system("cp *.html $dest_dir/.");
    system("cp *.css $dest_dir/.");
    print "\nHTML and CSS files copied to $dest_dir\n";
}else{
    print "\n\nlocation not defined.\n\nCheck Script\n\n";
}

# make a system call to move everything in cgi-bin to the cgi-bin on the server
if($cgi_dest_dir){
    my $temp_var = "cp cgi-bin/*.* $cgi_dest_dir/.";
    print "\nExecutable files in cgi-bin copied to $cgi_dest_dir\n\n";
    system($temp_var);
}
else{
    print "\n\nlocation not defined.\n\nCheck Script\n\n";
}
