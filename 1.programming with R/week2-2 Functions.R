Sys.Date()
args(rnorm(1))
function(x){x[length(x)]}
telegram <- function(...){
  paste("START", ..., "STOP")
}
  
"%p%" <- function(x, y){ # Remember to add arguments!
  paste(x,y)
}
