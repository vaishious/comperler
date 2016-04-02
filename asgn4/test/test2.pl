my $a = 10;
my $b = 20;
my $c;
my $d;
$c = $a + $b;
$c = $c - $b;
$c = $c * $a;
$d = ((1 > 0) && (2 > 0));
unless (!(1 < 0)) {
    $c = 10;
} elsif (2 > 0) {
    $c = 20;
} elsif (3 > 0) {
    $c = 40;
} else {
    $c = 50;
}
