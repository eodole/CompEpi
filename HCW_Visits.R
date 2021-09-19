

#Load Libraries 
library(pscl)
library(dplyr)
library(lubridate)

#Load Data 
inputs = commandArgs(trailingOnly = TRUE)
print(inputs)						
g <- read.csv(paste("~/newdata/", inputs[1], sep = ""), sep = "\t")                               
  for(hcw in 1:33){
    #Label the Output

    #Filter the data to have a specific jobtype
    hcwOfInterest <-  dplyr::filter(g, jtid == hcw, daytype == inputs[2])
    print(paste("Group Facility IDs:", unique(hcwOfInterest$fid), "Job Type ID:", hcw, sep = " " ))

    #What is too small to fit? For a zero inflated poisson
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
