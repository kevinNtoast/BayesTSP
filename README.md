# BayesTSP

## Research Question
Is there an individual difference between people in solving the Traveling Salesperson Problem (TSP)?
  
## Dataset  
### Data  
  
The dataset is from Chronicle et. al. (2008), and includes 82 participants’ solutions to 9 TSP problems, of 30- and 40-city problems. 
The dataset was modified and organized such that each column represents each participant, and each row represents the index choice they made on the original TSP problem.
A distance matrix is available, of each participant’s available distances to other cities from the current city they are in at each choice.
 
|![PGN File](/images/Model1.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
   
### Model Summary 
The model here is indicated by i choices and j people, which make up the row and columns of the dataset c_ij. The model also takes in the distance matrix at each choice for each participant, d_i.
The γ value is the hidden value that guides the choice heuristics for people’s solutions. This value is implemented in s_ij, where s is the softmax function, defined as the following:
P(x)=  e^(-γd_cx^  )/(∑_(p∈all others)▒e^(-γd_cx^  ) ) = distance to chosen point/sum of distance of all other points
The function is carried out by comparing a specific choice of city to all others and choosing the best city. Depending on the γ value, this specific choice may change, and the question for this model is identifying the difference in this γ value per person. This γ value can range from 0 from 50, as it is initialized using dunif(0,50) in this current version. Values closer to 0 signify random choice between all available cities, and values closer to 50 correspond to strictly choosing closest cities, or more deterministic choices.


### The First Model
First Model
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
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|

|![40c](/images/40city_s1.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
This was the result for the first subject, with the graph on the left being the 30-city environment and the graph on the right being the 40-city environment. 
The following is the resulting model on all subjects in 30-city:
|![nid](/images/NoInddiff.png)|
|:--:| 


Second Model
The second model includes room for individual differences.
IndividualDiff.txt – Includes individual gamma values per person
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
}

|![40c](/images/rstudio_JULNzrax9h.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|


|![40c](/images/rstudio_9rsKXpav20.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|

The above are the results for the 30- and 40-city environments. It can be seen that values on average are higher in the 40-city environments as opposed to 30-city environments.

|![40c](/images/Solve1.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|

|![40c](/images/Solve2.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|

This is an example of someone with high deterministic choice.

Additional analysis on the tour themselves could possibly be done to see intersects or differences between the tour themselves.


|![40c](/images/Graph1.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
This is the scatterplot portraying the comparison between 30-city on the x axis and 40-city on the y axis. It can be seen that on average, people are more deterministic in the 40-city environment over the 30-city environment.


|![40c](/images/Graph2.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
|![40c](/images/Graph3.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
The above show the graphs of sample random tour (left) and the nearest neighbor tour (right). This verifies that random tours are closer to γ=0 and completely nearest neighbor tours are close to γ=50. This reinforces our idea that human solvers have some γ value in the middle, not completely nearest  neighbor and not completely random.

Additionally, an optimal solution was added as a tour in the model.
|![40c](/images/Graph4.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
Above is the resulting density of the optimal solution on the model, with the mean value being 23.3. The tours were measured against the optimal solution, and plotted against the gamma values as such:

|![40c](/images/Graph5.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|

Here, the red point is the gamma value of the optimal solution. The x-axis is measured based on the proportion longer than the optimal solution, where farther to the right the point is, the longer it is than the optimal solution. It seems difficult to identify a trend between the gamma values and the proximity to the optimal solution. 


Third Model
The third model answers the question about whether people have different values while they are starting the tour vs when they are finishing the tour.
|![40c](/images/Graph6.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|

Above is the model interpretation, where each person would have two different γ values, one for the first half of the tour and one for the second half of the tour.
|![40c](/images/Graph7.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
Above is the resulting graph of 30- and 40-city tours divided by the first and second half. At first glance, it seem there is no significant difference between the two halves, as most points are nearby the y=x line.
|![40c](/images/Graph8.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
|![40c](/images/Graph9.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|


|![40c](/images/Graph10.png)|
|:--:| 
|Figure 6. The error rate of the neural network in data requiring the corresponding piece needed to move for checkmate.|
Above are the two scatterplots comparing the first and last across the two different city counts. The trends between the first and last half of each seem similar, so from the results it shows that either at a local level there is no significant difference, or that splitting the tour in half is not a proper metric to observer difference in local choices.
## Results 
|
## Discussion  

  
## References  
Oshri, B., & Khandwala, N. (2016). Predicting moves in chess using convolutional neural networks.    
  
Silver, D., Hubert, T., Schrittwieser, J., Antonoglou, I., Lai, M., Guez, A., ... & Lillicrap, T. (2018). A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play. Science, 362(6419), 1140-1144.  
  
Vikström, J. (2019). Training a Convolutional Neural Network to Evaluate Chess Positions.  
