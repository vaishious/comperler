my $b = 11;
my $a = 0;
my $sum = 0;
my $efg = "abcdef";
my $rty = 10;

while ($a < $b) {
    my $c = 0;
    my $hola = $efg | $rty;
    while ($c < $b) {
        my $d = 0;
        while ($d < $b) {
            $d += 1;
            $sum = $sum + 1;
        }
        $c += 1;
    }
    $a += 1;
}

print ("The cube of %d is %d\n", $b, $sum);

my $ref = \$sum;
print ("Address : %d, Value : %d\n", $ref, $$ref);




