# Testing printing of hashes, arrays and nested hashes and arrays
my %h = (123 => "abcd", 456 => "efgh", 789 => "ijkl");
my @a = (1,2,3,%h);
my %hout = ("inner-array" => @a, "inner-hash" => %h);

print("Array is: %a\n",@a);
print("Hash is: %h\n",%hout);
print("Inner hash is: %h\n",$hout{"inner-hash"});
