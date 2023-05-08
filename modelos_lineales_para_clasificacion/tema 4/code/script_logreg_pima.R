library(glmnet)
library(ggplot2)
library(GGally)
library(caret)
library(mlbench)
library(tidyverse)
library(dplyr)

# Load the data and remove NAs
data("PimaIndiansDiabetes2", package = "mlbench")
PimaIndiansDiabetes2 <- na.omit(PimaIndiansDiabetes2)

# The Pima Indians Diabetes Dataset involves predicting the onset of diabetes 
# within 5 years in Pima Indians given medical details.
# 
# pregnant	Number of times pregnant
# glucose	Plasma glucose concentration (glucose tolerance test)
# pressure	Diastolic blood pressure (mm Hg)
# triceps	Triceps skin fold thickness (mm)
# insulin	2-Hour serum insulin (mu U/ml)
# mass	Body mass index (weight in kg/(height in m)\^2)
# pedigree	Diabetes pedigree function
# age	Age (years)
# diabetes	Class variable (test for diabetes)

# Inspect the data
sample_n(PimaIndiansDiabetes2, 3)
# Split the data into training and test set
set.seed(123)
training.samples <- PimaIndiansDiabetes2$diabetes %>% 
  createDataPartition(p = 0.8, list = FALSE)
train.data  <- PimaIndiansDiabetes2[training.samples, ]
test.data <- PimaIndiansDiabetes2[-training.samples, ]

# Dumy code categorical predictor variables
# model.matrix() helps to create the matrix of predictors and also 
#   automatically converts categorical predictors to appropriate dummy variables
x <- model.matrix(diabetes~., train.data)[,-1]
# Convert the outcome (class) to a numerical variable REQUIRED for glmnet
y <- ifelse(train.data$diabetes == "pos", 1, 0)

# computing penalized logistic regression.
# alpha: the elasticnet mixing parameter. Allowed values include:
#   “1”: for lasso regression
#   “0”: for ridge regression
#   a value between 0 and 1 (say 0.3) for elastic net regression.
l1mod_1 <- glmnet(x, y, family = "binomial", alpha = 1, lambda = 0.05)
coef(l1mod_1)
# The best lambda for your data is the lambda that minimize the 
#   cross-validation prediction error rate. 
# Determined automatically using the function cv.glmnet().
set.seed(123) 
cv.lasso <- cv.glmnet(x, y, alpha = 1, family = "binomial")
# The plot displays the cross-validation error according to the log of lambda.
#   The left dashed vertical line indicates that the log of the optimal value of 
#   lambda is approximately -5, which is the one that minimizes the prediction error.
plot(cv.lasso)
# Using lambda.min as the best lambda, gives the following regression coefficients:
coef(cv.lasso, cv.lasso$lambda.min)

#
# Compute the final model using lambda.min:
# Fit the final model on the training data
model <- glmnet(x, y, alpha = 1, family = "binomial",
                lambda = cv.lasso$lambda.min)
# Display regression coefficients
coef(model)

# Make predictions on the test data
x.test <- model.matrix(diabetes ~., test.data)[,-1]
probabilities <- model %>% predict(newx = x.test, type="response")
predicted.classes <- ifelse(probabilities > 0.5, "pos", "neg")
# Model accuracy
observed.classes <- test.data$diabetes
mean(predicted.classes == observed.classes)


# Compute the full logistic model
# Fit the model
full.model <- glm(diabetes ~., data = train.data, family = binomial)
# Make predictions
probabilities <- full.model %>% predict(test.data, type = "response")
predicted.classes <- ifelse(probabilities > 0.5, "pos", "neg")
# Model accuracy
observed.classes <- test.data$diabetes
mean(predicted.classes == observed.classes)
