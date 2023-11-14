import os
import pandas as pd
import numpy as np


df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/loans.csv"))

df.rename(columns={'id': 'loans_id'}, inplace=True)

print(df)

print(df.replace('-', np.nan, inplace=True))


for i in df[['24_A', '12_B',
       '12_A', '60_D', '48_C', '36_D', '36_C', '12_C', '48_A', '24_C', '60_C',
       '24_B', '48_D', '24_D', '48_B', '36_A', '36_B', '60_B', '12_D', '60_A']].columns:
    df[i].replace('X',i,inplace=True)


df['Values'] = df[df.columns[5:]].apply(
    lambda x: ','.join(x.dropna().astype(str)),
    axis=1
)

df.drop(['24_A', '12_B',
       '12_A', '60_D', '48_C', '36_D', '36_C', '12_C', '48_A', '24_C', '60_C',
       '24_B', '48_D', '24_D', '48_B', '36_A', '36_B', '60_B', '12_D', '60_A'], axis=1, inplace= True)

df[['number_of_months', 'current_loan_status']] = df['Values'].str.split('_', expand=True)

df.drop(['Values'], axis = 1, inplace= True)

print(df)

df.to_csv(os.path.join(os.path.dirname(__file__), 'loans_py.csv'), index=False)