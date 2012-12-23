#!/usr/bin/perl -wT
use strict;
use warnings;
use CGI;
#use CGI::Carp qw(warningsToBrowser fatalsToBrowser); 

print "Content-type: text/html\n\n";
print '<!DOCTYPE HTML>';
print '<html>';
print '<head>';
print '<title>Sleeping Parrots Readme</title>';
print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />';
print '<meta name="copyright" content="www.brentc.net"/>';
print '<meta name="licence" content="GPL"/>';
print '<link rel="icon" href="/media/parrot-media/favicon.png" type="image/png"/>';
print '</head>';

print '<body>';

print '<a href="index.cgi" title="Parrot home">Roost</a>';

print '<h1>Sleeping Parrots</h1>';
print '<h2>README</h2>';

print '<pre>';
my $f = "README";
open(my $fh, "<", $f) || die "Couldn't open '".$f."' for reading because: ".$!;
while(1) 
{
   my $line = readline $fh; 
   last unless defined $line;   
   print $line;
}
close $fh;
print '</pre>';

print qq^
<div id="footer" style="width: 100%; text-align: center;">by: <a href="http://brentc.net">www.brentc.net</a>&nbsp;|&nbsp;<a href="readme.cgi">readme</a></div>
^;

print '</body>';
print '</html>';
