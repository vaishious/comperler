# Function definition
sub Average{
   # get total number of arguments passed.
   $n = @_;

   $sum = 0;

   foreach $item (@_){
      $sum += $item;
   }
   $average = $sum / $n;

   return $average;
}

# Function call
$num = Average(10, 20, 30);
print("Average for the given numbers : $num\n");
