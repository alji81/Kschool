# POLLUTANT ALERT SYSTEM

### INTRODUCTION
The main objective of this TFM is to develop a PM2.5 Pollutant Alert System application capable to predict in 24h forecast whether to Activate or not some countermeasures to keep pollutant values under threshold established by authorities.

To do so, this TFM will allow someone with a bit of knowledge in Data Science to understand how to:
   1.	Live download, pre-process and merge datasets from different formats structured into a unique dataset to be analysed.
   2.	Explore and select different features, and to compare different preparation and sampling methods.
   3.	Launch, compare and evaluate different Machine Learning classification techniques under comprehensive metrics.
   4.	Build a friendly FrontEnd interface to allow a non-Data Science knowledge user to predict PM2.5 pollutant 24h forecast.

MAIN REPORT file and Notebooks attached are complementary documents with full details about TFM information and all decisions taken.

### DATASETS
Pollutant and Meteorological datasets were downloaded automatically via Socrata API from  the domain belonging to government of Catalonia  http://www.analisi.transparenciacatalunya.cat

Tarragona-Bonavista (North-East Spain) was the location selected because of long-time PM2.5 pollutant data available, and surrounded industries, schools and high-density population co-living together.


### REPLICATION
To replicate the TFM, it is needed to follow strictly Notebooks sequenced below, supported by MAIN REPORT file:

A) Data acquisition: 
   - Pollutants: 1A.Obtain_data_pollutants.ipynb
   - Meteorological: 1B.Obtailn_data_meteo.ipynb
   
B) Data merge:
   - 2.Merge_data_pollutant_meteo.ipynb
   
C) Data cleansing, preparation and Analysis:
   - 3.Modelling.ipynb
   
D) FrontEnd:
   - FrontEnd.ipynb

### MODELLING
Exploratory data analysis, pre-processing, pre-sampling, over-sampling and feature selection methods were applied to simplify complexity of the dataset. Then, different classification models were run to evaluate the most suitable one, and used to launch later a FrontEnd. 
Results got, demonstrated that SVC tuned method provided best F1, Recall and Accuracy scores, and Confusion matrix results.
