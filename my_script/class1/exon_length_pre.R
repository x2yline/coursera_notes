setwd('E:\\r\\biotrainee_demo\\class1')#修改工作路径
t1 <- Sys.time()#把程序运行之前的时间赋值给t1
directory = 'CCDS.current.txt'#把文件名赋值给directory

data <- read.table(directory, sep='\t',
                   stringsAsFactors=F, header=T)[c(1,10)]#读取数据并提取出第一和第十列

get_gene <-function(data_item){
  # 该函数用于apply执行
  # 输入的数据为仅含原始数据第1列和第10列的dataframe
  # 用apply函数执行后输出的数据为每个基因外显子的坐标，
  # 一个基因的所有外显子以逗号分隔组成一个string，所有基因的string组成一个vector
  # 用apply函数执行后，最后格式为c('111-112, 115-135, 125-138', '254-258',...)
  if (!data_item[2] =='-'){
    exon_ranges <- data_item[2]
    exon_ranges <- substr(exon_ranges, start=2, stop=nchar(exon_ranges)-1)# 去除首尾的中括号符号
  }
}


get_exon <- function(gene){
  # 输入的数据为c('111-112, 115-135', '125-138', '254-258,...')
  # 把i号染色体上的所有外显子后在一起，并去除完全相同的外显子
  # 输出的数据为c('111-112','115-135', '125-138', '254-258', ...)
  exon <- unique(strsplit(gene,", ")[[1]])
}

get_length <- function(exon){
  # 输入的数据为lapply(c('111-112','115-135', '125-138', '254-258', ...),fun)
  # 输出结果为左右两坐标之差+1即外显子的长度
  loc <- strsplit(exon,"-")[[1]]
  a <- as.numeric(loc[2])-as.numeric(loc[1]) +1 #每个外显子的碱基数目
  a
}


exon_length = 0
exon_length_items = NULL
for (i in unique(data[,1])){
  gene_i <- paste(apply(data[which(data[1]==i & data[2] != '-'),], 1, get_gene),collapse=', ')
  exon_i <-  get_exon(gene_i)
  exon_i_length <- sapply(exon_i, get_length)
  exon_length <- exon_length + sum(exon_i_length)
  exon_length_items <- c(exon_i_length, exon_length_items)
  names(exon_length_items)[1:length(exon_i_length)] <- i
}

hist(exon_length_items,xlim=c(0,500),breaks = 20000, 
     main='Distribution of exon length', xlab='exon length')

difftime(Sys.time(), t1, units = 'secs')# 计算执行完成后时间与t1的间隔

print(paste('all exons length is',exon_length))

