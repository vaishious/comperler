my $b;
$b = 1;
HOLA: while ((1 > 0)) {
    while ((1 > 0)) {
        $b = 0;
        next;
        $b = 1;
    }
} continue {
    $b = $b + 1;
}

$b = $b + 1;
