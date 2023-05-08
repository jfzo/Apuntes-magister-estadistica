library(catdata)
library(tidymodels)


data(vaso)

vaso$vaso <- as.factor(vaso$vaso)
mod_logit <- glm(vaso ~ vol + rate, data=vaso, family="binomial")
summary(mod_logit)


vaso$vaso <- as.factor(vaso$vaso)
mod_logit <- glm(vaso ~ vol + rate, data=vaso, family = binomial(link = logit))
summary(mod_logit)


# version log-trans
vaso$vaso <- as.factor(vaso$vaso)
mod_logit <- glm(vaso ~ log(vol) + log(rate), data=vaso, family="binomial")
summary(mod_logit)


# alternativamente con tidymodels
log_m <- logistic_reg()
lm_fit <- fit(log_m, vaso ~ vol + rate, data = vaso)
tidy(lm_fit)