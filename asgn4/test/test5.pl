my $a;
my $b;
my $c;
  
$a = 0;

A:while($a < 3){
   $b = 0;

   if($a == 2) {
	redo B;
   }
   B:while( $b < 3 ){
      print("value of a = $a, b = $b\n");
      $b = $b + 1;
      if($b == 2) {
	last C;
      }
      $c = 3;

      C:while( $c > 0) {
	 print("value of c = $c");
      	 if($c == 2) {
	    next A;
         }
	 $c = $c - 1;
      }
   }
   $a = $a + 1;
   print("Value of a = $a\n");
}
