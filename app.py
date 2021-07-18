#!/usr/bin/env python
# coding: utf-8

# ## In this Notebook, I will prepare the app to be executed at the end of the script

# # 1. Import Libraries

# In[1]:


#Import libraries required
import os
import pandas as pd
import numpy as np
import pickle 
import streamlit as st 
import matplotlib.pyplot as plt
from PIL import Image
import requests
from bs4 import BeautifulSoup


# In[2]:


#Install packs needed


# In[3]:


#Web scrap page desired
r = requests.get('https://aqicn.org/city/spain/catalunya/tarragona-bonavista/es/')
soup = BeautifulSoup(r.text, 'lxml')


# In[12]:


# Let's import minimum values
f_min = soup.find_all('td', class_="tdmin")
pm25_min = (f_min[1].text)
pm10_min = (f_min[2].text)
NO2_min = (f_min[4].text)
t_min = (f_min[7].text)
p_min = (f_min[8].text)
v_min = (f_min[10].text)
features_min = [pm25_min,pm10_min,NO2_min,t_min,p_min,v_min]
def stringToFloat(a):

    return list(map(float, a))

a = stringToFloat(features_min)


# In[13]:


# Let's import maximum values
f_max = soup.find_all('td', class_="tdmax")
pm25_max = (f_max[1].text)
pm10_max = (f_max[2].text)
NO2_max = (f_max[4].text)
t_max = (f_max[7].text)
p_max = (f_max[8].text)
v_max = (f_max[10].text)
features_max = [pm25_max,pm10_max,NO2_max,t_max,p_max,v_max]
def stringToFloat(a):

    return list(map(float, a))

b = stringToFloat(features_max)


# In[6]:


print(a)
print(b)


# In[7]:


c = [(a[0]+b[0])/2,(a[1]+b[1])/2,(a[2]+b[2])/2,(a[3]+b[3])/2,(a[4]+b[4])/2,(a[5]+b[5])/2]
print(c)


# In[8]:


pickle_in = open('FrontEnd_docs_related/aplication.pkl', 'rb') 
pipe_svc = pickle.load(pickle_in) 


# In[9]:


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
select1 = st.sidebar.selectbox('Select method',(['Authomatic'],['Manual']))

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
    
    features2 = {'PM2.5': c[0], 'PM10': c[1],'NO2':c[2],'Pressió atmosfèrica': c[4],'Temperatura': c[3],'Velocitat del vent a 10 m (esc.)': c[5]}    
    X_user1  = pd.DataFrame([features2])
    st.table([features2])  

    submit =st.button('Predict')

    if submit:   
        
        prediction = pipe_svc.predict(X_user1)
            
        if prediction == 1 and a[0]>=20:
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


# In[10]:




# In[11]:




# In[ ]:




