library(tidyverse)
library(readr)

loandf <- read_csv("loans_r.csv")
disdf <- read_csv("district_py.csv")
accdf <- read_csv("../data/accounts.csv")
linkdf <- read_csv("../data/links.csv")
trandf <- read_csv("../data/transactions.csv")
carddf <- read_csv("../data/cards.csv")

# Rename Columns
accdf <- accdf %>% rename(account_id = id, open_date = date)
linkdf <- linkdf %>% rename(link_id = id)
carddf <- carddf %>% rename(card_id = id) %>% select(-type)
disdf <- disdf %>% rename(district_name = name)


# Initiate dataframe
df <- accdf

# district_name
df <- df %>%
  right_join(disdf %>% select(district_id, district_name), by = "district_id") %>%
  select(-district_id)

# num_customers
temp <- linkdf %>%
  group_by(account_id) %>%
  summarize(num_customers = n())

df <- df %>%
  left_join(temp, by = "account_id")

# credit_cards
tempdf <- linkdf %>%
  select(account_id, link_id) %>%
  right_join(carddf %>% select(link_id, card_id), by = "link_id") %>%
  group_by(account_id) %>%
  summarize(credit_cards = n())

df <- df %>%
  left_join(tempdf, by = "account_id")
  
# loan
tempdf <- loandf %>%
  group_by(account_id) %>%
  summarize(loan = n())
# Merge with the main df and replace NA with 'F' and non-NA with 'T'
df <- df %>%
  left_join(tempdf, by = "account_id") %>%
  mutate(loan = ifelse(is.na(loan), 'F', 'T'))

# loan_amount
df <- df %>%
  left_join(select(loandf, account_id, amount), by = "account_id") %>%
  mutate(loan_amount = ifelse(is.na(amount), NA, amount)) %>%
  select(-amount)

# loan_payment
df <- df %>%
  left_join(select(loandf, account_id, payments), by = "account_id") %>%
  mutate(loan_payments = ifelse(is.na(payments), NA, payments)) %>%
  select(-payments)

# loan_term
df <- df %>%
  left_join(select(loandf, account_id, month), by = "account_id") %>%
  mutate(loan_term = ifelse(is.na(month), NA, month)) %>%
  select(-month)

# loan_status
df <- df %>%
  left_join(select(loandf, account_id, type_loans), by = "account_id") %>%
  mutate(
    loan_status = case_when(
      is.na(type_loans) ~ NA_character_,
      type_loans %in% c("A", "B") ~ "expired",
      TRUE ~ "current"
    )
  ) %>%
  select(-type_loans)

# loan_default
df <- df %>%
  left_join(select(loandf, account_id, type_loans), by = "account_id") %>%
  mutate(
    loan_default = case_when(
      is.na(type_loans) ~ NA_character_,
      type_loans == "B" ~ "T",
      TRUE ~ "F"
    )
  ) %>%
  select(-type_loans)

# max_withdrawal, min_withdrawal, cc_payments, max_balance, min_balance
df <- df %>%
  left_join(trandf %>% filter(type == 'debit') %>% group_by(account_id) %>% summarise(max_withdrawal = max(amount), min_withdrawal = min(amount)), by = "account_id") %>%
  left_join(trandf %>% group_by(account_id) %>% summarise(max_balance = max(balance), min_balance = min(balance)), by = "account_id")

# cc_payments
cc_payments <- trandf %>%
  filter(type == "debit", method == "credit card") %>%
  group_by(account_id) %>%
  summarize(cc_payments = n()) %>%
  ungroup()
df <- df %>%
  left_join(cc_payments, by = "account_id")

# Rearrange columns
columns_order <- c('account_id', 'district_name', 'open_date','statement_frequency', 'num_customers', 'credit_cards', 'loan', 'loan_amount', 'loan_payments', 'loan_term', 'loan_status', 'loan_default','max_withdrawal','min_withdrawal','cc_payments','max_balance','min_balance')
df <- df %>% select(all_of(columns_order))

write_csv(df, "analytical_r.csv")