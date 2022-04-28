
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from secrets_1 import API_KEY
from secrets_1 import client_id
from secrets_1 import refresh_token
# from secrets_1 import access_token
import pandas as pd
from pandas.io.json import json_normalize
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import json
from flask import Flask, render_template
import io
from flask import Response



# API 

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': {client_id},
    'client_secret': {API_KEY},
    'refresh_token': {refresh_token},
    'grant_type': "refresh_token",
    'f': 'json'
}

#CACHING

CACHE_FILE_NAME = 'strava_cache.json'

def load_cache():
  try: 
    cache_file = open(CACHE_FILE_NAME, 'r')
    cache_contents = cache_file.read()
    cache = json.loads(cache_contents)
    cache_file.close()
  except:
    cache = {}
  return cache

def store_in_cache_file(cache):
  cache_contents = json.dumps(cache)
  cache_file = open(CACHE_FILE_NAME, 'w')
  cache_file.write(cache_contents)
  cache_file.close()  

def construct_unique_key(baseurl, params):
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key

strava_cache = load_cache()

def make_request_with_cache(url):
  request_key = construct_unique_key(url)
  if request_key in strava_cache.keys():
    print("Data from cache being used")
    return strava_cache[request_key]
  else:
    print("Searching webpage for data")
    response = requests.get(url)
    strava_cache[request_key] = response.text
    store_in_cache_file(strava_cache)
    return strava_cache[request_key]


# how to signal if more data needs to be cached  
if load_cache() != strava_cache:
  print("Requesting Token...\n")
  res = requests.post(auth_url, data=payload, verify=False)
  access_token = res.json()['access_token']
  print("Access Token = {}\n".format(access_token))

  header = {'Authorization': 'Bearer ' + access_token}
  param = {'per_page': 200, 'page': 1}
  df = requests.get(activites_url, headers=header, params=param).json()
  store_in_cache_file(df)
else:
  activities = pd.json_normalize(strava_cache)


# print(my_dataset[5]["name"])
# print(activities.columns)
# print(activities)

#CREATING DATASET

cols = ['name', 'upload_id', 'type', 'distance', 'moving_time',   
         'average_speed', 'max_speed','total_elevation_gain',
         'start_date_local', 'achievement_count'
       ]
activities = activities[cols]
activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
activities['start_time'] = activities['start_date_local'].dt.time
activities['start_date_local'] = activities['start_date_local'].dt.date
activities = activities.astype({'moving_time':'int'})
# print(activities.dtypes)


#CREATING SUBDATASETS

runs = activities.loc[activities['type'] == 'Run']
bikes = activities.loc[activities['type'] == 'Ride']

# print(runs)
# print(bikes)

#CREATING PLOTS 

# plt.plot(runs['start_date_local'], (runs['distance']/1609.344), color='blue', marker='o')
# plt.title('Distance Vs Date', fontsize=14)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('Distance (Miles)', fontsize=14)
# plt.grid(True)
# # plt.savefig('/static/styles/dis.png')
# # plt.show()

# plt.plot(runs['start_date_local'], (runs['average_speed']*2.237), color='blue', marker='o')
# plt.title('Average Speed over Time', fontsize=14)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('Average Speed (mph)', fontsize=14)
# plt.grid(True)
# plt.savefig('speedovertime_1.png')
# plt.show()


# plt.plot(runs['start_date_local'], (runs['moving_time']/60), color='blue', marker='o')
# plt.title('Average Moving Time Vs Date', fontsize=14)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('Average Moving Time (mins)', fontsize=14)
# plt.grid(True)
# # plt.savefig('movingtime.png')
# # plt.show()

# plt.plot(runs['start_date_local'], (runs['total_elevation_gain']), color='blue', marker='o')
# plt.title('Date Vs Elevation Gain', fontsize=14)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('Elevation Gain', fontsize=14)
# plt.grid(True)
# # plt.savefig('elegain.png')
# # plt.show()

# type = activities['type']
# ele_gain = activities['total_elevation_gain']
# plt.xlabel('Type')
# plt.ylabel('Elevation Gain')
# plt.title('Elevation gain by activity type')
# plt.bar(type, ele_gain)
# # plt.savefig('barelegain.png')
# # plt.show()

# type = activities['type']
# speed = (activities['max_speed']*2.237)
# plt.xlabel('Type')
# plt.ylabel('Max Speed (mph)')
# plt.title('Max speed by activity type')
# plt.bar(type, speed)
# # plt.savefig('barspeed.png')
# # plt.show()

# achievement = activities['achievement_count']
# distance = (activities['distance']/1609.344)
# plt.xlabel('Achievements')
# plt.ylabel('Distance (miles)')
# plt.title('Achievments by Distance')
# plt.bar(achievement, distance)
# plt.savefig('barachievement_1.png')
# plt.show()

# distance_1 = (runs['distance']/1609.344)
# avg_speed = (runs['average_speed']*2.237)
# plt.xlabel('Distance (miles)')
# plt.ylabel('Average Speed (mph)')
# plt.title('Average speed by distance for Runs')
# plt.bar(distance_1, avg_speed)
# # plt.savefig('bardis.png')
# # plt.show()





# #CREATING GRAPH/TREE
class BST:
  def __init__(self, key):
    self.key = key
    self.lchild = None
    self.rchild = None
  def insert(self, data):
    if self.key is None:
      self.key = data
      return
    if self.key > data:
      if self.lchild:
        self.lchild.insert(data)
      else:
        self.lchild = BST(data)
    else:
      if self.rchild:
        self.rchild.insert(data)
      else:
        self.rchild = BST(data)


moving_time_lst_r = (runs['moving_time']/60)
moving_time_lst_r = moving_time_lst_r.astype(int)
# print(f'moving type {moving_time_lst.dtypes}')
# print(moving_time_lst_r)
root_r = BST(int(input("Running \n Enter a time in minutes: ")))

for i in moving_time_lst_r:
  root_r.insert(i)


moving_time_lst_b = (bikes['moving_time']/60)
moving_time_lst_b = moving_time_lst_b.astype(int)
# print(f'moving type {moving_time_lst.dtypes}')
# print(moving_time_lst_b)
root_b = BST(int(input("Biking \n Enter a time in minutes: ")))

for i in moving_time_lst_b:
  root_b.insert(i)

#FLASK APP

app = Flask(__name__)

@app.route('/')

def homepage():
    return render_template('index.html')

@app.route('/graphs')

def plotChart():


  return render_template('activities.html')


# @app.route('/<name>')

# def name(name):
#     return render_template('name.html', name = name)

if __name__ == '__main__':
    print('start strava app', app.name)
    app.run(debug=True)



#SAVING TREE
# def isLeaf(tree):
#     if tree[1] is None and tree[2] is None:
#         return True
#     else:
#         return False
# def yes(prompt):
#     print(prompt)
#     answer = input()
#     if answer.lower() == 'yes' or answer.lower() == "yea" or answer.lower() == "yep" or answer.lower() == "yup": 
#         return True
#     else: 
#         return False 

# def saveTree(tree, treeFile):
#     if isLeaf(tree):
#         print("Leaf", file = treeFile)
#         print(tree[0], file = treeFile)
#     else:
#         print("Internal node", file = treeFile)
#         print(tree[0], file = treeFile)
#         saveTree(tree[1], treeFile)
#         saveTree(tree[2], treeFile)
