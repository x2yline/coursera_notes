
find_target_data <- function(gene, all_data){
  gene_info_vect <- all_data[,9]
  gene_info_vect[all_data[,3]!='gene'] = ''
  gene_name_vect <- sapply(gene_info_vect,function(x){
    strsplit(strsplit(x,';')[[1]][3], '\"')[[1]][2]
  })
  names(gene_name_vect) = NULL
  target_row <- which(gene_name_vect == toupper(gene))
  i <- 1
  while( is.na(gene_name_vect[target_row +i])){
    i <- i+ 1
  }
  target_data<-all_data[target_row:(target_row+i-1),]
  colnames(target_data) =c('chr','db','record','start','end','tmp1','strand','tmp3','tmp4')
  return(target_data)
}



plot_gene_structure <- function (target_data, gene) {
  gene_start <- target_data$start[1]
  gene_end <- target_data$end[1]
  transcript_num <- length(which(target_data$record == 'transcript'))
  tmp_colors <- c('green', 'red', 'black', 'blue', 'yellow', 'blue','grey','grey')
  names(tmp_colors) <- c('gene', 'CDS', 'transcript', 'exon','start_codon','stop_codon','three_prime_utr','five_prime_utr')
  rect_sep <- c(0.2,rep(0.8,7))
  names(rect_sep) <-c('transcript','gene', 'exon', 'CDS','start_codon','stop_codon','three_prime_utr','five_prime_utr')
  par(mar=c(6,6,2,6), bty='n', new=F)
  plot(gene_start:gene_start, 1, type = 'n', xlab='', ylab ='',ylim = c(0,transcript_num*2+1), xlim = c(gene_start,gene_end), yaxt='n',xaxt='n')
  title(main = gene,sub = paste("chr",target_data$chr,": ",gene_start,"-",gene_end,sep=""))
  if (target_data$strand[1]=='-'){
    strand <- 1
  }else { strand <-2 }
  j <- 0
  rect_ybottom <- j-rect_sep[1]
  rect_ytop <- j+rect_sep[1]
  rect(gene_start, rect_ybottom, gene_end, rect_ytop, col = tmp_colors['gene'], border = F)
  arrows(gene_start, j+rect_sep[1]+0.1, gene_end, j+rect_sep[1]+0.1, code= strand, col = tmp_colors['gene'], lwd = 4, angle=30)
  for (rows in (2:dim(target_data)[1])){
    if (target_data$record[rows] == 'transcript') {
      j <- j + 2
    }
    rect_ybottom <- j-rect_sep[target_data$record[rows]]
    rect_ytop <- j+rect_sep[target_data$record[rows]]
    #print(tmp_colors[target_data$record[rows]])
    rect(target_data$start[rows], rect_ybottom, target_data$end[rows], rect_ytop, col=tmp_colors[target_data$record[rows]], border = NA)
  }
  
  axis(1,c(gene_start,gene_start+(gene_end-gene_start)/5,gene_start+(gene_end-gene_start)*2/5,gene_start+(gene_end-gene_start)*3/5,gene_start+(gene_end-gene_start)*4/5,gene_end))
  
  axis(2,c(seq(0,transcript_num*2,2)), labels=c('gene',paste('transcipt', seq(1:transcript_num), sep=' ')),las=1)
  legend(x=gene_end, transcript_num*2,horiz=F,
         box.lty=0,xpd=T,
         c('gene','nonCDS_exon','CDS_exon','UTR','intron'),
         fill=c('green','blue','red','grey','black'),
         border = F,bty='n',
         cex=0.8)
}


setwd('E:\\r\\biotrainee_demo\\class5')
file <- 'Homo_sapiens.GRCh38.87.chr.gtf'
library(data.table)
all_data<-as.data.frame(fread(file, header=F, sep='\t', stringsAsFactors=F, skip =5))
#load('all.Rdata')

gene='ANXA1'

target_data <- find_target_data (gene, all_data=all_data)

png(paste(gene,'.png'),width = 1200, height = 680)
plot_gene_structure(target_data, gene)
dev.off()






