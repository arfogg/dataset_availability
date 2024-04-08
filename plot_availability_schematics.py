# -*- coding: utf-8 -*-
"""
Created on Mon May 22 17:59:42 2023

@author: A R Fogg
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def read_availability():
    
    availability_csv=r'Users\admin\Documents\Notes\lit_reviews\mission_start_and_end.csv'
    availability_csv=os.path.join('C:'+os.sep,availability_csv)
    
    
    print('Reading: ', availability_csv)
    
    df=pd.read_csv(availability_csv , dtype={'start_month':np.float64, 'start_year':np.float64, 'end_month':np.float64, 'end_year':np.float64})

    sdtime=[]
    edtime=[]
    for i in range(len(df)):
        #print(i, df.start_month.iloc[i], df.start_year.iloc[i])
        smo=df.start_month.iloc[i] if ~np.isnan(df.start_month.iloc[i]) else 1
        sdtime.append(pd.Timestamp(year=int(df.start_year.iloc[i]), month=int(smo), day=1))
        
        if np.isnan(df.end_year.iloc[i]):
            edtime.append(pd.Timestamp.now())
        else:
            emo=df.end_month.iloc[i] if ~np.isnan(df.end_month.iloc[i]) else 1   
            edtime.append(pd.Timestamp(year=int(df.end_year.iloc[i]), month=int(emo), day=1))

    df['sdtime']=sdtime
    df['edtime']=edtime
    
    
    return df
    

def all_space():
    
    df=read_availability()
    
    df=df.loc[df.space_ground_flag=='space'].reset_index(drop=True)
    
    fig,ax=plt.subplots()
    csize=15

    # Overplot a line for each mission
    for i in range(len(df)):
        ax.plot([df.sdtime.iloc[i], df.edtime.iloc[i]], [df.name.iloc[i], df.name.iloc[i]], linewidth=5)

    ax.set_xlim(left=pd.Timestamp(int(df.start_year.min())-1,1,1))        