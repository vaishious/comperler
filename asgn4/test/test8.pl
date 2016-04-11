sub Rec {
   my $n;
   $n = $_[0];

   if( $n > 0 ) {
        Rec( $n - 1 );
        print("Value of n is: $n\n");
   }
   return;
}

Rec(10);

