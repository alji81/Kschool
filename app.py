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

# In[2]:


pickle_in = open('FrontEnd_docs_related/aplication.pkl', 'rb') 
pipe_svc = pickle.load(pickle_in) 


# In[3]:


#Let's create a FrontEnd where the user can have an overview about Evolution of the 4 main Pollutants from period 2010-2020, and Predict if PM2.5 system Alert and meausures involved will be activated tomorrow. 
st.title('Pollutant Evolution and Preventive Alert System')
#st.write('This web app allows you to know Pollutant Evolution from 2010 to 2020 and PM2.5 24h prediction as Preventive Sytem Alert')



st.header('Pollutant Evolution')
st.write('This web app allows you to know Pollutant Evolution from 2010 to 2020 from pollutant selected')

st.sidebar.title("Pollutant")
select = st.sidebar.selectbox('Select Pollutant',(['PM2.5'],['PM10'],['NO2'],['NOx'],['NO'],['H2S'],['SO2']))

#submit2 =st.button('Graph')

#if submit2:
                              
if select == ['PM2.5']:
        st.image(Image.open('FrontEnd_docs_related/PM2.5.jpg'))
        st.write('Downward trend in average annual values obtained for pollutant PM2,5 during last years. The worst results were registered in 2015')
elif select == ['PM10']:
        st.image(Image.open('FrontEnd_docs_related/PM10.jpg'))
        st.write('Stable results with an upward trend in average annual values obtained for pollutant PM10 in recent years. The improvement in 2020 was due to the influence of the Covid-19 pandemic')
elif select == ['H2S']:
        st.image(Image.open('FrontEnd_docs_related/H2S.jpg'))
        st.write('Downward trend in average annual values obtained for pollutant H2S during last years. The worst results were registered in 2015')
elif select == ['NO']:
        st.image(Image.open('FrontEnd_docs_related/NO.jpg'))
        st.write('Stable results got for pollutant NO during last years')
elif select == ['NOx']:
        st.image(Image.open('FrontEnd_docs_related/NOx.jpg'))
        st.write('Stable results got for pollutant NOx during last years')
elif select == ['SO2']:
        st.image(Image.open('FrontEnd_docs_related/SO2.jpg'))
        st.write('Stable results with an upward trend in average annual values obtained for pollutant SO2 in recent years. The improvement in 2020 was due to the influence of the Covid-19 pandemic')
else:
        st.image(Image.open('FrontEnd_docs_related/NO2.jpg'))
        st.write('Stable results got for pollutant NO2 during last years')

    
        

st.header('Preventive System PM2.5 Alert')
st.write('This web app allows you to predict PM2.5 24h forecast. Preventive Sytem Alert is Activated when:')
st.write('     - average PM2,5 today feature exceeed threshold 25 micrograms/m3')
st.write('     - prediction at 24h does not improve the results')

PM25 =  st.number_input("PM2.5 (micrograms/m3):")
NO2 = st.number_input("NO2 (micrograms/m3):")
PM10 =  st.number_input("PM10 (micrograms/m3):")
Pressio_atmosferica = st.number_input("Atmospheric pressure (hPa):")
Temperatura = st.number_input("Temperature (ºC):")
Velocitat = st.number_input("Wind spped (m/s):")

submit =st.button('Predict')


features = {'PM2.5': PM25, 'PM10': PM10,'NO2':NO2,'Pressió atmosfèrica': Pressio_atmosferica,'Temperatura': Temperatura,'Velocitat del vent a 10 m (esc.)': Velocitat}
X_user  = pd.DataFrame([features])
#st.table(X_user)  



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


# In[4]:




# In[5]:




# In[ ]:




