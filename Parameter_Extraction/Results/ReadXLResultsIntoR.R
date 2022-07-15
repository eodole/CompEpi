library(readxl)
library(tidyverse)

path = "path_to_result_file"
setwd(path)

sheet = excel_sheets("VisitFreqResults.xlsx")
#sheet = excel_sheets("DurationResults.xlsx")

results = lapply(setNames(sheet,sheet), function(x) read_excel("VisitFreqResults.xlsx", sheet =x, col_types =  c("numeric","text","numeric","numeric")))
results = bind_rows(results, .id = "Sheet")

head(results)
