my_vector <- 1:20
length(my_vector)
dim(my_vector) <- c(4, 5)
dim(my_vector)
attributes(my_vector)
class(my_vector)
my_matrix <- my_vector
my_matrix2 <- matrix(1:20, nrow = 4, ncol = 5)
identical(my_matrix, my_matrix2)
patients <- c('Bill', 'Gina', 'Kelly', 'Sean')
cbind(patients, my_matrix)
my_data <- data.frame(patients, my_matrix)
cnames <- c('patient', 'age', 'weight', 'bp', 'rating', 'test')
colnames(my_data) <- cnames
