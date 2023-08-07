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

# Define the URL to scrape
url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'

# Page response from the HTTP GET request to the URL; parsing of page content with BeautifulSoup
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
#print(soup)

# Selecting the right 'table' element out of the markup
table = soup.find_all('table')[4]
#print(table)

# Determining all column titles in table
col_titles = table.find_all('th')[:9]
col_table_titles = [title.text.strip().replace('[c]','') for title in col_titles]
#print(col_table_titles)

# Opting to manually create DataFrame column titles
df = pd.DataFrame(columns =['City', 'State', '2022 estimate', '2020 census', 'Change', '2020 land area (sq mi)', '2020 land area (sq km)','2020 population density (sq mi)', '2020 population density (sq km)','Location'])
df

# Extracting all 'table row' data
col_data = table.find_all('tr')
col_data

# Iterating through all table row data to append to DataFrame        
for row in col_data[1:]:
    row_data = row.find_all('td')
    record_data = [data.text.strip() for data in row_data]
    length = len(df)
    df.loc[length] = record_data

# Adjusting DataFrame index to align default index properly
df.index = np.arange(1, len(df) + 1)

# Renaming Index column of DataFrame to associated 'Rank' column from table
df.index.name = '2022 Rank'

# Exporting DataFrame to a CSV file
df.to_csv(r'C:\Users\nbush\python\output_csvs\spy_US_City_Populations.csv', encoding='utf-8')
