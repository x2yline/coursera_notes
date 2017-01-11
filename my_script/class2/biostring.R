source("https://bioconductor.org/biocLite.R")
biocLite("BSgenome.Hsapiens.UCSC.hg19")
library(Biostrings)
library(BSgenome.Hsapiens.UCSC.hg19)
alphabetFrequency(Hsapiens$chrY)
GC_content<-letterFrequency(Hsapiens$chrY,letters = "CG")
GC_content
GC_pencentage <- letterFrequency(Hsapiens$chrY,letters = "CG")/letterFrequency(Hsapiens$chrY,letters = "ACGT")
GC_pencentage
