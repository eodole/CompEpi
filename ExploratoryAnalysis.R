library(readxl)
library(tidyverse)
library(ggridges)

path = "~/Desktop/CompEpi/Results/"
setwd(path)

sheet = excel_sheets("VisitFreqResults.xlsx")

results = lapply(setNames(sheet,sheet), function(x) read_excel("VisitFreqResults.xlsx", sheet =x, col_types =  c("numeric","text","numeric","numeric")))
results = bind_rows(results, .id = "Sheet")

#All results as geompoint
ggplot(results, mapping = aes(x = `Job Type ID`, y = Estimate )) + geom_point(aes(col = Sheet))

#All results as hist
ggplot(results,mapping = aes(x=Estimate, fill = `Job Type ID`, color = `Job Type ID`))+
  geom_histogram(alpha = 0.5, binwidth = 0.05) 
  #geom_density(aes(kernel = "gaussian"))

#All results as ridges by jobtype
ggplot(results) +
  geom_density_ridges(aes(x = Estimate, y = `Sheet`, fill = Sheet))

results_j3 = filter(results, `Job Type ID` == 3)

df =  seq(1,10,0.1)
jt3 = lapply(setNames(1:7, results_j3$Sheet[1:7]), function(x) dpois(1:10,exp(results_j3$Estimate[x])))
df = cbind(df, bind_cols(l))

#JT 3 Poisson Plot
matplot(df[2:8],type ="l", pch =1, col=1:7, ylab = "Density", main = "Poisson Density for Job Type 3")       


results_jt12 = filter(results, `Job Type ID` ==12)
jt12 = lapply(setNames(1:7, results_jt12$Sheet[1:7]), function(x) dpois(1:10, exp(results_jt12$Estimate[x]))) 
jt12 = bind_cols(jt12)
matplot(jt12, type = "l", col = 1:7, ylab= "Density", main = "Poisson Density for Job Type 12")


results_jt1 = filter(results,`Job Type ID` ==1 )
jt1 = lapply(setNames(1:11, results_jt12$Sheet[1:11]), function(x) dpois(0:10, exp(results_jt1$Estimate[x]))) 
jt1 = bind_cols(jt1)
matplot(jt1, type = "l", col = 1:11, lty = 1:11,ylab= "Density", main = "Poisson Density for Job Type 1") 
#legend("topright", names(jt1), col = 1:11, lty = 1:11)

results_jtavg <- results %>% na.omit() %>% group_by(`Job Type ID`) %>%
  summarize(Avg_Est = mean(Estimate))

results_sheetavg <- results %>% na.omit() %>% group_by(Sheet) %>% summarize(Avg_Est = mean(Estimate))

ggplot(results_sheetavg, aes(color = Sheet, xlab = "none")) + geom_bar(aes(x = Sheet, y= Avg_Est),stat = "identity")

