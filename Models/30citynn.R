setwd("C:/Users/Toast/Dropbox/PhD/psych234")

# clears workspace:  
rm(list=ls()) 

library(R2jags)
library(tidyverse)

#doing dist shenanigans
setwd("C:/Users/Kevin/Dropbox/PhD/psych234/city30_nn2")
distfiles <- list.files(path=".",pattern = "*\\.csv$") %>%
  map_df(~read_csv(.))
dist <- distfiles

#doing y shenanigans
#bb <-read.csv("C:/Users/Kevin/Dropbox/PhD/psych234/city40/solution/sol30_sub0_prob0.csv")
setwd("C:/Users/Kevin/Dropbox/PhD/psych234/city30_nn2/solution")
yfiles <- list.files(path=".",pattern = "solutioncomplete.csv$") %>%
  map_df(~read_csv(.))

colnames(yfiles)[] <- ""
y <- yfiles

subjects <- ncol(y)
n <-nrow(y)
cities <- ncol(dist)

data <- list("dist","n","y","cities","subjects")
myinits <- list( list(gamma = rep(1,ncol(y)) ))
parameters <- c("gamma")

setwd("C:/Users/Kevin/Dropbox/PhD/psych234")
samples30nn <- jags(data, inits=myinits, parameters,
                  model.file ="modelind.txt", n.chains=1, n.iter=1000, 
                  n.burnin=1, n.thin=1, DIC=T)

# Now the values for the monitored parameters are in the "samples" object, 
# ready for inspection.
samples30nn

plot(samples30nn)
mean.gamma <- samples$BUGSoutput$mean$gamma
simlist.gamma <- samples$BUGSoutput$sims.list

#some plotting options to make things look better:
par(cex.main = 1.5, mar = c(5, 6, 4, 5) + 0.1, mgp = c(3.5, 1, 0), cex.lab = 1.5,
    font.lab = 2, cex.axis = 1.3, bty = "n", las=1)

mcmc <- as.mcmc(samples30nn)
plot(mcmc)


MCMCsummary(mcmc)
MCMCtrace(mcmc, params = c('gamma[84]', 'gamma[85]'),ISB = FALSE, exact = TRUE, type = 'density', pdf = FALSE)
MCMCplot(mcmc, params = 'gamma', ci = c(50,90), HPD = TRUE)
