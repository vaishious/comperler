#!/usr/bin/perl

# Testing Hashes
my %data;
my $var = 101;
%data = ("abcd" => "1234", 1000 => 30, "Kumar" => 40, "Pqrs" => "MNOP");

$data{"abcd"} = $data{"abcd"} x 3;
$data{"Pqrs"} = $data{"Pqrs"} . $data{"Pqrs"};
$data{"Kumar"} = $var;

print("%s\n",$data{"abcd"});
print("%d\n",$data{1000});
print("%d\n",$data{"Kumar"});
print("%s\n",$data{"Pqrs"});



# Testing references
my $a = 10;
my $aref;
$aref = \$a;
my $dataref = \%data;
$a = 20;
print("Modified value of $a is : %d\n",$$aref);
