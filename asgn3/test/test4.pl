sub parg {
    $a = @_[0];
    $b = @_[1];
    $c = @_[2];
    print("A: $a $b $c\n");
    print("B: $#_ [@_]\n\n");
}

parg("Hi", "there", "fred");

@a1 = ("Today", "is", "the", "day");
parg(@a1);

parg("Me", @a1, "too");

$joe = "sticks";
parg ("Pooh $joe");

parg();

@a2 = ("Never", "Mind");
parg (@a2, "Boris", @a1, $joe);
