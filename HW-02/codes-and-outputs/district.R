library(tidyr)
library(readr)
library(tidyverse)


# Read the CSV file
df <- read_csv('HW-02/data/districts.csv')

# Split 'municipality_info' column into four columns
df <- df %>%
  separate(municipality_info, 
           into = c("municipality_1", "municipality_2", "municipality_3", "municipality_4"), 
           sep = ",", 
           remove = TRUE, 
           convert = TRUE) %>%
  mutate(across(starts_with("municipality_"), ~str_remove_all(., "\\[|\\]")))

# Split 'unemployment_rate' column into two columns
df <- df %>%
  separate(unemployment_rate, 
           into = c("unemployment_rate_95", "unemployment_rate_96"), 
           sep = ",", 
           remove = TRUE, 
           convert = TRUE) %>%
  mutate(across(starts_with("unemployment_rate_"), ~str_remove_all(., "\\[|\\]")))

# Split 'commited_crimes' column into two columns
df <- df %>%
  separate(commited_crimes, 
           into = c("committed_crimes_95", "commited_crimes_96"), 
           sep = ",", 
           remove = TRUE, 
           convert = TRUE) %>%
  mutate(across(starts_with("committed_crimes_"), ~str_remove_all(., "\\[|\\]")))


last_col_name <- names(df)[ncol(df)]
df <- df %>%
  mutate(!!last_col_name := str_remove(!!sym(last_col_name), "\\]$"))

df <- df %>% rename(district_id = !!names(df)[1])

# Write to a new CSV file
write.csv(df, "district_R.csv", row.names = FALSE)
