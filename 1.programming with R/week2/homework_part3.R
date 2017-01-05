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
#df <- complete("E:/r/rprog-data-specdata/specdata",c(2, 4, 8, 10, 12))
#threshold = 200
corr <- function(directory, threshold=0){
  cor_result = NULL
  df <- complete(directory,1:332)
  id_vect <- df[1][df[2]>threshold]
  for (i in id_vect){
    if (i <10){
      i = paste('00' , as.character(i), sep='')
    }else if (i <100){
      i = paste('0' , as.character(i), sep='')
    }else {
      i = as.character(i)
    }
    
    df <- read.csv(file.path(directory, paste(i,'.csv',sep='')))
    cor_result <- c(cor_result,cor(df[2][!is.na(df[2]) & !is.na(df[3])], df[3][!is.na(df[2]) & !is.na(df[3])]))
  
  }
  cor_result
}
result <- corr("E:/r/rprog-data-specdata/specdata",threshold=400)
summary(result)
