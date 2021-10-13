
# load the data from .Rdata file load()
#assume we are working with hcwOfInterest

#### fix the groups thing change it to a list. lol not just c() which will append. 

#inputs = commandArgs(trailingOnly = T)

#filename = paste("group", input[1], "jtid", input[2], ".Rdata")

inputs = commandArgs(trailingOnly = TRUE)
print(inputs)
library(mclust)
library(dplyr)

#g = read.csv(paste("~/newdata/", inputs[1], sep = ""), sep = "\t")
#g = read.csv(inputs[1], sep = "\t")
# print("Done")
#   for (hcw in 1:33){
#     print("newloop")
#     hcwOfInterest = dplyr::filter(g, jtid == hcw, daytype == inputs[2])
#     if(nrow(hcwOfInterest) != 0){
#         duration_data = log(hcwOfInterest$duration)
# 	maxG = min(15,( nrow(duration_data)/20))
#         fit_k = Mclust(duration_data, G = 1:maxG)
#         print(paste("facilities", unique(hcwOfInterest$fid), "jtid:",hcw ,"daytype: ", inputs[2], sep = " "))
#         print(fit_k$parameters)
#         print("========================================")
#     }	
#   } 

 




