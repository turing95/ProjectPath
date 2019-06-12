# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 22:48:44 2019

@author: marco
"""
import pandas as pd

df = pd.read_csv('Datasets/Como_dataset.csv')

print('tot records:',df.count()) #to understand the number of rows

print('groupby ts:',df.groupby('ts').count()) #to understand if ts is already rounded and used as unique identifier

df['date'] = pd.to_datetime(df['ts'],unit='ms')#to convert ts in datetime
print(df)

df['date_s']=df['date'].dt.round('1s')#to round date to seconds 
print(df)

df['date_min']=df['date_s'].dt.round('1min')#to round date to minutes 
print(df)

print('groupby ts:',df.groupby('date_min').count()) #to group by rounded date, maybe i can understand approximately how many people are in df


d=df.groupby('date_min').agg(lambda x: list(x)) #create a subset of lists  groupbying date_min
print(list(d))


print(d.drop(columns=['date_s', 'date','latitude','longitude','ts','time_zone']))