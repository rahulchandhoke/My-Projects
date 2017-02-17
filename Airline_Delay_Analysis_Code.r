### Description of Code:-

jandata <- read.csv("E:/1 Jan 2014.csv") #reading the data for January
febdata <- read.csv("E:/2 Feb 2014.csv") #reading the data for February
mardata <- read.csv("E:/3 Mar 2014.csv") #reading the data for March
aprdata <- read.csv("E:/4 Apr 2014.csv") #reading the data for April
maydata <- read.csv("E:/5 May 2014.csv") #reading the data for May
jundata <- read.csv("E:/6 Jun 2014.csv") #reading the data for June
juldata <- read.csv("E:/7 Jul 2014.csv") #reading the data for July
augdata <- read.csv("E:/8 Aug 2014.csv") #reading the data for August
sepdata <- read.csv("E:/9 Sep 2014.csv") #reading the data for September
octdata <- read.csv("E:/10 Oct 2014.csv") #reading the data for October
novdata <- read.csv("E:/11 Nov 2014.csv") #reading the data for November
decdata <- read.csv("E:/12 Dec 2014.csv") #reading the data for December

totdata <- rbind(jandata,febdata,mardata,aprdata,maydata,jundata,juldata,augdata,sepdata,octdata,novdata,decdata) #combining all the data

uniquecarriers <- unique(totdata$Unique_Carrier) #list of unique carriers
uniqueorigins <- unique(totdata$Origin) #list of departure airports 
uniquedests <- unique(totdata$Dest) #list of arrival airports 
airlinenames <- c("American Airlines","Alaska Airlines","JetBlue","Delta Airlines","Atlantic Southeast Airlines","Frontier Airlines","AirTran","Hawaiian Airlines","American Eagle Airlines","Skywest Airlines","United Airlines","US Airways","Virgin America","Southwest Airlines") #list of airline names
names(uniquecarriers) <- airlinenames #assigning names to the carriers
months <- c("January","February","March","April","May","June","July","August","September","October","November","December")
deptimes <- sort(unique(totdata$Dep_Time)) #set of departure times
arrtimes <- sort(unique(totdata$Arr_Time)) #set of arrival times
doweek <- c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

