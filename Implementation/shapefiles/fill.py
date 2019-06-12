# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:24:18 2019

@author: marco
"""

import csv
from random import randint
import random

def interactions():
    with open('interactions.csv', 'a') as csvFile:
        for x in range(1,5000):
            n=randint(1, 50)
            m=randint(1,436)
            k=random.uniform(0.1,5)
            row = [x, n, m,k]
            writer = csv.writer(csvFile)
            writer.writerow(row)        
    csvFile.close()
    
def friends():
    with open('friends.csv', 'a') as csvFile:
        i=1
        for x in range(1,50):
            n_friends=randint(1,50)
            for k in range(1,n_friends):
                n=randint(1,50)
                if(n!=x):
                    row = [i,x,n]
                    i+=1
                    writer = csv.writer(csvFile)
                    writer.writerow(row)        
    csvFile.close()
interactions()


    