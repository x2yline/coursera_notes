setwd('E:\\r\\biotrainee_demo1')
t1 <- Sys.time()
directory = 'CCDS.current.txt'

data <- read.table(directory, sep='\t',
  stringsAsFactors=F, header=T)[c(1,10)]

get_gene <-function(data_item){
  if (!data_item[2] =='-'){
    exon_ranges <- data_item[2]
    exon_ranges <- substr(exon_ranges, start=2, stop=nchar(exon_ranges)-1)
  }
}

get_exon <- function(gene){
  exon <- unique(strsplit(gene,", ")[[1]])
}

get_lenth <- function(exon){
  loc <- strsplit(exon,"-")[[1]]
  a <- as.numeric(loc[2])-as.numeric(loc[1])
}


exon_length = 0
for (i in unique(data[,1])){
  
  gene_i <- paste(apply(data[which(data[1]==i & data[2] != '-'),], 1, get_gene),collapse=', ')
  exon_i <-  get_exon(gene_i)
  exon_i_length <- sapply(exon_i, get_lenth)
  exon_length <- exon_length + sum(exon_i_length)
}

# 耗时长度
difftime(Sys.time(), t1, units = 'secs')

print(paste('all exons length is',exon_length))
