TRUE & c(TRUE, FALSE, FALSE)
TRUE && c(TRUE, FALSE, FALSE)#is only evaluated with the first member of the right operand (the vector)
TRUE | c(TRUE, FALSE, FALSE)
TRUE || c(TRUE, FALSE, FALSE)
isTRUE(6>4)
xor(5 == 6, !FALSE) #  xor() to evaluate to TRUE, one argument must be TRUE and one must be FALSE
ints <- sample(10) # The vector `ints` is a random sampling of integers from 1 to 10 without replacement
which(ints >7)
any(ints < 0)
all(ints > 0)
