import os
import pandas as pd
import numpy as np


df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/districts.csv"))


df[['municipality_1', 'municipality_2', 'municipality_3', 'municipality_4']] = df['municipality_info'].str.strip('[]').str.split(',', expand=True)
df[['unemployment_rate_95', 'unemployment_rate_96']] = df['unemployment_rate'].str.strip('[]').str.split(',', expand=True)
df[['committed_crimes_95', 'commited_crimes_96']] = df['commited_crimes'].str.strip('[]').str.split(',', expand=True)

df = df.drop(columns=['unemployment_rate', 'commited_crimes', 'municipality_info'])

df.columns.values[0] = 'district_id'

df.to_csv('district_py.csv', index=False, mode="w")