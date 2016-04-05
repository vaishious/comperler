my $b = 5;
my $a = 0;
my $sum = 0;

while ($a < $b) {
    my $c = 0;
    while ($c < $b) {
        my $d = 0;
        while ($d < $b) {
            $sum = $sum + 1;
            $d += 1;
        }
        $c += 1;
    }
    $a += 1;
}

print ("Cube of %d is %d\n", $b, $sum);


