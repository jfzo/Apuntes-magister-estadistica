library(tidyverse)
library(ggplot2)

heart_disease_dataset <- read.csv(file = "processed.cleveland.data", header = F)

names <- c("Age",
           "Sex",
           "Chest_Pain_Type",
           "Resting_Blood_Pressure",
           "Serum_Cholesterol",
           "Fasting_Blood_Sugar",
           "Resting_ECG",
           "Max_Heart_Rate_Achieved",
           "Exercise_Induced_Angina",
           "ST_Depression_Exercise",
           "Peak_Exercise_ST_Segment",
           "Num_Major_Vessels_Flouro",
           "Thalassemia",
           "Diagnosis_Heart_Disease")
#Apply column names to the dataframe
colnames(heart_disease_dataset) <- names

#Determine the number of values in each level of dependent variable
heart_disease_dataset %>% 
  drop_na() %>%
  group_by(Diagnosis_Heart_Disease) %>%
  count() %>% 
  ungroup() %>%
  kable(align = rep("c", 2)) %>% kable_styling("full_width" = F)


heart_dataset_clean_tbl <- heart_disease_dataset %>% 
  drop_na() %>%
  mutate_at(c("Resting_ECG", 
              "Fasting_Blood_Sugar", 
              "Sex", 
              "Diagnosis_Heart_Disease", 
              "Exercise_Induced_Angina",
              "Peak_Exercise_ST_Segment", 
              "Chest_Pain_Type"), as_factor) %>%
  mutate(Num_Major_Vessels_Flouro = as.numeric(Num_Major_Vessels_Flouro)) %>%
  mutate(Diagnosis_Heart_Disease = fct_lump(Diagnosis_Heart_Disease, other_level = "1")) 




ggplot(heart_dataset_clean_tbl, aes(x = Age, y = Diagnosis_Heart_Disease)) +  
  geom_point(alpha = 0.3) + xlab("Age") + ylab("Heart disease")+theme_light()
