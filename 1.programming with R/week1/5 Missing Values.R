x <- c(44, NA, 5, NA)
x * 3
y <- rnorm(1000, mean = 0, sd = 1)
z <- rep(NA,1000)
my_data <- sample(c(y, z), 100)#select 100 elements at random from these 2000 values (combining y and z)
my_na <- is.na(my_data)
sum(my_na)

0/0
Inf - Inf
