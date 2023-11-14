library(tidyverse)

df <- read.csv(("HW-02/data/loans.csv"))

df <- df %>% 
      rename_all(~stringr::str_replace(.,"^X",""))

result_df <- df %>%
  transmute(
    id,
    account_id,
    date,
    amount,
    payments,
    combined = apply(select(., -c(id, account_id, date, amount, payments)), 1,
                    function(row) paste(names(row)[row == "X"], collapse = ",")))

# Separate the 'combined' column into two new columns 'column1' and 'column2' based on the delimiter '_'
result_df <- result_df %>%
  separate(combined, into = c("month", "type_loans"), sep = "_", extra = "merge")


# Write the result DataFrame to a CSV file, overwriting the file if it already exists
write_csv(result_df, "loans_r.csv")
head(df)
resultdf <- df %>%
  gather()