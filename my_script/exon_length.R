setwd('E:\\r\\biotrainee_demo1')
data <- read.table('CCDS.current.txt', sep='\t',
stringsAsFactors=F, header=T)
head(data)
exon_num<-function(data){
  exon_length <- 0
  #得到倒数第二列数据(vector)
  exon_range_vect <- data[,dim(data)[2]-1]
  for (i in exon_range_vect) {
    if (i != '-'){
      #去重首末两个中括号
      #print(class(i))
      i <- substr(i, start=2, stop=nchar(i)-1)
      # 把i分割为vector(num1-num2, num3-num4)
      i_vect <- strsplit(i,",")[[1]]
      #print(class(i_vect))
       for (j in i_vect){
         # 把j分割为vector(num1,num2)
         start_end <- strsplit(j,"-")[[1]]
         #print(start_end)
         print(as.numeric(start_end[2]) - as.numeric(start_end[1]))
         exon_length <- exon_length + as.numeric(start_end[2])-as.numeric(start_end[1])
       }
    }
  }
  exon_length
}
exon_length <- exon_num(data)
