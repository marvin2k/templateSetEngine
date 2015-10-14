#!/usr/bin/perl -w

# original source see: https://github.com/ktrask/xml2yaml

# sudo apt-get install libyaml-syck-perl libxml-simple-perl

# better still, use a perl-oneliner, see http://xmltwig.org/talk/stop/img5.html
#
# perl -MYAML -MXML::Simple -e 'print Dump XMLin "woerter.xml"'
#
# does not used sycks implicit typing...

# NOTE:
# - no mixed content
# - the ForceArray option, see http://search.cpan.org/dist/XML-Simple/lib/XML/Simple/FAQ.pod#What_is_the_forcearray_option_all_about?
use XML::Simple;
use YAML::Syck;
use Data::Dumper;

if( ( not defined $ARGV[0]) or ( $ARGV[0] eq "-h" ) or ( $ARGV[0] eq "--help" ) ) {
	print "USAGE: perl xml2yaml.pl file.xml > file.yaml\n";
	exit();
}

# this makes it "hard" to write/read code for the resulting yaml structure...
# too much arrays with only one element.
#
# this can be fixed using "KeyAttr => { template => '+header' }"
#
# by the way, the default for KeyAttr is ['name', 'key', 'id'], so maybe
# just choose our identifiers wisely?
my $data = XMLin( $ARGV[0], ForceArray => 1 );

# Setting this to a true value will make Load recognize various implicit types
# in YAML, such as unquoted true, false, as well as integers and floating-point
# numbers. Otherwise, only ~ is recognized to be undef.
$YAML::Syck::ImplicitTyping = 1;
print Dump( $data );
