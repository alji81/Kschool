#!/usr/bin/env python
# coding: utf-8

# # 1. Import packs and libraries

# In[1]:


#Install all packs needed to download data from Pollutant website Catalonia's government (sodapy) and web scrapping from meteo web


# In[2]:


#Import libraries required
import os
import pandas as pd
import numpy as np
from sodapy import Socrata
from datetime import datetime
from datetime import timedelta
import pickle 
import streamlit as st 
import matplotlib.pyplot as plt
from PIL import Image
import requests
from bs4 import BeautifulSoup
import re
import operator


# #### NOTE: I tried to use web scrapping in order to get data, but I attempt in 2 different web sites,and I highlighted that every few hours, position of data change location, doing not ppossible to fix data.

# # 2. Download Pollutant DATA from web page by downloading dataset

# In[3]:


#Current day
now = datetime.now()

#In order to get enough data, if time is prior to midday, data is got from prior day, if not so, data is got from current day. 
#The aim of this is to get minimum 12 hours dataset.

if now.strftime('%H')>='12':
    fecha = now
else:
    fecha = now - timedelta(days=1)
    
fecha=fecha.strftime('%Y-%m-%d')


# In[4]:


#Download data info from web. It is not needed token because we will download data once.
socrata_domain = "analisi.transparenciacatalunya.cat"
socrata_dataset_identifier = "tasf-thgu"
#socrata_token = os.environ.get("None") --> not needed, but just in case, here we have the sentence to include it.

client = Socrata(socrata_domain, None)
#print(
#    "Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(
#        **client.__dict__
#    )
#)

metadata = client.get_metadata(socrata_dataset_identifier)
#[x["name"] for x in metadata["columns"]]

results = client.get(socrata_dataset_identifier,
                    limit=100000, 
                    nom_estacio="Tarragona (Bonavista)",
                    data=fecha)    
    
dfA = pd.DataFrame.from_dict(results);


# In[5]:


#Let's select features interested
dfB=dfA.drop(['codi_eoi', 'nom_estacio', 'data', 'magnitud', 'unitats',
       'tipus_estacio', 'area_urbana', 'codi_ine', 'municipi', 'codi_comarca',
       'nom_comarca', 'altitud', 'latitud',
       'longitud', 'geocoded_column'],axis=1)
#Let's create an average feature 
ave = dfB.loc[: , "h01":]
ave = ave.astype(float)
dfB['0'] = ave.mean(axis=1)
# Simplified dataframe 
dfC = dfB[['contaminant','0']]
#Crete a pivot table to adecuate the format
tableA = dfC.pivot_table(columns='contaminant', aggfunc=np.sum)
#Let's select interested pollutant features 
tableB=tableA[['NO2','PM2.5','PM10']]


# # 3. Download Meteorological DATA from web page by downloading dataset

# In[6]:


socrata_domain = "analisi.transparenciacatalunya.cat"
socrata_dataset_identifier = "nzvn-apee"
#socrata_token = os.environ.get("None")

client = Socrata(socrata_domain, None)
print(
    "Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(
        **client.__dict__
    )
)

#metadata = client.get_metadata(socrata_dataset_identifier)
#[x["name"] for x in metadata["columns"]]

results = client.get(socrata_dataset_identifier,
                    limit=775,
                    codi_estacio="XE",
                    order='data_lectura DESC')
                     
df = pd.DataFrame.from_dict(results)


# In[7]:


#Data object should be modified to datetime, to later on be merged with Pollutant data.
df['data_lectura'] = pd.to_datetime(df['data_lectura'], dayfirst=True)
#Let's reduce dataframe to columns desired: date, feature and value
df1=df[['data_lectura','codi_variable','valor_lectura']]
#Let's generate a pivot table to allocate meteorological features in columns as features and date samples as rows
table = df1.pivot_table(index='data_lectura', columns='codi_variable', aggfunc=np.sum,)
#Reduce a unique column row
table = pd.DataFrame(table.to_records())
#Date is sorted by ascending value
table = table.sort_values(['data_lectura'],ascending=True)
#Relabel columns
table.columns = ['data_lectura','1','2','3','30','31','32','33','34','35','36','40','42','44','50','51','72']
#Features values should be transformed to float to be interpreted mathematically
table[['1','2','3','30','31','32','33','34','35','36','40','42','44','50','51','72']] = table[['1','2','3','30','31','32','33','34','35','36','40','42','44','50','51','72']].astype(float)
#Table is grouped by daily measures in order to be consistency with Pollutant dataset. It means, daily samples
table1 = table.groupby(table['data_lectura'].dt.month).mean()
table2 = table1.reset_index()


