# -*- coding: utf-8 -*-
"""
Created on Thu May 30 21:17:36 2019

@author: marco
"""

import os
import pandas as pd
from scipy.sparse import csr_matrix

# configure file path
data_path = os.getcwd()

# read data
df_paths = pd.read_csv(
    os.path.join(data_path, 'paths.csv'),
    usecols=['id', 'time_zone'],
    dtype={'id': 'int32', 'time_zone': 'str'})

df_interactions = pd.read_csv(
    os.path.join(data_path, 'interactions.csv'),
    usecols=['user', 'path', 'rating'],
    dtype={'user': 'int32', 'path': 'int32', 'rating': 'float32'})

#pivot ratings into paths features
df_path_features = df_interactions.pivot(
    index='path',
    columns='user',
    values='rating'
).fillna(0)

#pivot ratings into paths features
mat_movie_features = csr_matrix(df_path_features.values)