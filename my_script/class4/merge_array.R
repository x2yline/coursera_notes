merge_file_by_column1 <- function(fname_list) {
  #函数输入为目标文件名列表，gz文件或txt文件
  #输出为按第一列合并的数据框
  pb <- txtProgressBar(1, length(fname_list)-1, style=3)
  merged_dat <- read.table(gzfile(fname_list[1]), stringsAsFactors = F, header = T)
  for (i in (1:(length(fname_list)-1))){
    setTxtProgressBar(pb, i)
    tmp_dat <- read.table(gzfile(fname_list[i+1]), stringsAsFactors = F, header = T)
    merged_dat <- merge(merged_dat, tmp_dat, by = colnames(tmp_dat)[1], all=T)
  }
  close(pb)
  return(merged_dat)
}
 
# 先把GSE48213_RAW.tar解压为.gz文件（不用解压为TXT文件）
# 确保E:\\GSE48213_RAW目录下只含有目标文件（即只有56个gz文件或者只有56个txt文件）
setwd('E:\\GSE48213_RAW')
 
merged_dat <- merge_file_by_column1(fname_list=list.files())
View(merged_dat)
