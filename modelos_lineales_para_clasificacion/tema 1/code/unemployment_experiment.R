library(catdata)
library(tidymodels)


data(unemployment)

summary(unemployment)

#Tabla:
#               <=6 meses   >6 meses  marginales    Odds    Log-Odds
#  Genero: H       403         167     570         2.413     0.881
#          M       238         175     413         1.360     0.307

 
403/570 # [1] 0.7070175
(403/570)/(1-(403/570)) # [1] 2.413174
log((403/570)/(1-(403/570))) # [1] 0.8809427
(238/413)/(1-(238/413)) #[1] 1.36
log((238/413)/(1-(238/413))) #[1] 0.3074847
0.8809427-0.3074847 # [1] 0.573458




#  Level   <=6 meses   >6 meses   marginal
#    1         202         96       298
#    2         307         162      469
#    3         87          66       153
#    4         45          18       63