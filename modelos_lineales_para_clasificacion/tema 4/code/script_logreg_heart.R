library(glmnet)
library(ggplot2)
library(GGally)
library(caret)
# https://hastie.su.domains/StatLearnSparsity/


# Coronary Heart Disease (CHD)
# males in a heart-disease high-risk region of the Western Cape, South Africa.
# Many of the CHD positive men have undergone blood pressure reduction treatment 
# and other programs to reduce their risk factors after their CHD event.
# https://user-images.githubusercontent.com/13688320/67481737-0838a200-f695-11e9-9a84-336518f59c1d.png

heart <- read.csv2("https://hastie.su.domains/ElemStatLearn/datasets/SAheart.data", sep=",")
head(heart)
str(heart)

heart <- na.omit(heart)


heart$tobacco <- as.numeric(heart$tobacco)
heart$ldl <- as.numeric(heart$ldl)
heart$adiposity <- as.numeric(heart$adiposity)
heart$famhist <- as.factor(heart$famhist)
heart$obesity <- as.numeric(heart$obesity)
heart$alcohol <- as.numeric(heart$alcohol)

set.seed(123)
training.samples <- heart$chd %>% 
  createDataPartition(p = 0.8, list = FALSE)
train.data  <- heart[training.samples, ]
test.data <- heart[-training.samples, ]

x <- model.matrix(chd ~ age + famhist + ldl + tobacco + sbp + alcohol + obesity, train.data)[,-1]
y <- ifelse(train.data$chd == 1, 1, 0)

l1mod_1 <- glmnet(x, y, family = "binomial", alpha = 1, lambda = 1.0)

set.seed(123) 
cv.lasso <- cv.glmnet(x, y, alpha = 1, family = "binomial", type.measure = "class", nfolds=10)
predict(cv.lasso, newx = x[1:10,], s = "lambda.min", type = "class")


plot(glmnet(x,y, alpha=1, family="binomial", xvar = "lambda"), label = TRUE)
plot(cv.lasso)
coef(cv.lasso, cv.lasso$lambda.min)

l1mod_1 <- glmnet(x, y, family = "binomial", alpha = 1, lambda = cv.lasso$lambda.min)
coef(l1mod_1)


fit_lasso = glmnet(x, y, family = "binomial", alpha = 1)
plot(fit_lasso, xvar = "lambda", label = TRUE)


