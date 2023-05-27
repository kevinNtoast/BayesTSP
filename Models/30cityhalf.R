setwd("C:/Users/Toast/Dropbox/PhD/psych234")

# clears workspace:  
rm(list=ls()) 

library(R2jags)
library(tidyverse)

#doing dist shenanigans
setwd("C:/Users/Kevin/Dropbox/PhD/psych234/city30")
distfiles <- list.files(path=".",pattern = "*\\.csv$") %>%
  map_df(~read_csv(.))
dist <- distfiles

#doing y shenanigans
#bb <-read.csv("C:/Users/Kevin/Dropbox/PhD/psych234/city40/solution/sol30_sub0_prob0.csv")
setwd("C:/Users/Kevin/Dropbox/PhD/psych234/city30/solution")
yfiles <- list.files(path=".",pattern = "solutioncomplete.csv$") %>%
  map_df(~read_csv(.))

colnames(yfiles)[] <- ""
y <- yfiles

subjects <- 82
n <-252
cities <- ncol(dist)

data <- list("dist","n","y","cities","subjects")
myinits <- list( list(gamma = cbind(rep(1,82), rep(1,82))))
parameters <- c("gamma")

setwd("C:/Users/Kevin/Dropbox/PhD/psych234")
samples30half <- jags(data, inits=myinits, parameters,
                  model.file ="modelhalf.txt", n.chains=1, n.iter=1000, 
                  n.burnin=1, n.thin=1, DIC=T)

# Now the values for the monitored parameters are in the "samples" object, 
# ready for inspection.
samplesind

plot(samples30half)
mean.gamma <- samples$BUGSoutput$mean$gamma
simlist.gamma <- samples$BUGSoutput$sims.list

sam30h <- data.frame(samples30half$BUGSoutput$mean$gamma)
pl <- ggplot(sam30h, aes(x = sam30h[,1], y = sam30h[,2])) +
  geom_point() +
  geom_smooth(method=lm)

pl+geom_segment(aes(x=10, y=10, xend=40, yend=40)) +labs(x = "First half", y="Second Half")
  
pl + xlim(10, 40)+ylim(10,40)+labs(x = "First half", y="Second Half")
  


#some plotting options to make things look better:
par(cex.main = 1.5, mar = c(5, 6, 4, 5) + 0.1, mgp = c(3.5, 1, 0), cex.lab = 1.5,
    font.lab = 2, cex.axis = 1.3, bty = "n", las=1)

mcmc <- as.mcmc(samples30half)
plot(mcmc)


MCMCsummary(mcmc)
MCMCtrace(mcmc, params = c('gamma'),ISB = FALSE, exact = TRUE, type = 'density', pdf = FALSE)
MCMCplot(mcmc, params = 'gamma', ci = c(50,90), HPD = TRUE)
