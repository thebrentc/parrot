## Parrot Common functions ##

sub getSettings
{
   my %parrot_settings= {};
   my $f = "parrot.ini";
   open(my $fh, "<", $f) || die "Couldn't open '".$f."' for reading because: ".$!;
   while(1) 
   {
      my $line = readline $fh;
      last unless defined $line;
      if (index ($line,"#") > -1) { next; }
      if (index ($line,"=") > -1)
      {
         chomp $line;
         my @parts = split('=',$line);
         $parrot_settings{@parts[0]}=@parts[1];
      }
   }
   close $fh;
   return %parrot_settings;
}

 sub sendEmail
 {
 	my ($to, $from, $subject, $message) = @_;
 	my $sendmail = '/usr/lib/sendmail';
 	open(MAIL, "|$sendmail -oi -t");
 		print MAIL "From: $from\n";
 		print MAIL "To: $to\n";
 		print MAIL "Subject: $subject\n\n";
 		print MAIL "$message\n";
 	close(MAIL);
 } 

#print "Parrot.pm included";
return 1;