my $a;
$a = 10;
while( $a < 20 ){
   if( $a == 15)
   {
       $a = $a + 1;
       last;
   }
   print("value of a: $a\n");
   $a = $a + 1;
}

