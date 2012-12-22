#!/usr/bin/perl -wT
use strict;
use warnings;
use CGI;
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser); 

print "Content-type: text/html\n\n";
#print '<!DOCTYPE HTML>';
#print '<html>';
#print '<body>';

#determine path of script (whether running as .cgi or an SSI include)
my $path = $ENV{'SCRIPT_NAME'};
if (rindex($path,"/") < 0) { $path = '.'; } else { $path = substr($path,0,rindex($path,"/")); }

print '<h1>Sleeping Parrots</h1>';

print qq^
<p>There are sleeping Parrots that have secrets. Users are linked to Parrots by email address. A user can wake a Parrot which will then email its secret to the user. Other users linked to that Parrot will be notified that it has been awakened.</p>
^;

print qq^
<p>Note: This is experimental software that provides convenience more than security- use with caution. See <a href="readme.cgi">README</a> for more info.</p>
^;

print qq^
<p>Enter your email address to find your parrot(s):</p>
^;

print '<form method="post" action = "'.$path.'/'.'parrots.cgi">';
print '<input type="email" name = "email" maxsize="256" size="30" required />';
print '<input type="submit" name = "submit" value="submit" />';
print '</form>';

print qq^
<div id="footer" style="width: 100%; position: absolute; top: 90%; text-align: center;">by: <a href="http://brentc.net">www.brentc.net</a>&nbsp;|&nbsp;<a href="readme.cgi">readme</a></div>
^;

#print '</body>';
#print '</html>';
