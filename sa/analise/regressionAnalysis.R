# Description: Analyze 10% of train corpus in linear regression algorithm 

library("princurve")
library("longitudinalData")

process_line <- function(l){
  d <- as.numeric(unlist(strsplit(l, ",")))
  d  <- matrix(d,nrow = 1,ncol = 400 , byrow = TRUE)
  return(d)
}

dir_data="/home/evelinamorim/Documentos/UFMG/wordembedding/data/out/"


files <- list.files(path=dir_data, pattern="*.txt", full.names=T, recursive=FALSE)

# reading features files
ptm <- proc.time()
doc_list = lapply(files, function(x) {
   dat = readLines(x)
   l = lapply(dat, process_line)
   nrowl = length(l)
   l <- matrix(unlist(l), nrow = nrowl)
})

# taking the id from files in order to take the answers in answer vector
t <- sapply(strsplit(files, split = "docs"), "[",2)
t <- sapply(strsplit(t,split = ".txt"),"[",1)
docid_list <- strtoi(t)

#reading ans 
ans <- read.csv("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/ans.txt")

proc.time() - ptm
# length(doc_list)