# In[8]:


#Features above were downloaded as label numbered, so let's rename the features with Features label accordingly.
socrata_domain = "analisi.transparenciacatalunya.cat"
socrata_dataset_identifier = "4fb2-n3yi"
#socrata_token = os.environ.get("None")

client = Socrata(socrata_domain, None)
print(
    "Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(
        **client.__dict__
    )
)

results = client.get(socrata_dataset_identifier)    
v = pd.DataFrame.from_dict(results)


# In[9]:


#Dataframe creation
v1 = pd.DataFrame(v.to_records())
#Let's create a Dictionary to relabel columns
dict = pd.Series(v1.codi_variable.values,index=v1.nom_variable).to_dict()
#Let's sort the dictionary
sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=False)
#Rename columns with feature labels
table2.columns = ['data_lectura','Pressió atmosfèrica màxima',
 'Pressió atmosfèrica mínima',
 'Humitat relativa màxima',
 'Velocitat del vent a 10 m (esc.)',
 'Direcció de vent 10 m (m. 1)',
 'Temperatura',
 'Humitat relativa',
 'Pressió atmosfèrica',
 'Precipitació',
 'Irradiància solar global',
 'Temperatura màxima',
 'Temperatura mínima',
 'Humitat relativa mínima',
 'Ratxa màxima del vent a 10 m',
 'Direcció de la ratxa màxima del vent a 10 m',
 'Precipitació màxima en 1 minut']
table3 = table2[['Velocitat del vent a 10 m (esc.)', 'Temperatura', 'Pressió atmosfèrica',]]


# # 4. Join datasets

# In[10]:


table3.insert(0,"orden",['0'],True)
tableB.insert(0,"orden",['0'],True)
merged = pd.merge(left=tableB, right=table3, how='left', left_on='orden', right_on='orden')
porfin=merged.drop(['orden'],axis=1)


# # 5. Import Model

# In[11]:


pickle_in = open('FrontEnd_docs_related/aplication.pkl', 'rb') 
pipe_svc = pickle.load(pickle_in) 


# # 6. Define App

# In[12]:


#Let's create a FrontEnd where the user can have an overview about Evolution of the 4 main Pollutants from period 2010-2020, and Predict if PM2.5 system Alert and meausures involved will be activated tomorrow. 
st.title('Pollutant Evolution and Preventive Alert System')
st.write('This web app allows you to know Pollutant Evolution from 2010 to 2020 and PM2.5 24h prediction as Preventive Sytem Alert')



st.header('Pollutant Evolution')
st.write('This section allows you to know Pollutant Evolution from 2010 to 2020 from pollutant selected')
st.text('Please, select Pollutant desired in side to see its Evolution graph during last 10 years')

st.sidebar.title("Pollutant")
select = st.sidebar.selectbox('Select Pollutant',(['PM2.5'],['PM10'],['NO2'],['NOx'],['NO'],['H2S'],['SO2']))

                              
if select == ['PM2.5']:
        st.image(Image.open('FrontEnd_docs_related/PM2.5.jpg'))
        st.text('PM2.5 Evolution: Downward trend in average annual values obtained for pollutant PM2,5 during last years.') 
        st.text('The worst results were registered in 2015')
elif select == ['PM10']:
        st.image(Image.open('FrontEnd_docs_related/PM10.jpg'))
        st.text('PM10 Evolution: Stable results with an upward trend in average annual values obtained for pollutant PM10 in recent years.')
        st.text('The improvement in 2020 was due to the influence of the Covid-19 pandemic')
elif select == ['H2S']:
        st.image(Image.open('FrontEnd_docs_related/H2S.jpg'))
        st.text('H2S Evolution: Downward trend in average annual values obtained for pollutant H2S during last years.')
        st.text('The worst results were registered in 2015')
