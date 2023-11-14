import pandas as pd
import numpy as np
import os

loandf = pd.read_csv("loans_py.csv")
disdf = pd.read_csv("district_py.csv")
accdf = pd.read_csv("../data/accounts.csv")
linkdf = pd.read_csv("../data/links.csv")
trandf = pd.read_csv("../data/transactions.csv")
carddf = pd.read_csv("../data/cards.csv")

accdf = accdf.rename(columns={'id': 'account_id'})
accdf = accdf.rename(columns={'date': 'open_date'})
linkdf = linkdf.rename(columns={'id': 'link_id'})
carddf = carddf.rename(columns={'id': 'card_id'})
carddf.drop('type', axis=1, inplace=True)
disdf = disdf.rename(columns={'name': 'district_name'})
loandf = loandf.rename(columns={'id': 'loan_id'})

print(loandf.head())
# Initiate dataframe
df = accdf.copy()

# district_name
df = pd.merge(df, disdf[["district_id","district_name"]], how="inner", on="district_id")
df.drop(columns = ['district_id'], inplace=True)

# num_customers
df = pd.merge(df, linkdf, how="outer", on='account_id')
temp = linkdf.groupby(['account_id'])['account_id'].count()
temp = temp.to_frame()
temp.index.name = ''
temp.rename(columns = {'account_id': 'num_customers'}, inplace = True)
temp.index.name = "account_id"
df = pd.merge(df, temp, how="inner", on="account_id")

print(df.head())
# credit_cards
tempdf = pd.merge(linkdf[['account_id', 'link_id']], carddf[['link_id','card_id']], how="outer", on="link_id")
tempdf = tempdf.groupby(['account_id']).count().reset_index()
df = pd.merge(df, tempdf[['account_id', 'card_id']], how="inner", on="account_id")
df.rename(columns = {'card_id': 'credit_cards'}, inplace = True)
df.drop(columns = ['link_id','client_id'], inplace=True)

# loan
tempdf = loandf.groupby(['account_id'])['account_id'].count().to_frame()
tempdf.index.name = ''
tempdf.rename(columns = {'account_id': 'loan'}, inplace = True)
tempdf.index.name = "account_id"

df = pd.merge(df, tempdf, how="outer", on="account_id")
df['loan'] = df['loan'].apply(lambda x: 'T' if pd.notna(x) else 'F')

#loan_amount
df = pd.merge(df, loandf[['account_id','amount']], how="outer", on="account_id")
df['amount'] = df['amount'].apply(lambda x: x if pd.notna(x) else np.nan)
df = df.rename(columns={'amount': 'loan_amount'})

# loan_payments
df = pd.merge(df, loandf[['account_id','payments']], how="outer", on="account_id")
df['payments'] = df['payments'].apply(lambda x: x if pd.notna(x) else np.nan)
df = df.rename(columns={'payments': 'loan_payments'})

print(df.head())
print(loandf)

# loan_term
df = pd.merge(df, loandf[['account_id','number_of_months']], how="outer", on="account_id")
df['number_of_months'] = df['number_of_months'].apply(lambda x: x if pd.notna(x) else np.nan)
df = df.rename(columns={'number_of_months': 'loan_term'})

# loan_status
df = pd.merge(df, loandf[['account_id','current_loan_status']], how="outer", on="account_id")
df['current_loan_status'] = df['current_loan_status'].apply(lambda x: np.nan if pd.isna(x) else ("expired" if x =='A' or x == 'B' else "current"))
df = df.rename(columns={'current_loan_status': 'loan_status'})

# loan_default
df.drop(columns=['type'], inplace=True)
temp = loandf[['account_id','current_loan_status']].rename(columns={'current_loan_status':'type'})
df = pd.merge(df, temp, how="outer", on="account_id")
print(df.tail())
print(temp.head())

df['type'] = df['type'].apply(lambda x: x if pd.notna(x) else np.nan)
df['type'] = df['type'].apply(lambda x: np.nan if pd.isna(x) else ("T" if x in ["B"] else "F"))
df = df.rename(columns={'type': 'loan_default'})

# max_withdrawal
temp = trandf[trandf['type']=='debit'].groupby('account_id')['amount'].max().to_frame()
temp.index.name = ''
temp.rename(columns = {'amount': 'max_withdrawal'}, inplace = True)
temp.index.name = "account_id"
df = pd.merge(df, temp, how="outer", on="account_id")

# min_withdrawal
temp = trandf[trandf['type']=='debit'].groupby('account_id')['amount'].min().to_frame()
temp.index.name = ''
temp.rename(columns = {'amount': 'min_withdrawal'}, inplace = True)
temp.index.name = "account_id"

df = pd.merge(df, temp, how="outer", on="account_id")

# cc_payments
temp = trandf[(trandf['type']=='debit') & (trandf['method']=='credit card')].groupby('account_id')['date'].count()
temp = temp.to_frame()
temp.index.name = ''
temp.rename(columns = {'date': 'cc_payments'}, inplace = True)
temp.index.name = "account_id"

df = pd.merge(df, temp, how="outer", on="account_id")

# max_balance
temp = trandf.groupby('account_id')['balance'].max().to_frame()
temp.index.name = ''
temp.rename(columns = {'balance': 'max_balance'}, inplace = True)
temp.index.name = "account_id"

df = pd.merge(df, temp, how="outer", on="account_id")

# min_balance
temp = trandf.groupby('account_id')['balance'].min().to_frame()
temp.index.name = ''
temp.rename(columns = {'balance': 'min_balance'}, inplace = True)
temp.index.name = "account_id"

df = pd.merge(df, temp, how="outer", on="account_id")

columns_order = ['account_id', 'district_name', 'open_date','statement_frequency', 'num_customers', 'credit_cards', 'loan', 'loan_amount', 'loan_payments', 'loan_term', 'loan_status', 'loan_default','max_withdrawal','min_withdrawal','cc_payments','max_balance','min_balance']
df = df[columns_order]

df.to_csv('analytical_py.csv')