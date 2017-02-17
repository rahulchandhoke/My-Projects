#CALCULATING COMPONENT SCORES 
#Component scores are calculated using the indicator values and the weights are modifield according to the component being calculated
data <- read.csv("E:/Component12.csv")
data

u1 <- rnorm(33)
for(i in 1:33)
{
  u1[i] <- ((data[i,1]*.26)+(data[i,2]*.27)+(data[i,3]*.26)+(data[i,4]*.21))
}

u1

u2 <- rnorm(33)
for(i in 1:33)
{
  u2[i] <- ((u1[i]-0.13)/(5.76))
}

u2 <- u2*100
u2 <- round(u2, digits=2)
u2

write.csv(u2, file = "E:/Component12Vals.csv")


#CALCULATING DIMENSION SCORES
#Dimension Scores are calculated as an average of the components scores within each dimension
data <- read.csv("E:/Dim3.csv")
data

u1 <- rnorm(33)
for(i in 1:33)
{
  u1[i] <- ((data[i,1]+data[i,2]+data[i,3]+data[i,4])/4)
}
u1 <- round(u1, digits=2)

u1

write.csv(u1, file = "E:/Dim3Vals.csv")


#CALCULATING INDEX SCORES
#Index Scores are calculated as an average of the dimension scores
data <- read.csv("E:/Spi.csv")
data

u1 <- rnorm(33)
for(i in 1:33)
{
  u1[i] <- ((data[i,1]+data[i,2]+data[i,3])/3)
}
u1 <- round(u1, digits=2)

u1

write.csv(u1, file = "E:/SpiVals.csv")


#GRAPHICAL REPRESENTATION
#Plotting graphs to represent final values of the index and each dimension
data <- read.csv("E:/SpiVals.csv")

data2 <- read.csv("E:/Demo.csv")

data3 <- read.csv("E:/Spi.csv")

areas <- data2$Area
codes <- data2$Code

spi <- data$x
codes
areas

names(spi) <- c(sort(areas))

plot(names(spi),spi,type='b',main="Plot of SPI Values for the State and Districts",xlab="Districts",xaxt="n",ylab="Social Progress Index") #plot of SPI
axis(1,1:length(spi),codes)
abline(h=spi[1]) 

plot(data3$Bas,type='b',main="Plot of Basic Human Needs Values for the State and Districts",xlab="Districts",xaxt="n",ylab="Basic Human Needs") #plot of Basic Human Needs dimension
axis(1,1:length(spi),codes)
abline(h=data3$Bas[1])

plot(data3$Fou,type='b',main="Plot of Foundations of Wellbeing Values for the State and Districts",xlab="Districts",xaxt="n",ylab="Foundations of Wellbeing") #plot of Foundations of Wellbeing dimension
axis(1,1:length(spi),codes)
abline(h=data3$Fou[1])

plot(data3$Opp,type='b',main="Plot of Opportunity Values for the State and Districts",xlab="Districts",xaxt="n",ylab="Opportunity") #plot of Opportunity dimension
axis(1,1:length(spi),codes)
abline(h=data3$Opp[1])

kc <-  kmeans(spi,3)
kc$size
kc$centers

spi2 <- sort(spi,decreasing = T)
spi2

vec <- rep(0, 33)
vec[5] <- kc$centers[3]
vec[16] <- kc$centers[2]
vec[27] <- kc$centers[1]

plot(names(spi), spi2, main="Plot of SPI Values for the State and Districts(Descending)",xlab="Districts",ylab="Social Progress Index") #Clustering districts with similar indices
points(vec,pch=8)
