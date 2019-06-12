# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 18:57:52 2019

@author: marco
"""
import json
from user_predictions import recommend
from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

'''@app.route('/path')
def parsed(timezone):
   ''' 
@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<id>')
def hello_user(id):
    id=int(id)
    already_rated, predictions=recommend(id)
    d = predictions.to_dict(orient='record')
    j=json.dumps(d)
    print(j)
    return j

if __name__ == '__main__':
   app.run(debug = True)