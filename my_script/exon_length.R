setwd('E:\\r\\biotrainee_demo1')
data <- read.table('CCDS.current.txt', sep='\t',
stringsAsFactors=F, header=T)
head(data)
exon_num<-function(data){
  exon_length <- 0
  all_exons <- NULL
  pb <- txtProgressBar(min = 0, max = dim(data)[1], style = 3)
  for (i in 1:dim(data)[1]){
    setTxtProgressBar(pb, i)
    # 得到第i行的基因全部信息
    gene <- as.vector(as.matrix(data[i,]))
    if (gene[dim(data)[2]-1]!='-'){
      # 得到第i行基因对应的染色体号
      chr <- gene[1]
      # 得到第i行基因对应的exon坐标
      exon_ranges <- gene[dim(data)[2]-1]
      # 去除exon坐标范围首末两个中括号
      exon_ranges <- substr(exon_ranges, start=2, stop=nchar(exon_ranges)-1)
      # 把坐标分割vector格式为(num1-num2, num3-num4...)
      # 注意strsplit得到的坐标为list对象需要提取出vector
      exon_vect <- strsplit(exon_ranges,",")[[1]]
       for (j in exon_vect){
         # 把j分割为vector(num1,num2)
         start_end <- strsplit(j,"-")[[1]]
         #print(j)
         record <- paste(chr, ':', as.numeric(start_end[2]), as.numeric(start_end[1]))
         if (!any(record == all_exons)){
           exon_length <- exon_length + as.numeric(start_end[2])-as.numeric(start_end[1])
           all_exons <- c(all_exons, record)
           }
         
       }
    }
  }
  close(pb)
  exon_length
}
exon_length <- exon_num(data)
