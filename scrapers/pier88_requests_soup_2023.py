# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 20:25:10 2022

@author: nbush
"""

import requests
from bs4 import BeautifulSoup
import unicodecsv as csv

# URL containing all stores' locational information
storeUrl = ['https://www.pier88seafood.com/locations/']
errorUrls = []

# Creates a Session object, mounts headers, and updates the User-Agent
s=requests.Session()
s.mount("http://", requests.adapters.HTTPAdapter(max_retries=2))
s.mount("https://", requests.adapters.HTTPAdapter(max_retries=2))
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'})

# Function sends a GET request in the Session to the provided storeURL
# If the response comes back as intended, the markup is assigned to html with various touch ups on characters
def urlsearch(storeUrl):
    try:
        response = s.get(storeUrl[0])
        
    except requests.exceptions.HTTPError as e:
        print (e.request.url, "*connection failed*")
        response = e.response        
    html = response.text.replace('\n', '').replace('\t', '').replace('@', '').replace('(', '').replace(')', '').replace('\r', '').replace('\\', '').replace('&nbsp','').strip()
    return html

# Opens and writes to output_csv text file (creates one if one does not already exist)
with open("C:/Users/nbush/python/output_csvs/pier_88+seafood_2023.txt", "wb") as w: #remove b
    fields = ["name", "storeno", "address1", "city", "state", "zipcode", "phone"]
    writer = csv.writer(w, encoding='utf-8', delimiter="\t", lineterminator='\n')
    writer.writerow(fields)

# Initializes store number counter
    n=1

# Extracts and parses through page HTML, grabbing the desired 'div' block with a unique 'class' identifier    
    html = urlsearch(storeUrl)
    soup = BeautifulSoup(html, 'xml')
    storeList = soup.find_all('div', attrs={"class":"row single-location wow slideInUp"})
    
# Iterates through each 'div' block found above and extracts and assigns desired text to field variables    
    for store in storeList:
        name = 'Pier 88 Boiling Seafood & Bar'
        storeno = n
        address1 = store.find('p').get_text().split('&nbsp')[0].split(',')[0]
        city = store.find('h3', attrs={'class':'location-title'}).get_text().split(',')[0]
        state = store.find('h3', attrs={'class':'location-title'}).get_text().split(',')[1].strip()
        postalCode = store.find('p').get_text().split(',')[-1]
        zipcode = postalCode[2:]
# Geocoordinates are not available through HTML parsing but can be geocoded through Google
#       latitude = ''
#       longitude = ''
        if store.find('div', attrs={'class':'location-contact'}):
            phone = store.find('div', attrs={'class':'location-contact'}).get_text().strip().replace('Phone:  ','').split('Order')[0].split('Mon')[0].split('Sun')[0]

# Writes the data values to each row with the values corresponding to their various fields
        writer.writerow([name, storeno, address1, city, state, zipcode, phone])
        n += 1

# Verbose confirmation of program completion as well as store count accumulated        
print ("Done", n)










