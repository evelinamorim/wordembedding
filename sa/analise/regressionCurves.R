# Description: Plot the regression curve for the first 10 documents of the training
# set

library("princurve")
library("longitudinalData")

process_line <- function(l){
  d <- as.numeric(unlist(strsplit(l, ",")))
  d  <- matrix(d,nrow = 1,ncol = 400 , byrow = TRUE)
  return(d)
}


# read the documens
dat1 = readLines("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/docs5.txt")
l1 = lapply(dat1,process_line)
# print(length(l1))
l1 <- matrix(unlist(l1),nrow = 105)

dat2 = readLines("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/docs9.txt")
l2 = lapply(dat2,process_line)
l2 <- matrix(unlist(l2),nrow = 196)


fit1 <- principal.curve(l1)
fit2 <- principal.curve(l2)


# outros documentos

dat3 = readLines("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/docs2.txt")
l3 = lapply(dat3,process_line)
l3 <- matrix(unlist(l3),nrow = 72)


dat4 = readLines("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/docs4.txt")
l4 = lapply(dat4,process_line)
l4 <- matrix(unlist(l4),nrow = 43)

fit3 <- principal.curve(l3)
fit4 <- principal.curve(l4)



# mais alguns documentos

dat5 = readLines("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/docs8.txt")
l5 = lapply(dat5,process_line)
l5 <- matrix(unlist(l5),nrow = 196)

dat6 = readLines("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/docs10.txt")
l6 = lapply(dat6,process_line)
l6 <- matrix(unlist(l6),nrow = 54)


fit5 <- principal.curve(l5)
fit6 <- principal.curve(l6)

x1 <- fit1$s[,c(1)]
y1 <- fit1$s[,c(2)]

x2 <- fit2$s[,c(1)]
y2 <- fit2$s[,c(2)]

x3 <- fit3$s[,c(1)]
y3 <- fit3$s[,c(2)]

x4 <- fit4$s[,c(1)]
y4 <- fit4$s[,c(2)]

x5 <- fit5$s[,c(1)]
y5 <- fit5$s[,c(2)]

x6 <- fit6$s[,c(1)]
y6 <- fit6$s[,c(2)]

# read answers of documents
ans10 <- read.csv("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/ans10.txt")
x2
# k = 10, coordinates for each document
k <- 10
doc_size <- seq(k)

x1 <- x1[doc_size]
y1 <- y1[doc_size]
doc1 <- c(x1,y1)
  
x2 <- x2[doc_size]
y2 <- y2[doc_size]
doc2 <- c(x2,y2)

x3 <- x3[doc_size]
y3 <- y3[doc_size]
doc3 <- c(x3,y3)

x4 <- x4[doc_size]
y4 <- y4[doc_size]
doc4 <- c(x4,y4)

x5 <- x5[doc_size]
y5 <- y5[doc_size]
doc5 <- c(x5,y5)

x6 <- x6[doc_size]
y6 <- y6[doc_size]
doc6 <- c(x6,y6)

X <- c(x1,x2,x3,x4,x5,x6)
X <- matrix(X,nrow = 6,byrow = TRUE)

Y <- c(Y1,Y2,Y3,Y4,Y5,Y6)
Y <- matrix(X,nrow = 6,byrow = TRUE)


reg1 <- lm( ans10$satisfaction ~ X + Y)

#plot residual: importa mais para o teste 
# TODO: fazer um script para os resultados do teste
resid(reg1)
plot(density(resid(reg1))) #A density plot
qqnorm(resid(reg1)) # A quantile normal plot - good for checking normality
qqline(resid(m1))