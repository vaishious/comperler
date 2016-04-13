sub Rec {
   my $n;
   $n = $_[0];
   $n = $n + 1;
   $n = $n - 1;

   if( $n > 0 ) {
	Rec( $n - 1 );
	print("Value of n is: %d\n", $n);
   }
   return;
}

Rec(10);

