#!/usr/bin/env python
import numpy as np
import pandas as pd
import os



ratings= pd.read_csv('../csv_data/interactions.csv')

paths = pd.read_csv('../csv_data/paths.csv')

como_dataset = pd.read_csv('../csv_data/speedy_como_dataset2.csv')

def get_related_paths(pathId):

    paths_data = paths.merge(ratings,left_on='pathId',right_on='path')

    ratings_mean_count = pd.DataFrame(paths_data.groupby('title')['rating'].mean()) 

    ratings_mean_count['rating_counts'] = pd.DataFrame(paths_data.groupby('title')['rating'].count())  

    user_path_rating=paths_data.pivot_table(index='user',columns='title', values='rating')


    path1=user_path_rating['path' + str(pathId)]


    paths_like_path1=user_path_rating.corrwith(path1)


    corr_path1 = pd.DataFrame(paths_like_path1, columns=['Correlation'])
    corr_path1.dropna(inplace=True)


    corr_path1 = corr_path1.join(ratings_mean_count['rating_counts'])


    corr=corr_path1[corr_path1['rating_counts']>12].sort_values('Correlation', ascending=False)

    corr['path_title']=corr.index

    d = paths_data

    d.drop_duplicates(subset ="time_zone", keep = 'last', inplace = True) 


    c=corr.merge(d,left_on='path_title',right_on='title')




    dataset_merged = como_dataset.merge(c, how='inner', on='time_zone', validate='many_to_one')
    dataset_merged['coordinates'] = list(zip(dataset_merged.latitude, dataset_merged.longitude))

    grouped_dataset = dataset_merged.groupby().aggregate(list)


    return grouped_dataset['coordinates']
