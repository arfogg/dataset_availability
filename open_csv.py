import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
from datetime import datetime

file_dict = {"Forsyth" : "Forsyth2015.csv",
             "Frey" : "Frey_2004_2006.csv",
             "Lio" : "Lio_2010.csv",
             "NG" : "Newell_Gjerloev2011.csv",
             "Ohtani" : "Ohtani_Gjerloev2020.csv", 
             "Soph50" : "sophie_50.txt",
             "Soph75" : "sophie_75.txt",
             "Soph90" : "sophie_90.txt"}

def open_csv(key):
 
    if (key == "Soph50") or (key == "Soph75") or (key == "Soph90"):
        # Read in '.csv' file using key-value relationship established in dictionary
        file = file_dict[key]
        print('File you are accessing is: ', file)

        # Connect to Github copies of Substorm data published
        url= f"https://raw.githubusercontent.com/arfogg/dataset_availability/main/substorm_lists/sophie_substorm_list/{file}"
        data = np.loadtxt(url, skiprows = 13, delimiter = ' ', dtype = str)

        # Manipulate the time-date format in '.txt' files to easily interpretable columns
        data[:, 0] = [datetime.strptime(data[i, 0], "%Y/%m/%d-%H:%M:%S") for i in range(len(data))]
        data = pd.DataFrame(data, columns = ['Date-UTC', 'Phase', 'Flag'] )
        
        # Conversion of datatypes to NUMERIC (i.e. integer) and datetime
        data['Phase'] = pd.to_numeric(data['Phase'])
        data['Flag'] = pd.to_numeric(data['Flag'])
        data['Date-UTC'] = pd.to_datetime(data['Date-UTC'])

        # Omit data points that are flagged (i.e. where data['Flag'] == 1)
        data = data.iloc[np.where(data['Flag'] == 0)[0]]

        ## Create 6 columns separating year, month, day, hour, minute, second
        #data['Year'] = [data["Date-UTC"].iloc[i].year for i in range(np.shape(data)[0])]
        #data['Month'] = [data["Date-UTC"].iloc[i].month for i in range(np.shape(data)[0])]
        #data['Day'] = [data["Date-UTC"].iloc[i].day for i in range(np.shape(data)[0])]
        #data['Hour'] = [data["Date-UTC"].iloc[i].hour for i in range(np.shape(data)[0])]
        #data['Minute'] = [data["Date-UTC"].iloc[i].minute for i in range(np.shape(data)[0])]
        #data['Second'] = [data["Date-UTC"].iloc[i].second for i in range(np.shape(data)[0])]
    
    else:

        file = file_dict[key]
        print('File you are accessing is: ', file)

        # Connect to Github copies of Substorm data published
        url= f"https://raw.githubusercontent.com/arfogg/dataset_availability/main/substorm_lists/{file}"
        data = pd.read_csv(url)

        # Convert to proper datetime format
        data['Date_UTC'] = pd.to_datetime(data['Date_UTC'])

        ## Create 6 columns separating year, month, day, hour, minute, second
        #data['Year'] = [data["Date-UTC"].iloc[i].year for i in range(np.shape(data)[0])]
        #data['Month'] = [data["Date-UTC"].iloc[i].month for i in range(np.shape(data)[0])]
        #data['Day'] = [data["Date-UTC"].iloc[i].day for i in range(np.shape(data)[0])]
        #data['Hour'] = [data["Date-UTC"].iloc[i].hour for i in range(np.shape(data)[0])]
        #data['Minute'] = [data["Date-UTC"].iloc[i].minute for i in range(np.shape(data)[0])]
        #data['Second'] = [data["Date-UTC"].iloc[i].second for i in range(np.shape(data)[0])]
    

    return data
