setwd("C:/Users/Toast/Dropbox/PhD/psych234")

# clears workspace:  
rm(list=ls()) 

library(R2jags)
library(tidyverse)


dist <- read.csv(file = "dist.csv", header=FALSE)
y2 <- c(15,19,18,13,25,30,10,22,28,16,2,11,1,12,4,8,24,14,29,23,21,3,5,9,7,17,26,20,6,27)


#doing dist shenanigans
setwd("C:/Users/Kevin/Dropbox/PhD/psych234/city30")
distfiles <- list.files(path=".",pattern = "(sub00).*\\.csv$") %>%
  map_df(~read_csv(.))
dist <- distfiles

#doing y shenanigans
#bb <-read.csv("C:/Users/Kevin/Dropbox/PhD/psych234/city30/solution/sol30_sub0_prob0.csv")
setwd("C:/Users/Kevin/Dropbox/PhD/psych234/city30/solution")
yfiles <- list.files(path=".",pattern = "(sub00).*\\.csv$") %>%
  map_df(~read_csv(.))

colnames(yfiles)[] <- ""
y <- as.list(t(yfiles))


n <-nrow(dist)
cities <- ncol(dist)

data <- list("dist","n","y","cities")
myinits <- list( list(gamma = runif(1,1,2)) )
parameters <- c("gamma")

setwd("C:/Users/Kevin/Dropbox/PhD/psych234")
samples30 <- jags(data, inits=myinits, parameters,
                model.file ="model2.txt", n.chains=1, n.iter=1000, 
                n.burnin=1, n.thin=1, DIC=T)

# Now the values for the monitored parameters are in the "samples" object, 
# ready for inspection.
samples

plot(samples)
mean.gamma <- samples$BUGSoutput$mean$gamma
simlist.gamma <- samples$BUGSoutput$sims.list

#some plotting options to make things look better:
par(cex.main = 1.5, mar = c(5, 6, 4, 5) + 0.1, mgp = c(3.5, 1, 0), cex.lab = 1.5,
    font.lab = 2, cex.axis = 1.3, bty = "n", las=1)
# the plotting: 
plot(c, type="l", main="", ylab="Values", xlab="Samples")
lines(c(1, mean.mu1), c(mean.mu1,mean.mu1), lwd=2, col="red")

plot(samples)

lm1_mcmc <- as.mcmc(samples)
plot(lm1_mcmc)

PR <- dunif(1,0,50)
MCMCtrace(samples, 
          params = c('gamma'),
          ISB = FALSE,
          exact = TRUE,
          priors = PR
          pdf = FALSE,
          Rhat = TRUE,
          n.eff = TRUE)

