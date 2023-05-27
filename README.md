# BayesTSP

## Research Question
Is there an individual difference between people in solving the Traveling Salesperson Problem (TSP)?

The traveling salesperson problem is a popular algorithm optimization problem, where given a set of points or cities, an agent must visit every city while minimizing the distance traveled.
Computers and computer algorithms have a very set way of solving the problem, and the main optimization point comes from minimizing the time spent. Though the problem could be solved by trying every single tour
possible on every single problem, this also means that there is an exponential increase in time and tours needed to be compared in order to reach the optimal tour.
However, humans have displayed an ability to solve these problems very very quickly and at near-optimal levels. The question here is how this occurs. Humans can solve problems that computers take ages to solve.

This project explored how varying values of delta(γ), which is a variable determining how rigidly someone or something chose the next city to visit in a traveling salesperson problem.
A low value of γ, nearing 0, means that the next city chosen to visit would be completely at random. This would lead to highly sub-optimal tours to be formed and a bad performance on the problem.
A high value of γ, which in the analysis was near values of 10, would be choosing the closest city from the current point. This would mean that the agent is following the nearest neighbor algorithm
in order to solve the problem. The nearest neighbor algorithm is defined as choosing the next city of lowest distance and yields decent results in optimizing the problem, there are cases where this does not apply and the
resulting tour is highly suboptimal.

This is an exploratory analysis of the dataset of Chronicle et. al. (2008), which includes 82 participants’ solutions to 9 TSP problems, of 30- and 40-city problems. 
The dataset was modified and organized such that each column represents each participant, and each row represents the index choice they made on the original TSP problem.
A distance matrix is available, of each participant’s available distances to other cities from the current city they are in at each choice.

A Bayesian Model was applied to explore the deterministic nature of human solutions to the problem, and compared to with algorithmic solutions. Three total models were used in this analysis.
The first model assumed that there were no individual differences between people. Everyone chose the next city with the same decision-making process. The second model assumed individual differences 
allowing for people to choose with different justifications. The third model assumed that there were two types of determinism. The first half of the problem involved one value, and while the tour comes to a close 
on the second half the problem, a different value was used.


  
## Dataset  
### Data  
  
The dataset is from Chronicle et. al. (2008), and includes 82 participants’ solutions to 9 TSP problems, of 30- and 40-city problems. 
The dataset was modified and organized such that each column represents each participant, and each row represents the index choice they made on the original TSP problem.
A distance matrix is available, of each participant’s available distances to other cities from the current city they are in at each choice.
 
|![PGN File](/images/Model1.png)|
|:--:| 
|Figure 1. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
   
## Model Summary 
The model here is indicated by i choices and j people, which make up the row and columns of the dataset $$c_ij$$. The model also takes in the distance matrix at each choice for each participant, $$d_i$$.
The γ value is the hidden value that guides the choice heuristics for people’s solutions. This value is implemented in $$s_ij$$, where s is the softmax function, defined as the following:
$$P(x)=  {e^(-γd_cx^  )}/{(∑_(p∈all others)e^(-γd_cx^  ) )} = {distance to chosen point}/{sum of distance of all other points}$$
The function is carried out by comparing a specific choice of city to all others and choosing the best city. Depending on the γ value, this specific choice may change, and the question for this model is identifying the difference in this γ value per person. This γ value can range from 0 from 50, as it is initialized using dunif(0,50) in this current version. Values closer to 0 signify random choice between all available cities, and values closer to 50 correspond to strictly choosing closest cities, or more deterministic choices.


## The First Model

The first model, also known as the test model, assumed that every person had the same γ value. 

model.txt – Assumes same γ for everyone
model{
  for (i in 2:(n-1)){
    y[i] ~ dcat(theta[i, ])
    for (j in 1:n){
          theta[i, j] = exp(-gamma*dist[i-1, j])
    }
  }
  gamma ~ dunif(0,50)
}

