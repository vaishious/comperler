sub Rec {
	my $n;
	$n = $_[0];
	$n = $n + "1";
	$n = "1" - $n;
	$n = -$n;
	$n = $n * "100";
	$n = $n / "100";

	if( $n > 0 ) {
		Rec( $n - 1 );
		print("Value of n is: %d\n", $n);
	}
	return $n;
}

sub DiffRet {
	my $a;
	$a = $_[0];
	if($a eq "hash") {
		return (100 => "flkjsdlfk", "1000" => 239, "ghsk" => 9);
	}
	elsif($a eq "array"){
		return (1,2,3,4,"dkfjldkf");
	}
	elsif($a eq "str"){
		return "TEST STRING";
	}
	elsif($a eq "int"){
		return 10001;
	}
	else {return 0;}
}

my $hdf = Rec(10);
my %b = DiffRet("hash");
my @c = DiffRet("array");
my $d = DiffRet("str");
my $e = DiffRet("int");

print ("\nMATCHING VALUES:\n239 = %d?\ndkfjldkf = %s\nTEST STRING = %s\n10001 = %d\n", $b{1000}, $c[4], $d, $e);

my $a = 100 . 8989;
print ("1008989 = %s\n",$a);

my $b = 1090 x "2";
print ("10901090 = %s\n",$b);
