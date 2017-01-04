y <- rnorm(1000, mean = 0, sd = 1)
z <- rep(NA,1000)
my_data <- sample(c(y, z), 100)#select 100 elements at random from these 2000 values (combining y and z)
my_na <- is.na(my_data)
my_data[1:10]
my_data[my_na]
my_data[!my_na]
my_data[!is.na(my_data) & my_data > 0]
my_data[0]
my_data[400000000000000]
my_data[c(-4, -8)]
my_data[-c(4, 8)]
vect <- c(foo = 11, bar = 2, norf = NA)
names(vect)
vect2 <- c(11, 2, NA)
names(vect2) <- c('foo', 'bar', 'norf')
identical(vect, vect2)
vect['bar']
vect[c('foo', 'bar')]


