

#Load Libraries 
library(pscl)
library(dplyr)
library(lubridate)

## This code generates a zero-inflated poisson distribution to describe 
## the number of visits healthcare workers make in the an hour. 
## Results are printed to a text file. 

#Load Data 
inputs = commandArgs(trailingOnly = TRUE)
print(inputs)						
g <- read.csv(paste("~/newdata/", inputs[1], sep = ""), sep = "\t")                               
  for(hcw in 1:33){
    #Label the Output

    #Filter the data to have a specific jobtype
    hcwOfInterest <-  dplyr::filter(g, jtid == hcw, daytype == inputs[2])
    print(paste("Group Facility IDs:", unique(hcwOfInterest$rfid), "Job Type ID:", hcw, sep = " " ))

    #Condition: not enough data to build a reasonable distribution
    if(nrow(hcwOfInterest) < 25){
      print("Less Than 25 Observations")
    }else{
      #What time of day that the observations are  made, rounded to nearest hour
      hcwOfInterest$dayhour = floor_date(as.POSIXct(hcwOfInterest$itime), unit = "hours")
      hcwVistsPerHour = as.data.frame(table(hcwOfInterest$hid, hcwOfInterest$dayhour))
      
      #Fit count data 
      zipVisits = zeroinfl(hcwVistsPerHour$Freq ~ 1, dist = "poisson")
      
      #Print parameters and basic diagnostics
     print(summary(zipVisits))}
    print("=========================")
  }
}
