import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import csv
from csv import writer
from notify_run import Notify
import tqdm
import functools
notify = Notify()
print(notify.register())

#Go on and add your url of interest for the scraping...
#Make sure that the url reflects your desired filters for housing
#For me - Rent max: 1500 Euro, 50+ m2, 3+ rooms, 2+ bedrooms
pararius = 'https://www.pararius.com/apartments/utrecht/0-1750/3-rooms/2-bedrooms/50m2/page-{}?ac=1'

#Scrape through pararius to find the information
for x in range(0,6,1):
    names = pararius.format(x)
    r = requests.get(names)
    soup = BeautifulSoup(r.text,'html.parser')
    for item in soup.find_all('li',attrs={'class':'search-list__item search-list__item--listing'}):
            weblink, address, rent, size,agent,description =([], )*6
            try:
                agent.append(np.nan)
            except:
                agent.append(np.nan)
            try:
                address.append(item.find('div' ,attrs={'class':'listing-search-item__location'}).text)
            except:
                address.append(np.nan)
            try:
                rent.append(item.find('span', attrs={'class':'listing-search-item__price'}).text)
            except:
                rent.append(np.nan)
            try:
                size.append(item.find('span', attrs={'class':'illustrated-features__description'}).text)
            except:
                size.append(np.nan)
            try:
                weblink.append(item.find('a',attrs={'class':'listing-search-item__link listing-search-item__link--title'}))
            except:
                weblink.append(np.nan)
            with open('pararius_listing.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(weblink)
                f_object.close()

df = pd.read_csv('pararius_listing.csv',names=['nothing','address','price','size','link']) 

global_links = []
for element in df['link']:
    fixed_link = []
    link = ''
    checker_1 = False
    checker_2 = False
    for character in element:
        if character == "/":
            checker_1 == True
        if checker_1 and character == '>':
            checker_2 = True
        if character == "/":
            checker_1 = True
        if checker_1 == True:
            fixed_link.append(character)
        if checker_1 and checker_2:
            break
        else:
            continue
    link = functools.reduce(lambda a,b : a+b, fixed_link)
    link = link[:-1]
    global_links.append(link)
df['real_link'] = global_links
df = df.drop(columns='link')
df = df.drop_duplicates()
df.to_csv('listings.csv')
