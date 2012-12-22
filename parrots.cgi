#!/usr/bin/perl -wT
use strict;
use warnings;
use CGI;
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser); 

print "Content-type: text/html\n\n";
print '<!DOCTYPE HTML>';
print '<html>';
print '<body>';

print '<a href="index.cgi" title="Parrot home">Roost</a>';

print '<h1>Sleeping Parrots</h1>';
print '<h2>Your Parrots</h2>';

#validate...
my $q = new CGI;
if ($q->param())
{
    # Parameters are defined, therefore the form has been submitted
    if ($q->param('email') !~ /^([a-z0-9._-]+@[a-z0-9._-]+\.[a-z]{2,4}$)/i ) { die("<p>Invalid email</p>"); } # else { print "<p>Valid email</p>"; }
}
else
{
    die("<p>Enter an email address</p>");
}

require "./lib/Parrot.pm";
my %parrot_settings = getSettings();
#print "<p>Users file:" . $parrot_settings{"users_file"} . "</p>";

print "<p>Email: " . $q->param('email') . "</p>";

print qq^
<p>NOTES:<br/>
An awakened parrot will email its secret data to the user that woke it up.<br/>
Awakening a parrot will email all other users linked with that parrot notifying that the parrot has been awakened.<br/>
The parrot may have been told to divide the secret amongst users, so more than one user may be needed to fully recover the full secret.<br/>
</p>
^;

print qq^
<h4>Choose Parrot to wake:</h4>
^;


#examine users_file, outputing available parrots for user
my $f = $parrot_settings{"users_file"};
open(my $fh, "<", $f) || die "Couldn't open '".$f."' for reading because: ".$!;
while(1) 
{
   my $line = readline $fh; chomp $line;
   last unless defined $line;
   if (index ($line,"#") eq 0) { next; }
   (my $user,my $parrot,my $user_ss) = split(',',$line); 
   if ($user eq $q->param('email') || $parrot eq "TestParrot" )
   {
      print '<form method="post" action = "awaken.cgi">';
      print '<input type="hidden" name = "email" value="'.$q->param('email').'" />';	
      print '<input type="hidden" name = "parrot" value="'.$parrot.'" />';	
      print $parrot;
      print '&nbsp;';
      print '<input type="submit" name = "submit" value="Wake this parrot" />';
      print '</form> ';
   }
}
close $fh;

print qq^
<p>(Test Parrot can be woken by any user, doesn't send notification emails, gives full secret and outputs to the screen rather than emailing).
</p>
^;

print qq^
<div id="footer" style="width: 100%; position: absolute; top: 90%; text-align: center;">by: <a href="http://brentc.net">www.brentc.net</a>&nbsp;|&nbsp;<a href="readme.cgi">readme</a></div>
^;

print '</body>';
print '</html>';

1;