setwd('E:\\r\\biotrainee_demo\\class 2')
# 读入数据
t1 <- Sys.time()
df <- read.csv('chr1.fa', header=F, stringsAsFactors=F)
# index_df 为chr所在的位置
index_df <- data.frame(begin=which(sapply(df[,1], function(x){
  substr(x, start=1, stop=1)=='>'})))
# index_df1 为string所在的位置+1
index_df1 <- data.frame(rbind(matrix(index_df[-1,1]),dim(df)[1]+1))
# 把index_start和index_end存入data.frame
index_df2 <- cbind(index_df, index_df1)
remove(index_df1, index_df)
# 得出每个染色体对应string后计算其N与GC百分比
result <- apply(index_df2, 1, function(x) {  # 把提取字符串后把字符串变为大写
  y <- toupper(paste(df[(x[1]+1):(x[2]-1),1], collapse=''))
  y <- strsplit(y, split=character(0))[[1]]
  N <- length(y[y =='N'])/length(y)
  GC <- length(y[y =='G' | y == 'C'])/(length(y)-length(y[y =='N']))
  c(N,GC)
})
# 把行名改为N和GC并转秩
rownames(result) = c('N','GC')
result <- t(result)
# 取结果前几行
head(result)
difftime(Sys.time(), t1, units = 'secs')
