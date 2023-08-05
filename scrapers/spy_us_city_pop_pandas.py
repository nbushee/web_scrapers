# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 10:10:26 2023

@author: nbush
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import string

url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
#print(soup)

table = soup.find_all('table')[4]
#print(table)

col_titles = table.find_all('th')[:9]
col_table_titles = [title.text.strip().replace('[c]','') for title in col_titles]
#print(col_table_titles)

df = pd.DataFrame(columns =['City', 'State', '2022 estimate', '2020 census', 'Change', '2020 land area (sq mi)', '2020 land area (sq km)','2020 population density (sq mi)', '2020 population density (sq km)','Location'])
df

col_data = table.find_all('tr')
col_data

#reference_list = ['[a]','[b]','[c]','[d]','[e]','[f]','[g]','[h]','[i]','[j]','[k]','[l]','[m]',
                  #'[n]','[o]','[p]','[q]','[r]','[s]','[t]','[u]','[v]','[w]','[x]','[y]','[z]',
                  #'[aa]']


        
for row in col_data[1:]:
    row_data = row.find_all('td')
    record_data = [data.text.strip() for data in row_data]
    length = len(df)
    df.loc[length] = record_data
df.index = np.arange(1, len(df) + 1)
df.index.name = '2022 Rank'

df.to_csv(r'C:\Users\nbush\python\output_csvs\spy_US_City_Populations.csv', encoding='utf-8')
