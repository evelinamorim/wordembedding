library("princurve")
library("longitudinalData")

process_line <- function(l){
  d <- as.numeric(unlist(strsplit(l, ",")))
  d  <- matrix(d,nrow = 1,ncol = 400 , byrow = TRUE)
  return(d)
}

dat1 = readLines("/home/evelinamorim/Documentos/UFMG/wordembedding/sa/analise/docs5.txt")
l1 = lapply(dat1,process_line)
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

# plot(fit1, col = "red")
# par(new=TRUE)
# plot(fit2, col = "blue")
# par(new=TRUE)
# plot(fit3, col = "black")
par(new=TRUE)
# plot(fit4, col = "green")
#par(new=TRUE)
# plot(fit5, col = "darkgreen")
# par(new=TRUE)
plot(fit6, col = "orange")
# TODO: colocar aqui as coordenadas de fit (projeções)
x3 <- fit3$s[,c(1)]
y3 <- fit3$s[,c(2)]

x4 <- fit4$s[,c(1)]
y4 <- fit4$s[,c(2)]

x6 <- fit6$s[,c(1)]
y6 <- fit6$s[,c(2)]

# r1 <- distFrechet(x3,y3,x6,y6, timeScale=0.01, FrechetSumOrMax = "sum")
# r2 <- distFrechet(x3,y3,x4,y4, timeScale=0.01, FrechetSumOrMax = "sum")
# r1
# r2
