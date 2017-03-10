setwd('E:\\r\\biotrainee_demo1')
t1 <- Sys.time()
directory = 'CCDS.current.txt'
# 读取数据并提取第1列和第10列
data <- read.table(directory, sep='\t',
                   stringsAsFactors=F, header=T)[c(1,10)]

get_gene <-function(data_item){
  # 用apply执行该函数
  # 输入的数据为仅含原始数据第1列和第10列的dataframe
  # 输出的数据为c('111-112, 115-135, 125-138', '254-258',...)
  if (!data_item[2] =='-'){
    exon_ranges <- data_item[2]
    exon_ranges <- substr(exon_ranges, start=2, stop=nchar(exon_ranges)-1)
  }
}

get_exon <- function(gene){
  # 输入的数据为c('111-112, 115-135, 125-138, 254-258,...')
  # 输出的数据为c('111-112','115-135', '125-138', '254-258', ...)
  exon <- unique(strsplit(gene,", ")[[1]])# 注：strsplit的输出结果为列表
}

get_length <- function(exon){
  # 输入的数据为lapply(c('111-112','115-135', '125-138', '254-258', ...),fun)
  # 输出结果为两坐标值和左右两坐标之差
  loc <- strsplit(exon,"-")[[1]]
  a <- c(as.numeric(loc[1]), as.numeric(loc[2])-as.numeric(loc[1]), as.numeric(loc[2]))
  #if (a==0){
  #print(loc)
  #}
  a
}

exon_length = NULL
for (i in unique(data[,1])){
  # paste 函数把i号染色体的所有外显子的坐标合并为一个character对象
  # gene_i的格式为'111-112, 115-135, 125-138, 254-258,...'
  gene_i <- paste(apply(data[which(data[1]==i & data[2] != '-'),], 1, get_gene),collapse=', ')
  # exon_i的格式为c('111-112','115-135', '125-138', '254-258', ...)
  exon_i <-  lapply(get_exon(gene_i), get_length)
  mat <- matrix(unlist(exon_i), ncol=3, byrow = T)
  #mat <- mat[order(mat[,2], decreasing = F),]
  #mat <- mat[order(mat[,1], decreasing = F),]
  
  # 使用matrix 是因为vector太长会报错
  #R memory management / cannot allocate vector of size n MB
  base_loc <- matrix(unique(unlist(apply(mat, 1, function(x) c(x[1]:x[3])))))
  
  exon_length <- c(exon_length , dim(base_loc)[1] * dim(base_loc)[2])
}

# 耗时长度
difftime(Sys.time(), t1, units = 'secs')
chrs <- unique(data[,1])
barplot(exon_length,names.arg=chrs,xlab='Chromosomes',ylab='length of exons')
print(paste('all exons length is',sum(exon_length)))


