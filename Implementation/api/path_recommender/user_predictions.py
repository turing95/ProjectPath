# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 19:06:27 2019

@author: marco
"""
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds

import os


ratings = pd.read_csv('./csv_data/interactions.csv')
paths=pd.read_csv('./csv_data/paths.csv')
users=pd.read_csv('./csv_data/users.csv')

ratings= ratings.drop_duplicates(subset=['user', 'path'])
R_df = ratings.pivot(index = 'user', columns ='path', values = 'rating').fillna(0)

R = R_df.as_matrix()
user_ratings_mean = np.mean(R, axis = 1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)


U, sigma, Vt = svds(R_demeaned, k = 49)

sigma=np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)
preds_df.head()


def recommend_movies(predictions_df, user, paths_df, original_ratings_df, num_recommendations=5):
    
    # Get and sort the user's predictions
    user_row_number = user - 1 # UserID starts at 1, not 0
    sorted_user_predictions = preds_df.iloc[user_row_number].sort_values(ascending=False) # UserID starts at 1
    
    # Get the user's data and merge in the movie information.
    user_data = original_ratings_df[original_ratings_df.user == (user)]
    user_full = (user_data.merge(paths_df, how = 'left', left_on = 'path', right_on = 'pathId').
                     sort_values(['rating'], ascending=False)
                 )

    print ('User {0} has already rated {1} movies.'.format(user, user_full.shape[0]))
    print ('Recommending highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
    
    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (paths_df[~paths_df['pathId'].isin(user_full['path'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'pathId',
               right_on = 'path').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    return user_full, recommendations

def recommend(usr):
    return recommend_movies(preds_df, usr, paths, ratings, 10)
# In[90]:
'''

already_rated, predictions = recommend_movies(preds_df, 40, paths, ratings, 10)


# In[91]:


already_rated.head(10)


# In[92]:


print(predictions)

'''
