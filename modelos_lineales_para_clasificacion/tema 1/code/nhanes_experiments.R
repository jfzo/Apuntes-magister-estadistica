# analisis de conjunto nhanes
# sacado del package NHANES

#Question: Can we use a person's age and whether they do regular
#     physical activity to predict their self-reported health rating?

#We will analyze the following variables:
#  HealthGen: Self-reported rating of participant's health in general. 
#              Excellent, Vgood, Good, Fair, or Poor.
#
#  Age: Age at time of screening (in years). Participants 80 or older were recorded as 80.
#
#  PhysActive: Participant does moderate to vigorous-intensity sports, fitness or recreational activities


# relevel command: https://stats.oarc.ucla.edu/r/dae/multinomial-logistic-regression/
# buenas slides con ejemplo: https://www2.stat.duke.edu/courses/Fall19/sta210.001/slides/lec-slides/19-multinomial-logistic.pdf

library(dplyr)
library(nnet)
library(knitr)
library(tidymodels)

nhanes_adult <- read.csv("nhanes_adult.csv")


nhanes_adult$HealthGen <- as.factor(nhanes_adult$HealthGen)
nhanes_adult$PhysActive <- as.factor(nhanes_adult$PhysActive)

glimpse(nhanes_adult)


health_m <- multinom(HealthGen ~ Age + PhysActive, data = nhanes_adult)

tidy(health_m, exponentiate = FALSE, conf.int = TRUE) %>% kable(digits = 3, format = "simple")


#calculate predicted probabilities
pred_probs <- as_tibble(predict(health_m, type = "probs")) %>% mutate(obs_num = 1:n())

pred_probs %>% slice(1:10)


#calculate residuals
residuals <- as_tibble(residuals(health_m)) %>% #calculate residu
  setNames(paste('resid.' , names(.), sep = "")) %>% #update column
  mutate(obs_num = 1:n()) #add obs number

      
residuals %>% slice(1:10)


health_m %>% mutate(pred_health = predict(health_m, type = "class")) %>%
  count(HealthGen, pred_health, .drop = FALSE) %>%
  pivot_wider(names_from = pred_health, values_from = n)
