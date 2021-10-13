library(ggplot2)
library(dplyr)
library(lubridate)
f= read.csv("~/Desktop/Compepi/facility43.csv", sep = "\t")
f$itime = as.POSIXct(f$itime)
g = filter(f, jtype == "Nursing")
ggplot( data = f, mapping = aes(x = itime, y = hid, color = hid)) + geom_point()

ggplot( data = g, mapping = aes(x = dayhour, y = hid, color = hid)) + geom_point()
g$hour = hour(g$itime)
g$dayhour = floor_date(g$itime, unit = "hours")

nurses = unique(g$hid)

subG = filter(g, hid == nurses[1] | hid == nurses [2] | hid ==nurses[3] | hid ==nurses[4])
G<-table(g$hid, g$dayhour)

H<- as.vector(G)
ggplot(data = G, mapping = aes(x= dayhour)) + geom_point()


dfG <-data.frame()
 ##maybe can add efficency by not calling colnames everytime and instead storing it. 


for(h in 1:nrow(G)){
  for(t in 1:ncol(G)){
    dfG <-rbind(dfG, c(G[h,t], colnames(G)[t], rownames(G)[h]))
  }
}


dfG =`colnames<-`(dfG, c("freq", "itime", "hid"))
dfG$itime <-as.POSIXct(dfG$itime)
dfG$hid <- factor(dfG$hid)

ggplot(data = dfG, aes(x=i2, y=freq )) +geom_point() + geom_boxplot()
 dfG$i2 = factor(dfG$itime) 
 
hist(dfG$freq)

dfG$freq <-as.numeric(dfG$freq)

subG$otime <-as.POSIXct(subG$otime)
subG$hid <- as.factor(subG$hid)
ggplot(subG) + geom_segment(aes(x = hid, xend = hid, y=itime, yend=otime), color = "black")   #+ geom_point(aes(x=hid, y=itime), color = "red") + geom_point(aes(x = hid, y= otime, color = "blue")) + coord_flip()
ggplot(subG, aes(x = hid, y = dayhour, color = shift))  + geom_point() + coord_flip()
  
g$hid <- as.factor(g$hid)
  
  
  
  
## How is shift being labeled? 
DayShifts <-filter(f, shift == "day")
NightShifts <- filter(f, shift =="night")

ggplot(data = g, aes(x= hour)) + geom_bar( aes( color = shift))
ggplot( data = subG, mapping = aes(x = dayhour, y = hid, color = shift)) + geom_point()
  #this plot seems to indicate that in fact the shift is not necessarily consistent with being a "shift worker" but rather is arbitrary. 
  #how can I test this more widely? 

#what percentage/frequency of visits are at a particular time

NightVDay <- addmargins(table(f$hid, f$shift))
percentageND <-data.frame()
percentageND$p <- apply(NightVDay,c(1,3), "/" )



## Plot the percentages of day/night

#Want to end with the quantity of 
## total shifts in a hour/days at the hospital
## then add ggridges

g$day = day(g$itime)
h = as.matrix(table(g$hid, g$hour ))
h2= table(g$hid, g$day)
h3 = matrix(as.numeric(h2 >0), ncol = 5)

h4 = addmargins(h3)
h4 =as.matrix(h4, ncol = 1)
h4= h4[-169,6]

cbind(h, h4)



 h = as.data.frame(h)
 head(h)
 as.data.frame(h4)
 h =`colnames<-`(h, c("hid", "hour", "freq"))
h4 = matrix(c(h4,) , ncol = 2)

h4 =`rownames<-`(h4, rownames(table(g$hid, g$hour )))
h4 = as.data.frame(h4)
h4 =`colnames<-`(c("daysworked","hid"), h4)

h4$hid =rownames(h4)

h$daysworked = rep(1, nrow(h))
match(h$hid, rownames(h4))

h$daysworked = h4[match(h$hid, rownames(h4)),1]

h$avg = h$freq/h$daysworked
h$hour =as.factor(h$hour)

ggplot(h, aes(x=avg, y= hour, fill = hour)) + geom_density_ridges()
ggplot(h, aes(x=avg)) + geom_density() +geom_bar()


#is there some way to determine if the hcw was plausiblely at the hospital at a specific time? 
#I guess look at the specific segments that each one worked

subG = filter(g, hid %in% unique(g$hid)[1:5])
ggplot(data =subG, aes(x = dayhour, y =hid)) + geom_point()

## okay so ill look at min and max worked everyday, basically i want to find contiguous pieces of time at the hospital
## i really am stumped on how to get rid of the 0 cases


### okay another approach could be by using ZIP (zero inflated poisson):
library(pscl)
h =`colnames<-`(h, c("hid", "hour", "freq"))
h$daysworked = h4[match(h$hid, rownames(h4)),1]
h$avg = h$freq/h$daysworked

lm_out <- zeroinfl(h$freq ~ h$daysworked, data = h)

newdata = expand.grid(1:7)
colnames(newdata) = c("daysworked")
newdata$phat = predict(lm_out, newdata)

lm_out2 <-zeroinfl(h$freq ~1, data = h)

#Another try lettts goooo
G =table(g$hid, g$dayhour)
nurseVisits <- as.data.frame(table(g$hid, g$dayhour))
zipNurse<- zeroinfl(nurseVisits$Freq ~ 1, dist = "poisson")
rootogram(zipNurse, style ="standing")