airlinedepdelay <- function(airline){ #function to calculate the average departure delay based on the airline
  stopifnot(airline %in% uniquecarriers) #error checking
  delaysum <- sum(totdata$Dep_Delay[which(totdata$Unique_Carrier==airline)],na.rm=T) 
  delaycount <- length(which(totdata$Unique_Carrier==airline & (!is.na(totdata$Dep_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of departure delays by total number of records 
  return(avgdelay)
}

aldepdelays <- numeric(length(uniquecarriers)) 
for(i in 1:length(uniquecarriers)){ #calculating the average departure delay for each airline
  aldepdelays[i] <- airlinedepdelay(uniquecarriers[i])
}

plot(uniquecarriers,aldepdelays,type='l',main="Plot of the Departure Delays based on the Airlines",xlab="Airlines",xaxt="n",ylab="Average Departure Delay(In minutes)",sub="Negative value suggests before time departure") #plot of airline vs average departure delay
axis(1,1:length(uniquecarriers),airlinenames)

airlinearrdelay <- function(airline){ #function to calculate the average arrival delay based on the airline
  stopifnot(airline %in% uniquecarriers) #error checking
  delaysum <- sum(totdata$Arr_Delay[which(totdata$Unique_Carrier==airline)],na.rm=T) 
  delaycount <- length(which(totdata$Unique_Carrier==airline & (!is.na(totdata$Arr_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of arrival delays by total number of records 
  return(avgdelay)
}

alarrdelays <- numeric(length(uniquecarriers)) 
for(i in 1:length(uniquecarriers)){ #calculating the average arrival delay for each airline
  alarrdelays[i] <- airlinearrdelay(uniquecarriers[i])
}

plot(uniquecarriers,alarrdelays,type='l',main="Plot of the Arrival Delays based on the Airlines",xlab="Airlines",xaxt="n",ylab="Average Arrival Delay(In minutes)",sub="Negative value suggests before time arrival") #plot of airline vs average arrival delay
axis(1,1:length(uniquecarriers),airlinenames)

origindepdelay <- function(origin){ #function to calculate the average departure delay based on the origin airport
  stopifnot(is.character(origin))
  stopifnot(origin %in% uniqueorigins) #error checking
  delaysum <- sum(totdata$Dep_Delay[which(totdata$Origin==origin)],na.rm=T) 
  delaycount <- length(which(totdata$Origin==origin & (!is.na(totdata$Dep_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of departure delays by total number of records 
  return(avgdelay)
}

ordepdelays <- numeric(length(uniqueorigins)) 
for(i in 1:length(uniqueorigins)){ #calculating the average departure delay for each airport
  ordepdelays[i] <- origindepdelay(uniqueorigins[i])
}

plot(uniqueorigins,ordepdelays,type='l',main="Plot of the Departure Delays based on the Origin",xlab="Origin",ylab="Average Departure Delay(In minutes)",sub="Negative value suggests before time departure") #plot of origin vs average departure delay

destarrdelay <- function(dest){ #function to calculate the average arrival delay based on the destination
  stopifnot(is.character(dest))
  stopifnot(dest %in% uniquedests) #error checking
  delaysum <- sum(totdata$Arr_Delay[which(totdata$Dest==dest)],na.rm=T) 
  delaycount <- length(which(totdata$Dest==dest & (!is.na(totdata$Arr_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of arrival delays by total number of records 
  return(avgdelay)
}

dtarrdelays <- numeric(length(uniquedests)) 
for(i in 1:length(uniquedests)){ #calculating the average arrival delay for each destination
  dtarrdelays[i] <- destarrdelay(uniquedests[i])
}

plot(uniquedests,dtarrdelays,type='l',main="Plot of the Arrival Delays based on the Destination",xlab="Destinations",ylab="Average Arrival Delay(In minutes)",sub="Negative value suggests before time arrival") #plot of destination vs average arrival delay

monthdepdelay <- function(month){ #function to calculate the average departure delay based on the month
  stopifnot(is.numeric(month))
  month <- as.integer(month)
  stopifnot(month %in% 1:12) #error checking
  delaysum <- sum(totdata$Dep_Delay[which(totdata$Month==month)],na.rm=T) 
  delaycount <- length(which(totdata$Month==month & (!is.na(totdata$Dep_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of departure delays by total number of records 
  return(avgdelay)
}

modepdelays <- numeric(12) 
for(i in 1:12){ #calculating the average departure delay for each month
  modepdelays[i] <- monthdepdelay(i)
}

plot(1:12,modepdelays,type='l',main="Plot of the Departure Delays based on the Month",xlab="Month",xaxt="n",ylab="Average Departure Delay(In minutes)",sub="Negative value suggests before time departure") #plot of month vs average departure delay
axis(1,1:12,months)

montharrdelay <- function(month){ #function to calculate the average arrival delay based on the month
  stopifnot(is.numeric(month))
  month <- as.integer(month)
  stopifnot(month %in% 1:12) #error checking
  delaysum <- sum(totdata$Arr_Delay[which(totdata$Month==month)],na.rm=T) 
  delaycount <- length(which(totdata$Month==month & (!is.na(totdata$Arr_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of arrival delays by total number of records 
  return(avgdelay)
}

moarrdelays <- numeric(12) 
for(i in 1:12){ #calculating the average arrival delay for each month
  moarrdelays[i] <- montharrdelay(i)
}

plot(1:12,moarrdelays,type='l',main="Plot of the Arrival Delays based on the Month",xlab="Month",xaxt="n",ylab="Average Arrival Delay(In minutes)",sub="Negative value suggests before time departure") #plot of month vs average arrival delay
axis(1,1:12,months)

dowdepdelay <- function(dow){ #function to calculate the average departure delay based on the day of the week
  stopifnot(is.numeric(dow))
  dow <- as.integer(dow)
  stopifnot(dow %in% 1:7) #error checking
  delaysum <- sum(totdata$Dep_Delay[which(totdata$Day_Of_Week==dow)],na.rm=T) 
  delaycount <- length(which(totdata$Day_Of_Week==dow & (!is.na(totdata$Dep_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of departure delays by total number of records 
  return(avgdelay)
}

dowdepdelays <- numeric(7) 
for(i in 1:7){ #calculating the average departure delay for each day of the week
  dowdepdelays[i] <- dowdepdelay(i)
}

plot(1:7,dowdepdelays,type='l',main="Plot of the Departure Delays based on the Day of the Week",xlab="Day of the Week",xaxt="n",ylab="Average Departure Delay(In minutes)",sub="Negative value suggests before time departure") #plot of day of the week vs average departure delay
axis(1,1:7,doweek)

dowarrdelay <- function(dow){ #function to calculate the average arrival delay based on the day of the week
  stopifnot(is.numeric(dow))
  dow <- as.integer(dow)
  stopifnot(dow %in% 1:7) #error checking
  delaysum <- sum(totdata$Arr_Delay[which(totdata$Day_Of_Week==dow)],na.rm=T) 
  delaycount <- length(which(totdata$Day_Of_Week==dow & (!is.na(totdata$Arr_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of arrival delays by total number of records 
  return(avgdelay)
}

dowarrdelays <- numeric(7) 
for(i in 1:7){ #calculating the average arrival delay for each day of the week
  dowarrdelays[i] <- dowarrdelay(i)
}

plot(1:7,dowarrdelays,type='l',main="Plot of the Arrival Delays based on the Day of the Week",xlab="Day of the Week",xaxt="n",ylab="Average Arrival Delay(In minutes)",sub="Negative value suggests before time departure") #plot of day of the week vs average arrival delay
axis(1,1:7,doweek)

domdepdelay <- function(dom){ #function to calculate the average departure delay based on the day of the month
  stopifnot(is.numeric(dom))
  dom <- as.integer(dom)
  stopifnot(dom %in% 1:31) #error checking
  delaysum <- sum(totdata$Dep_Delay[which(totdata$Day_Of_Month==dom)],na.rm=T) 
  delaycount <- length(which(totdata$Day_Of_Month==dom & (!is.na(totdata$Dep_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of departure delays by total number of records 
  return(avgdelay)
}

domdepdelays <- numeric(31) 
for(i in 1:31){ #calculating the average departure delay for each day of the month
  domdepdelays[i] <- domdepdelay(i)
}

plot(1:31,domdepdelays,type='l',main="Plot of the Departure Delays based on the Day of the Month",xlab="Day of the Month",ylab="Average Departure Delay(In minutes)",sub="Negative value suggests before time departure") #plot of day of the month vs average departure delay

domarrdelay <- function(dom){ #function to calculate the average arrival delay based on the day of the month
  stopifnot(is.numeric(dom))
  dom <- as.integer(dom)
  stopifnot(dom %in% 1:31) #error checking
  delaysum <- sum(totdata$Arr_Delay[which(totdata$Day_Of_Month==dom)],na.rm=T) 
  delaycount <- length(which(totdata$Day_Of_Month==dom & (!is.na(totdata$Arr_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of arrival delays by total number of records 
  return(avgdelay)
}

domarrdelays <- numeric(31) 
for(i in 1:31){ #calculating the average arrival delay for each day of the month
  domarrdelays[i] <- domarrdelay(i)
}

plot(1:31,domarrdelays,type='l',main="Plot of the Arrival Delays based on the Day of the Month",xlab="Day of the Month",ylab="Average Arrival Delay(In minutes)",sub="Negative value suggests before time departure") #plot of day of the month vs average arrival delay

dptmdepdelay <- function(dptm){ #function to calculate the average departure delay based on the departure time
  stopifnot(is.numeric(dptm))
  dptm <- as.integer(dptm)
  stopifnot(dptm %in% deptimes) #error checking
  delaysum <- sum(totdata$Dep_Delay[which(totdata$Dep_Time==dptm)],na.rm=T) 
  delaycount <- length(which(totdata$Dep_Time==dptm & (!is.na(totdata$Dep_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of departure delays by total number of records 
  return(avgdelay)
}

dptmdepdelays <- numeric(length(deptimes)) 
j <- 0
for(i in deptimes){ #calculating the average departure delay for each departure time
  dptmdepdelays[j] <- dptmdepdelay(i)
  j <- j+1
}

plot(deptimes,dptmdepdelays,type='l',main="Plot of the Departure Delays based on the Departure Time",xlab="Departure Time",ylab="Average Departure Delay(In minutes)",sub="Negative value suggests before time departure") #plot of departure time vs average departure delay

artmarrdelay <- function(artm){ #function to calculate the average arrival delay based on the arrival time
  stopifnot(is.numeric(artm))
  artm <- as.integer(artm)
  stopifnot(artm %in% arrtimes) #error checking
  delaysum <- sum(totdata$Dep_Delay[which(totdata$Arr_Time==artm)],na.rm=T) 
  delaycount <- length(which(totdata$Arr_Time==artm & (!is.na(totdata$Dep_Delay))))
  avgdelay <- delaysum/delaycount #average as the sum of arrival delays by total number of records 
  return(avgdelay)
}

artmarrdelays <- numeric(length(arrtimes)) 
j <- 0
for(i in arrtimes){ #calculating the average arrival delay for each arrival time
  artmarrdelays[j] <- artmarrdelay(i)
  j <- j+1
}

plot(arrtimes,artmarrdelays,type='l',main="Plot of the Arrival Delays based on the Arrival Time",xlab="Arrival Time",ylab="Average Arrival Delay(In minutes)",sub="Negative value suggests before time arrival") #plot of arrival time vs average arrival delay
