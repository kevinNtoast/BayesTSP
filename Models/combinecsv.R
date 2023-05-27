library(dplyr)
library(readr)

setwd("C:/Users/Toast/Dropbox/PhD/psych234/city30_problem0/solution")

d <- list.files(path="C:/Users/Toast/Dropbox/PhD/psych234/city30_problem0/solution", full.names = FALSE) %>%
  lapply(read_csv) %>%
  bind_rows

write.csv(d, "C:/Users/Toast/Dropbox/PhD/psych234/city30_problem0/solution/s1.csv")


multmerge = function(path){
  filenames=list.files(path=path, full.names=TRUE)
  rbindlist(lapply(filenames, fread))
}

path <- "C:/Users/Toast/Dropbox/PhD/psych234/city30_problem0/solution"
DF <- multmerge(path)
