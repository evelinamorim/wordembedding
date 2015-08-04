# Description: Analyze 10% of train corpus in linear regression algorithm 

library("princurve")
library("longitudinalData")

process_line <- function(l){
  d <- as.numeric(unlist(strsplit(l, ",")))
  d  <- matrix(d,nrow = 1,ncol = 400 , byrow = TRUE)
  return(d)
}

dir_data="/scratch2/evelin.amorim/WebMD/outtest/"


files <- list.files(path=dir_data, pattern="*.txt", full.names=T, recursive=FALSE)

# reading features files
ptm <- proc.time()
k <- 10
doc_size <- seq(k)
doc_list = lapply(files, function(x) {
  dat = readLines(x)
  l = lapply(dat, process_line)
  nrowl = length(l)
  l <- matrix(unlist(l), nrow = nrowl)
  fit <- principal.curve(l)
  
  return(fit)
})

#build X and Y for multilinear regression
X <- c()
Y <- c()
for(d in doc_list){
  x <- d$s[,c(1)]
  X <- c(X,x[doc_size])
  
  y <- d$s[,c(2)]
  Y <- c(Y,y[doc_size])
}

X <- matrix(X, nrow = length(doc_list), byrow = TRUE)
Y <- matrix(Y, nrow = length(doc_list), byrow = TRUE)

# taking the id from files in order to take the answers in answer vector
t <- sapply(strsplit(files, split = "docs"), "[",2)
t <- sapply(strsplit(t,split = ".txt"),"[",1)
docid_list <- strtoi(t)

#reading the answer file (Y variable)
ans <- read.csv("/scratch2/evelin.amorim/WebMD/anstest.csv", header = FALSE)
# ans[docid_list]
proc.time() - ptm

#satisfaction only from the documents from docid_list
sat_y <- unlist(ans[1])
sat_y <- sat_y[docid_list]

# multilinear regression: load model
load()