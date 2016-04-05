my $b = 1;
my $a = 1;
while ($b < 5) {
   $a = $a * $b;
   $b++;
} 

print("Factorial of %d = %d\n", $b - 1, $a);
