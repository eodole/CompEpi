

#Load Libraries 
library(pscl)
library(dplyr)


#Load Data 
inputs = commandArgs(trailingOnly = TRUE)
print(inputs)						
g <- read.csv(paste("~/newdata/", inputs[1], sep = ""), sep = "\t")                               
for(hcw in 1:33){

  #Filter the data to have a specific jobtype
  hcwOfInterest <-  dplyr::filter(g, jtid == hcw, daytype == inputs[2], shift2 = inputs[3])
  #hcwOfInterest <-  dplyr::filter(g, jtid == 1, daytype == "weekday", shift2 == "day")
  
  #Label the Output
  print(paste("Group Facility IDs:", unique(hcwOfInterest$rfid), "Job Type ID:", hcw, sep = " " ))
  
  #What is too small to fit? For a zero inflated poisson
  if(nrow(hcwOfInterest) < 25){
    print("Less Than 25 Observations")
  }else{
    hcwTable = as.data.frame(table(hcwOfInterest$hid, hcwOfInterest$rid))
    
    
    #Fit count data 
    zipVisits = zeroinfl(hcwTable$Freq ~ 1, dist = "poisson")
    
    #Print parameters and basic diagnostics
    print(summary(zipVisits))}
    print("=========================")
}
}
