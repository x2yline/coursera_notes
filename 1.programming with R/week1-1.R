install.packages("swirl")
packageVersion('swirl')
library('swirl')
install_from_swril('R Programming') #install_course('R Programming: The basics of programming in R')
swirl()

help.start()
?c

x<- 1:4
names(x) <- letters[1:4]
c(x)          # has names
as.vector(x)  # no names
dim(x) <- c(2,2)
x
c(x)
as.vector(x)

x*3 + 100
my_sqrt <- sqrt(x-1)
