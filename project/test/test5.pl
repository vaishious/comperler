#!/usr/bin/perl

my %data;
%data = ("abcd" => 1000, 1000 => 30, "Kumar" => 40, "Pqrs" => "MNOP");
print("%s\n",$data{"Pqrs"});
#$data{"abcd"} = $data{"abcd"} * 16;
print("%d\n",$data{"abcd"});