elif select == ['NO']:
        st.image(Image.open('FrontEnd_docs_related/NO.jpg'))
        st.text('NO Evolution: Stable results got for pollutant NO during last years')
elif select == ['NOx']:
        st.image(Image.open('FrontEnd_docs_related/NOx.jpg'))
        st.text('NOx Evolution: Stable results got for pollutant NOx during last years')
elif select == ['SO2']:
        st.image(Image.open('FrontEnd_docs_related/SO2.jpg'))
        st.text('SO2 Evolution: Stable results with an upward trend in average annual values obtained for pollutant SO2 in recent years.')
        st.text('The improvement in 2020 was due to the influence of the Covid-19 pandemic')
else:
        st.image(Image.open('FrontEnd_docs_related/NO2.jpg'))
        st.text('NO2 Evolution: Stable results got for pollutant NO2 during last years')

    
        

st.header('Preventive System PM2.5 Alert')
st.write('This section allows you to predict PM2.5 24h forecast by automatically data requiered.')
st.text('Please, select data impute method to predict PM2.5 24h forecast')

st.sidebar.title("Predict impute method")
select1 = st.sidebar.selectbox('Select method',(['Automatic'],['Manual']))

st.text('Preventive Sytem Alert is Activated when:')
st.text('     - average PM2,5 today feature exceeed threshold 25 micrograms/m3')
st.text('     - prediction at 24h does not improve the results')



if select1 == ['Manual']:
    PM25 =  st.number_input("PM2.5 (micrograms/m3):")
    NO2 = st.number_input("NO2 (micrograms/m3):")
    PM10 =  st.number_input("PM10 (micrograms/m3):")
    Pressio_atmosferica = st.number_input("Atmospheric pressure (hPa):")
    Temperatura = st.number_input("Temperature (ºC):")
    Velocitat = st.number_input("Wind spped (m/s):")
        
    features = {'PM2.5': PM25, 'PM10': PM10,'NO2':NO2,'Pressió atmosfèrica': Pressio_atmosferica,'Temperatura': Temperatura,'Velocitat del vent a 10 m (esc.)': Velocitat}
    X_user  = pd.DataFrame([features])
        
    submit =st.button('Predict')
        
    if submit:   
        
        prediction = pipe_svc.predict(X_user)
            
        if prediction == 1 and PM25>=20:
            st.write('Alert activated')
            st.text('Countermeasures to be followed by:')
            st.write(' - Citizen awareness:')
            st.write('        -To reduce displacements with a private vehicle (use Public transport, trips on foot or by bicycle)')
            st.write(' - Municipalities city hall:')
            st.write('        -Local media diffusion campaigns to explain the warning situation')
            st.write('        -Do not allow the burning of vegetation and enhance the management of plant residues, such as crushing or collection for its composting')
            st.write('        -Suspended construction work')
            st.write(' - Industry:')
            st.write('        -Do not perform processes such as start up or set up not indispensable, if they can be delayed')
        else:
            st.write('No Alert')
        
        
        
        
else:
    
    
    X_user1  = pd.DataFrame(porfin)
    st.table(porfin)  

    submit =st.button('Predict')

    if submit:   
        
        prediction = pipe_svc.predict(X_user1)
            
        if prediction == 1 and int(X_user1['PM2.5'])>=20:
            st.write('Alert activated')
            st.text('Countermeasures to be followed by:')
            st.write(' - Citizen awareness:')
            st.write('        -To reduce displacements with a private vehicle (use Public transport, trips on foot or by bicycle)')
            st.write(' - Municipalities city hall:')
            st.write('        -Local media diffusion campaigns to explain the warning situation')
            st.write('        -Do not allow the burning of vegetation and enhance the management of plant residues, such as crushing or collection for its composting')
            st.write('        -Suspended construction work')
            st.write(' - Industry:')
            st.write('        -Do not perform processes such as start up or set up not indispensable, if they can be delayed')
        else:
            st.write('No Alert')


# # 7. Launch App

# In[13]:




# In[14]:




# In[ ]:




