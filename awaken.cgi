#!/usr/bin/perl -wT
$ENV{'PATH'} = '/bin:/usr/bin';
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
print '<h2>Awaken Parrot</h2>';

#validate...
my $q = new CGI;
if ($q->param())
{
    if ($q->param('email') !~ /^([a-z0-9._-]+@[a-z0-9._-]+\.[a-z]{2,4}$)/i ) { die("<p>Invalid email</p>"); } # else { print "<p>Valid email</p>"; }
    if ($q->param('parrot') !~ /^([a-z0-9._-])/i ) { die("<p>Invalid parrot</p>"); } # else { print "<p>Valid parrot</p>"; }
}
else
{
    die("<p></p>");
}

require "./lib/Parrot.pm";
my %parrot_settings = getSettings();

print "<p>Email: " . $q->param('email') . "</p>";
print "<p>Parrot: " . $q->param('parrot') . "</p>";

#examine users_file, check again user is entitled, get other users, and get ss percentage
my $found = -1; my $user_ss = 0; my @users = (); my $user_count = 0;
my $f = $parrot_settings{"users_file"};
open(my $fh, "<", $f) || die "Couldn't open '".$f."' for reading because: ".$!;
while(1) 
{
   my $line = readline $fh; chomp $line;
   last unless defined $line;
   if (index ($line,"#") > -1) { next; }
   my @parts = split(',',$line);
   if (@parts[1] eq $q->param('parrot'))
   {  
      $users[$user_count] = @parts[0]; $user_count++;
   }
   if (@parts[1] eq $q->param('parrot') && @parts[0] == $q->param('email'))
   {
      $user_ss = @parts[2];
      $found = 1;
   }
}
close $fh;

if ($q->param('parrot') eq "TestParrot")
{ 
   $user_ss = 100; 
}

if (!$found)
{
die("Not found");
}

#email all users
if ($q->param('parrot') ne "TestParrot")
{
foreach (@users) 
{
   if ($_ eq $q->param('email')) { next; }
   my $to = $_; 
   my $from = 'info@brentc.net';
   my $subject = 'Parrot '.$q->param('parrot').' awakened!';
   my $body = 'This is a notification that '.$q->param('email').' has awoken this Parrot. ';
   $body .= 'This means the Parrot has emailed some or all of its secret to '.$q->param('email').'. ';
   $body .= 'You are being notified because your email is also able to wake this Parrot ';
   $body .= 'so that you can investigate or take any action as required. ';
   $body .= 'Link: '.$parrot_settings{"parrot_roost"};;   
   sendEmail($to , $from ,$subject, $body ); 
   print "<p>Notification mail(s) sent to other users."."</p>";
}
}

#get secret
my $secret=""; 
my $d = $parrot_settings{"data_directory"};
$f = $d.'/'.$q->param('parrot');
if (!(-e $f)) { die("Parrot not found."); }
#print '<p>Parrot file:'.$f.'</p>';
open(my $fh, "<", $f) || die "Couldn't open '".$f."' for reading because: ".$!;
while(1) 
{
   my $line = readline $fh; chomp $line;
   last unless defined $line;
   $secret .= $line;
}
close $fh;

#prepare for email secret%
my $to = $q->param('email');
my $from = 'info@brentc.net';
my $subject = 'Parrot '.$q->param('parrot').' says';
my $body = $secret;

#default to whole secret
my $length = length($body);
my $start = 0;
my $chars = $length;

#check log file for previous requests 
my $logfile = $parrot_settings{"log_file"};
if (!(-e $logfile)) 
{ 
   print("<p>Log file not present.</p>");
}
else 
{
   #print '<p>Log file:'.$logfile.'</p>';
   open(my $fh, "<", $logfile) || die "Couldn't open '".$f."' for reading because: ".$!;
   my $break = -1;
   while(1) 
   {
      my $line = readline $fh; chomp $line;
      last unless defined $line;
      #parse log values
      my ($datetime,$user,$parrot,$ss) = split(',',$line);
      my $this_start = int(substr($ss,index($ss,'(')+1));
      my $this_chars = int(substr($ss,index($ss,'+')+1));     
      if ($q->param('parrot') ne "TestParrot")
      {
         #user already woken this parrot? - resend same ss part
         if ($parrot eq $q->param('parrot') && $user eq $q->param('email'))
         {
            print '<p>'.$q->param('email').' has previously woken this Parrot - using same secret share.</p>';
            $start = $this_start; $chars = $this_chars;
           $break = 1;
         }
         #parrot already woken? - modify start of next ss 
         if ($break ne 1 && $parrot eq $q->param('parrot'))
         {
             print '<p>'.$q->param('parrot').' previously woken, adjusting secret share.</p>';
             $start = $this_start + $this_chars;
            if ($start > $length-1) { $start = 0; } #loop around if necessary
         }  
      } 
   }
   close $fh;
}

if ($q->param('parrot') eq "TestParrot") #TestParrot always outputs whole secret, reset $start
{
   print '<p>TestParrot defaulting to whole secret.</p>';
   $start = 0; $chars = $length;
}

#apply user_ss
$user_ss = int($user_ss);
my $ss_message = "";
if ($user_ss < 100)
{
  $chars = int($length * $user_ss / 100);
   if ($start + $chars > $length){ $chars = $length - $start + 1; } #truncate if necessary
   $ss_message = 'User secret share percentage: '.$user_ss.'% (from char '.$start .' for '. $chars .' chars)'."\n";
}

#get ss share
$body = substr($body,$start,$chars);

if ($ss_message ne "")
{
   $body = $ss_message . $body;
   print '<p>'.$ss_message.'</p>';
}

if ($q->param('parrot') eq "TestParrot") #TestParrot outputs to screen only
{
   print '<i>'.$body.'</i>';
}
else
{
   #print '<i>'.$body.'</i>';
   sendEmail($to , $from ,$subject, $body ); 
   print "<p>Mail should have been sent to:".$q->param('email')."</p>";
}

#update log file
#untaint $logfile;
$logfile =~ m/^([a-zA-Z0-9\._\/]+)$/ or die "Untaining error";	
my $file = "$1";	# Assign untainted data
open(my $fh, ">>", $file) || die "Couldn't open '".$f."' for writing because: ".$!;
my $log = 1;
if ($log == 1)
{
   #datetime,#user,#parrot,#ss_percent (#start..#end)
   (my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst)=localtime(time);
   printf $fh "%4d-%02d-%02d %02d:%02d:%02d",$year+1900,$mon+1,$mday,$hour,$min,$sec;
   print $fh ','.$q->param('email').','.$q->param('parrot').','.$user_ss.'% '.'('.$start.'+'.$chars.')'."\n";
   print '<p>Log file updated.</p>';
}
close $fh;


print qq^
<div id="footer" style="width: 100%; position: absolute; top: 90%; text-align: center;">by: <a href="http://brentc.net">www.brentc.net</a>&nbsp;|&nbsp;<a href="readme.cgi">readme</a></div>
^;

print '</body>';
print '</html>';

1;