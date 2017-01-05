sum_pollutant <- function(directory, pollutant, single_id){
  if (single_id <10){
    single_id = paste('00' , as.character(single_id), sep='')
  }else if (single_id <100){
    single_id = paste('0' , as.character(single_id), sep='')
  }else {
    single_id = as.character(single_id)
  }
  
  df <- read.csv(file.path(directory, paste(single_id,'.csv',sep='')))
  if (pollutant == 'sulfate'){
    sum_num <- c(sum(df[2][!is.na(df[2])]),length(df[2][!is.na(df[2])]))
  }else if (pollutant == 'nitrate'){
    sum_num <- c(sum(df[3][!is.na(df[3])]),length(df[3][!is.na(df[3])]))
  }
  #mean <- sum_num[1]/sum_num[2]
}

pollutantmean <- function(directory, pollutant, id=1:332){
  pollutant_sum <- 0
  pollutant_num <- 0
  for (i in id) {
    all <- sum_pollutant(directory, pollutant, i)
    pollutant_sum <- pollutant_sum + all[1]
    pollutant_num <- pollutant_num + all[2]
  }
  pollutant_sum/pollutant_num
}

