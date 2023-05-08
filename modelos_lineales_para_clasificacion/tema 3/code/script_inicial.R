library(VGAM)

Polviews <- read.table("http://www.stat.ufl.edu/~aa/cat/data/Polviews.dat", header = TRUE)

fit <- vglm(cbind(y1,y2,y3,y4,y5) ~ party + gender, family=cumulative(parallel=TRUE), data=Polviews)
summary(fit) # # "parallel=TRUE" imposes proportional odds structure


#attach(Polviews)
data.frame(Polviews$gender, Polviews$party, fitted(fit)) # y1 = very lib., y5 = very conserv.


fit <- vglm(cbind(y1,y2,y3,y4,y5) ~ party + gender, family=cumulative(parallel=FALSE), data=Polviews)
summary(fit) # # without proportional odds structure

# Viewing these helps us to understand the effects of the explanatory variables. For each
# political party affiliation, the estimated distributions are very similar for females and males.
# The most common response is slightly liberal for Democrats, who are very likely to be in
# category 3 or below, and slightly conservative for Republicans, who are very likely to be in
# category 4 or 5


# 2006 US General Social Survey 
# opinion ratings, a variable indicating the fundamentalism / liberalism of the respondents’ religious
# opiniones en 4 niveles más una variable indicando creencias religiosas.
#
# we investigate to what extent religious belief predicts
# Deseamos investigar en que medida las creencias religiosas permiten predecir opiniones respecto
# de financiar investigación en células madre.
# La opinión respecto de financiar la investigación es la respuesta (var dependiente).
# Importante mencionar: 
#     Se desconoce separación psicológica entre categorías 
#     Tampoco son iguales estas separaciones entre participantes de la encuesta.
# (1), “probably not fund” (2), “probably fund” (3), and “definitely fund” (4)


stem_research <- read.csv2('stem cell research survey.csv')
stem_research$creencia <- as.factor(stem_research$creencia)
# stem_research$creencia <- relevel(stem_research$creencia, ref="moderado") # permite cambiar referencia

fit_stem <- vglm(cbind(y1,y2,y3,y4) ~ creencia, family=cumulative(parallel=TRUE), data=stem_research, )
summary(fit_stem)

# siendo "moderado" la referencia ...
#   b1 representa el contraste en entre "moderado" y "fundamentalista" y 
#   b2 el contraste entre "moderado" y "liberal"

data.frame(stem_research$creencia, fitted(fit_stem))

# ejemplo usando el modelo ajustado.

ESMODERADO <- 0
ESFUND <- 1
ESLIBERAL <- 0
eta <- (0.41693*ESFUND -0.56096*ESLIBERAL)
P_prob_fnr <- pnorm(0.93867-eta, 0, 1) - pnorm(-1.04048-eta, 0, 1)


##### Knee

kneedata <- read.csv2(file = "dolor_despues_tratamiento_rodilla.csv", header = TRUE)
kneedata$grupo <- as.factor(kneedata$grupo)

kneefit <- vglm(
  cbind(sin_dolor, dolor_leve, dolor_moderado, dolor_intenso, dolor_severo) ~ grupo, 
  family=cumulative(parallel=TRUE), data=kneedata)
summary(fit) # # "parallel=TRUE" imposes proportional odds structure



### KNEE BIEN HECHO
library(catdata)
data(knee)

# R4(no pain = 1, severe pain = 5)
# Therapy(placebo = 1, treatment = 2)
# Gender (male = 0, female = 1)

chisq.test(knee$Th,knee$R4) # muestra asociación entre terapia y nivel dolor lueego de 10 dias
# p-valor de 0.0011 muestra efecto significativo del tratamiento.

# Qué tanto será el efecto del tratamiento?
knee$R4 <- as.ordered(knee$R4)
knee$Th <- as.factor(knee$Th)
knee$Sex <- as.factor(knee$Sex)

kneefit <- vglm(
  R4 ~ Th, 
  family=cumulative(parallel=TRUE), data=knee)
summary(kneefit) # # "parallel=TRUE" imposes proportional odds structure
# exp(...) es 2.442 --> para cualquier dicotomizacion de las categorias, los odds
# ratios acumulados resultantes de comparar el grupo de tratamiento vs el de placebo es 2.442.
# Esto indica que las odds para categorias de menor dolor en comparacion con cats. de mayor dolor
# ... son más altas en el grupo de tratamiento.


# version tabla
knee$Therapy <- ifelse(knee$Th == "1","Placebo","Treatment")
cont_knee <- table(knee$Therapy, knee$R4)
colnames(cont_knee) <- paste("L",colnames(cont_knee),sep="")
cont_knee_df <- as.data.frame.matrix(cont_knee)
cont_knee_df <- cbind(Group = rownames(cont_knee_df), cont_knee_df)
rownames(cont_knee_df) <- 1:nrow(cont_knee_df)

kneefit_tb <- vglm(
  cbind(L1,L2,L3,L4,L5) ~ Group, 
  family=cumulative(parallel=TRUE), data=cont_knee_df)
summary(kneefit_tb) # # "parallel=TRUE" imposes proportional odds structure

#
kneefit2 <- vglm(
  R4 ~ Th + Sex + Age, 
  family=cumulative(parallel=TRUE), data=knee)
summary(kneefit2) # # "parallel=TRUE" imposes proportional odds structure

# usando el package MASS
# ver https://rpubs.com/shreejit16/625642
install.packages("effects")
library(MASS)
library(effects)
library(ggplot2)

polr1 <- polr(R4 ~ Th, method="logistic", data = knee)
summary(polr1)
plot(Effect("Th", polr1))
levels(knee$Th)

polr2 <- polr(R4 ~ Th  + Age, method="logistic", data = knee)
summary(polr2)
plot(Effect("Th", polr2))

test.data <- expand.grid(Th=c("1","2"), Sex=c("0","1"), Age=c(20,25,30))
predicted <- predict(polr2, test.data,type="probs")

