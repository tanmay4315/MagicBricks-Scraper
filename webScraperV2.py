import os
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
import json
import pandas as pd
import re
import csv


chromedriver = "C:\\software\\chromedriver_win32\\chromedriver.exe"
chromedriver = os.path.expanduser(chromedriver)
print('chromedriver path: {}'.format(chromedriver))
sys.path.append(chromedriver)
driver = webdriver.Chrome(chromedriver,120)
def get_house_links( driver):
    house_links=[]
    '''
    cities=['Gurgaon','Noida','Ghaziabad','Greater-Noida','Bangalore','Mumbai','Pune','Hyderabad','Kolkata','Chennai']
    '''
    cities=['Chennai']
    for city in cities:
        for i in range(1,500):
            driver.get("https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&page="+str(i)+"&cityName="+str(city))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            get_data(soup)
def house_description(url):
    driver.get(url)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    divpvalue=soup.find_all('div',class_='p_value')
    divtitle=soup.find_all('div',class_='p_title')
    dimension=soup.find_all('span',class_='ftrt bedroomVal')
    Puja_room=""
    super_area=""
    carpet_area=""
    status=""
    floor=""
    facing=""
    balconies=""
    address=""
    age_construct=""
    possession=""
    for j in range(0,len(divtitle)):
        if divtitle[j].get_text()=="Puja Room":
            Puja_room=divpvalue[j].get_text()
        if divtitle[j].get_text()=='Super area':
            super_area=re.findall('[0-9]+',divpvalue[j].get_text())[0]
        if divtitle[j].get_text()=='Carpet area':
            carpet_area=re.findall('[0-9]+',divpvalue[j].get_text())[0]
        if divtitle[j].get_text()=='Status':
            status=divpvalue[j].get_text()
        if divtitle[j].get_text()=='Floor':
            floor=(divpvalue[j].get_text()).replace('&nbsp;','');
            floor=floor.replace('\n','')
        if divtitle[j].get_text()=='Facing':
            facing=divpvalue[j].get_text()
        if divtitle[j].get_text()=='Balconies':
            balconies=divpvalue[j].get_text()
        if divtitle[j].get_text()=='Address':
            address=divpvalue[j].get_text()
            address=address.replace('\n','')
        if divtitle[j].get_text()=='Age of Construction':
            age_construct=divpvalue[j].get_text()
        if divtitle[j].get_text()=='Possession by':
            possession=divpvalue[j].get_text()
        var['Yr_built']=age_construct
        var['Sqft_Super_Carpet']=super_area
        var['Sqft_Carpet']=carpet_area
        var['View']=facing
        var['Condition']=status
        for k in range(0,len(dimension)):
            l,b=((dimension[k].get_text()).replace('ft','').split('X'))
            var['Sqft_bed'+str(k+1)]=float(l.strip())*float(b.strip())
def get_data(soup):
    prop=soup.find_all('div',class_='m-srp-card SRCard')
    #print(prop)
    for i in prop:
        global var
        var={}
        url=""
        price=""
        longitude=""
        latitude=""
        numberOfRooms=""
        bathroom=""
        bedroom=""
        floorSize=""
        floorno=""
        furnshingstatus=""
        meta=i.find_all('meta')
        for m in meta:
            if m['itemprop']=='name':
                name=m['content']
            if m['itemprop']=='url':
                url=str('https://www.magicbricks.com'+m['content'])
            if m['itemprop']=='longitude':
                longitude=m['content']
            if m['itemprop']=='latitude':
                latitude=m['content']
            if m['itemprop']=='numberOfRooms':
                numberOfRooms=m['content']
        s=i.find('span',class_='hidden')
        bathroom=s['data-bathroom']
        bedroom=s['data-bedroom']
        floorno=s['data-floorno']   
        price=s['data-price']
        completionscore=s['data-completionscore']
        id_=s['id']
        ag=soup.find('span',id=id_)
        priceInWord=ag['data-priced']
        cityName=ag['data-cityname']
        var['price']=price
        var['Bedrooms']=bedroom
        var['Bathrooms']=bathroom
        var['Sqft_Super_Carpet']=""
        var['Sqft_Carpet']=""
        var['floorno']=floorno
        var['View']=''
        var['Condition']=""
        var['Lat']=latitude
        var['Long']=longitude
        house_description(url)
        csv_file="Chennai.json"
        with open(csv_file,'a+',encoding='utf-8') as file:
            file.write(json.dumps(var, ensure_ascii=False) + "\n")

get_house_links(driver)
