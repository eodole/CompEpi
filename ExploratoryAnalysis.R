library(readxl)
library(tidyverse)

path = "~/Desktop/CompEpi/Results/"
setwd(path)

sheet = excel_sheets("VisitFreqResults.xlsx")

results = lapply(setNames(sheet,sheet), function(x) read_excel("VisitFreqResults.xlsx", sheet =x, col_types =  c("numeric","text","numeric","numeric")))
results = bind_rows(results, .id = "Sheet")

ggplot(results, mapping = aes(x = `Job Type ID`, y = Estimate )) + geom_point(aes(col = Sheet))

ggplot(results,mapping = aes(x=Estimate))+
  geom_histogram() +
  geom_density(aes(kernel = "gaussian"))

results_j3 = filter(results, `Job Type ID` == 3)

df = data.frame(x=1:10)
jt3 = lapply(setNames(1:7, results_j3$Sheet[1:7]), function(x) dpois(1:10,exp(results_j3$Estimate[x])))
df = cbind(df, bind_cols(l))

#JT 3 Poisson Plot
matplot(df[2:8], type = "l", pch =1, col=1:7, ylab = "Density", main = "Poisson Density for Job Type 3")       


results_jt12 = filter(results, `Job Type ID` ==12)
jt12 = lapply(setNames(1:7, results_jt12$Sheet[1:7]), function(x) dpois(1:10, exp(results_jt12$Estimate[x]))) 
jt12 = bind_cols(jt12)
matplot(jt12, type = "l", col = 1:7, ylab= "Density", main = "Poisson Density for Job Type 12")
