library(misaem)

N <- 100  # number of subjects
p <- 3     # number of explanatory variables
mu.star <- rep(0,p)  # mean of the explanatory variables
Sigma.star <- diag(rep(1,p)) # covariance
beta.star <- c(1, 1,  0) # coefficients
beta0.star <- 0 # intercept
beta.true = c(beta0.star,beta.star)
X.complete <- matrix(rnorm(N*p), nrow=N)%*%chol(Sigma.star) +
  matrix(rep(mu.star,N), nrow=N, byrow = TRUE)
p1 <- 1/(1+exp(-X.complete%*%beta.star-beta0.star))
y <- as.numeric(runif(N)<p1)

# Generate missingness
p.miss <- 0.10
patterns <- runif(N*p)<p.miss #missing completely at random
X.obs <- X.complete
X.obs[patterns] <- NA

df.obs = data.frame(y,X.obs)
miss.list = miss.glm(y~., data=df.obs, print_iter=FALSE,seed=100)
summary(miss.list)

df.complete = data.frame(y,X.complete)
lr_full <- glm(y~., data=df.complete, family='binomial')
summary(lr_full)
