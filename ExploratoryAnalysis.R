library(readxl)
library(tidyverse)

path = "~/Desktop/CompEpi/Results/"
setwd(path)

sheet = excel_sheets("VisitFreqResults.xlsx")

results = lapply(setNames(sheet,sheet), function(x) read_excel("VisitFreqResults.xlsx", sheet =x, col_types =  c("numeric","text","numeric","numeric")))
results = bind_rows(results, .id = "Sheet")

ggplot(results, mapping = aes(x = `Job Type ID`, y = Estimate )) + geom_point(aes(col = Sheet))

