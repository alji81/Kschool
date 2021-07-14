#!/usr/bin/env python
# coding: utf-8

# ## In this Notebook, I will prepare the app to be executed at the end of the script

# # 1. Import Libraries

# In[1]:


import pandas as pd 
import pickle 
import streamlit as st 
import matplotlib.pyplot as plt
from PIL import Image


# # 2. Import Model saved

# In[5]:


pickle_in = open('FrontEnd_docs_related/aplication.pkl', 'rb') 
pipe_svc = pickle.load(pickle_in) 


# In[6]:


#Let's create a FrontEnd where the user can have an overview about Evolution of the 4 main Pollutants from period 2010-2020, and Predict if PM2.5 system Alert and meausures involved will be activated tomorrow. 
st.title('Pollution Evolution and Preventive Alert System')
st.write('This web app allows you to know Pollutant Evolution from 2010 to 2020 and PM2.5 24h prediction as Preventive Sytem Alert')


st.header('Pollutant Evolution')

st.sidebar.title("Pollutant")
select = st.sidebar.selectbox('Select Pollutant',(['PM2.5'],['PM10'],['NO2'],['NOx'],['NO'],['H2S'],['SO2']))

submit2 =st.button('Graph')

if submit2:
                              
    if select == ['PM2.5']:
        st.image(Image.open('FrontEnd_docs_related/PM2.5.jpg'))
    elif select == ['PM10']:
        st.image(Image.open('FrontEnd_docs_related/PM10.jpg'))
    elif select == ['H2S']:
        st.image(Image.open('FrontEnd_docs_related/H2S.jpg'))
    elif select == ['NO']:
        st.image(Image.open('FrontEnd_docs_related/NO.jpg'))
    elif select == ['NOx']:
        st.image(Image.open('FrontEnd_docs_related/NOx.jpg'))
    elif select == ['SO2']:
        st.image(Image.open('FrontEnd_docs_related/SO2.jpg'))
    else:
        st.image(Image.open('FrontEnd_docs_related/NO2.jpg'))

    
        

st.header('Preventive System PM2.5 Alert')

PM25 =  st.number_input("PM2.5:")
NO2 = st.number_input("NO2 :")
PM10 =  st.number_input("PM10:")
Pressio_atmosferica = st.number_input("Pressio atmosferica:")
Temperatura = st.number_input("Temperatura:")
Velocitat = st.number_input("Velocitat del vent a 10 m (esc.):")

submit =st.button('Predict')


features = {'PM2.5': PM25, 'PM10': PM10,'NO2':NO2,'Pressió atmosfèrica': Pressio_atmosferica,'Temperatura': Temperatura,'Velocitat del vent a 10 m (esc.)': Velocitat}
X_user  = pd.DataFrame([features])
st.table(X_user)  



if submit:   
        
        prediction = pipe_svc.predict(X_user)
            
        if prediction == 1 and PM25>=20:
            st.write('Alert activated')
            st.text('Pondre algo mas')
        else:
            st.write('No Alert')


# In[7]:




# In[8]:




# In[ ]:




