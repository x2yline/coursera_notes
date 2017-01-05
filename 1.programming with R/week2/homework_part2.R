calculate_cases <- function(directory, single_id){
  if (single_id <10){
    single_id = paste('00' , as.character(single_id), sep='')
  }else if (single_id <100){
    single_id = paste('0' , as.character(single_id), sep='')
  }else {
    single_id = as.character(single_id)
  }
  df <- read.csv(file.path(directory, paste(single_id,'.csv',sep='')))
  sum_num <- length(df[1][!is.na(df[2]) & !is.na(df[3])])
}

complete <- function(directory, id=1:332){
  nobs = NULL
  for (i in id) {
    nobs <- c(nobs,calculate_cases(directory, i))
  }
  df <- data.frame(id, nobs)
}
print(complete("E:/r/rprog-data-specdata/specdata",c(2, 4, 8, 10, 12)))