The resulting density for the model is shown here. For one subject:
|![30c](/images/30city_s1.png)|
|:--:| 
|Figure 2. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|

|![40c](/images/40city_s1.png)|
|:--:| 
|Figure 3. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
This was the result for the first subject, with the graph on the left being the 30-city environment and the graph on the right being the 40-city environment. 
The following is the resulting model on all subjects in 30-city:
|![nid](/images/NoInddiff.png)|
|:--:| 


## Second Model
The second model includes room for individual differences.

|IndividualDiff.txt – Includes individual gamma values per person
model{
  for(i in 1:subjects){
    for(j in 1:n){
      for(k in 1:cities){
        theta[i,j,k] = exp(-1*gamma[i]*dist[n*(i-1)+j,k])
      }
    }
  }
  for(i in 1:subjects){
    for(j in 1:n){
      y[j,i] ~ dcat(theta[i,j , ])
    }
  }
  for(i in 1:subjects){
    gamma[i] ~ dunif(0,50)
  }
}|

|![40c](/images/rstudio_JULNzrax9h.png)|
|:--:| 
|![40c](/images/rstudio_9rsKXpav20.png)|
|:--:| 
|Figure 5. The above are the results for the 30- and 40-city environments. It can be seen that values on average are higher in the 40-city environments as opposed to 30-city environments.|

The above are the results for the 30- and 40-city environments. It can be seen that values on average are higher in the 40-city environments as opposed to 30-city environments.

|![40c](/images/Solve1.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
|![40c](/images/Solve2.png)|
|:--:| 
|Figure 7. 
This is an example of someone with high deterministic choice.|


Additional analysis on the tour themselves could possibly be done to see intersects or differences between the tour themselves.


|![40c](/images/Graph1.png)|
|:--:| 
|Figure 8. This is the scatterplot portraying the comparison between 30-city on the x axis and 40-city on the y axis. It can be seen that on average, people are more deterministic in the 40-city environment over the 30-city environment.|

|![40c](/images/Graph2.png)|
|:--:| 
|![40c](/images/Graph3.png)|
|:--:| 
|Figure 10. The above show the graphs of sample random tour (left) and the nearest neighbor tour (right).|
The above show the graphs of sample random tour (left) and the nearest neighbor tour (right). This verifies that random tours are closer to γ=0 and completely nearest neighbor tours are close to γ=50. This reinforces our idea that human solvers have some γ value in the middle, not completely nearest  neighbor and not completely random.

Additionally, an optimal solution was added as a tour in the model.
|![40c](/images/Graph4.png)|
|:--:| 
|![40c](/images/Graph5.png)|
|:--:| 
|Figure 12.Here, the red point is the gamma value of the optimal solution.|

Here, the red point is the gamma value of the optimal solution. The x-axis is measured based on the proportion longer than the optimal solution, where farther to the right the point is, the longer it is than the optimal solution. It seems difficult to identify a trend between the gamma values and the proximity to the optimal solution. 


## Third Model
The third model answers the question about whether people have different values while they are starting the tour vs when they are finishing the tour.
|![40c](/images/Graph6.png)|
|:--:| 
|Figure 13. Above is the model interpretation.|

Above is the model interpretation, where each person would have two different γ values, one for the first half of the tour and one for the second half of the tour.
|![40c](/images/Graph7.png)|
|:--:| 
|Figure 14. Above is the resulting graph of 30- and 40-city tours divided by the first and second half..|
At first glance, it seem there is no significant difference between the two halves, as most points are nearby the y=x line.
|![40c](/images/Graph8.png)|
|:--:| 
|![40c](/images/Graph9.png)|
|:--:| 
|![40c](/images/Graph10.png)|
|:--:| 
|Figure 17. bove are the two scatterplots comparing the first and last across the two different city counts.|
Above are the two scatterplots comparing the first and last across the two different city counts. The trends between the first and last half of each seem similar, so from the results it shows that either at a local level there is no significant difference, or that splitting the tour in half is not a proper metric to observer difference in local choices.
