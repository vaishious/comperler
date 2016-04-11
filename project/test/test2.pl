my $b = 5;
my $a = 0;
my $sum = 0;

while ($a < $b) {
    my $c = 0;
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

print ("A wrong cube of %d is %d\n", $b, $sum);

my $ref = \$sum;
print ("Address : %d, Value : %d\n", $ref, $$ref);




