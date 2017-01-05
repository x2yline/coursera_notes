allstrings <- readLines('F:\\meta\\endnote\\demo\\1.xml',encoding='UTF-8')

mydata <- data.frame(age=numeric(0), 
  gender=character(0), weight=numeric(0))
mydata <- edit(mydata)
library(XML)
xmlfile <- htmlParse('F:\\meta\\endnote\\demo\\1.xml', encoding='UTF-8')
record_path <- '//record'
title_path <- '//title'
year_path <- '//year'
abstract_path <- '//abstract'
record.node <- getNodeSet(xmlfile, record_path)
year.node <- getNodeSet(xmlfile, year_path)
title.node <- getNodeSet(xmlfile, title_path)
abstract.node <- getNodeSet(xmlfile, abstract_path)

print(xmlValue(year.node [[306]]))
title.value <- xmlValue(title.node [[1]])

class(xmlfile)
xmltop = xmlRoot(xmlfile)
all <- (xmltop)[[1]][[1]][[1]]
all[[2]][['dates']]
all
all <- list(all)
plantcat <- xmlSApply(xmltop, function(x) xmlSApply(x, xmlValue))
plantcat_df <- data.frame(t(plantcat),row.names=NULL)
plantcat_df[1:2]

root = 'F:\\meta\\endnote\\demo\\'
file = paste(root, '1.xml', sep = '')
filedata <- scan(file, what = '', sep='>', fileEncoding = 'UTF-8')
head(filedata)
class(filedata)
summary(filedata)



library(XML)
xmlfile <- htmlParse('F:\\meta\\endnote\\demo\\2.xml',
  encoding='UTF-8')
xmltop = xmlRoot(xmlfile)
all <- (xmltop)[[1]][[1]][[1]]
abstract <- all[[2]][['abstract']]
dataf <- xmlToDataFrame(all)
dim(dataf)
