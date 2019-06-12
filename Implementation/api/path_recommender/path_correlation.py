#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os

def get_related_paths(id=40):
    id=str(id)
    title='path'+id
    ratings= pd.read_csv('./csv_data/interactions.csv')


    paths = pd.read_csv('./csv_data/paths.csv')


    paths_data=paths.merge(ratings,left_on='pathId',right_on='path')


    ratings_mean_count = pd.DataFrame(paths_data.groupby('title')['rating'].mean()) 



    ratings_mean_count['rating_counts'] = pd.DataFrame(paths_data.groupby('title')['rating'].count())  




    user_path_rating=paths_data.pivot_table(index='user', columns='title', values='rating')


    path1=user_path_rating[title]
 

    paths_like_path1=user_path_rating.corrwith(path1)


    corr_path1 = pd.DataFrame(paths_like_path1, columns=['Correlation'])  
    corr_path1.dropna(inplace=True)



    corr_path1.sort_values('Correlation', ascending=False).head(10)  


    corr_path1 = corr_path1.join(ratings_mean_count['rating_counts'])  




    corr=corr_path1[corr_path1['rating_counts']>12].sort_values('Correlation', ascending=False)


    corr['path_title']=corr.index



    d=paths_data


    d.drop_duplicates(subset ="time_zone", keep = 'last', inplace = True) 



    c=corr.merge(d,left_on='path_title',right_on='title')

    return c.head()
