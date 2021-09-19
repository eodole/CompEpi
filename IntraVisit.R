### Intermittent Times ###

facilityOfInterest <- read.csv("~/Desktop/CompEpi/facility43.csv", sep = "\t")
facilityOfInterest$hid <- as.factor(facilityOfInterest)
tapply(facilityOfInterest, INDEX = facilityOfInterest$hid, compute_Intravisit_Time)

compute_Intravisit_Time = function(x){
  v <- c()
  for (r in 2:nrows(x)){
    v <- c(v, x$otime[r] - x$itime[r])
  }
  return(v)
}
