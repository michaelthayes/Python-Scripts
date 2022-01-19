# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 19:13:41 2022

@author: hayes
"""

from pymongo import MongoClient
from pprint import pprint
from random import randint
import pandas as pd

client = MongoClient('localhost')
db=client['admin']

serverStatusResult=db.command("serverStatus")
print(serverStatusResult)
pprint(serverStatusResult) # makes json fancy



#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(port=27017)
db=client['local']

#Step 2: Create sample data
names = ['Kitchen','Animal','State', 'Tastey', 'Big','City','Fish', 'Pizza','Goat', 'Salty','Sandwich','Lazy', 'Fun']
company_type = ['LLC','Inc','Company','Corporation']
company_cuisine = ['Pizza', 'Bar Food', 'Fast Food', 'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
for x in range(1, 501):
    business = {
        'name' : names[randint(0, (len(names)-1))] + ' ' + names[randint(0, (len(names)-1))]  + ' ' + company_type[randint(0, (len(company_type)-1))],
        'rating' : randint(1, 5),
        'cuisine' : company_cuisine[randint(0, (len(company_cuisine)-1))] 
    }
    #Step 3: Insert business object directly into MongoDB via insert_one
    result=db['reviews'].insert_one(business)
    #Step 4: Print to the console the ObjectID of the new document
    print('Created {0} of 500 as {1}'.format(x,result.inserted_id))
#Step 5: Tell us that you are done
print('finished creating 500 business reviews')


fivestar = db['reviews'].find_one({'rating': 5})
pprint(fivestar)

fivestarcount = db['reviews'].count_documents({'rating': 5})
print(fivestarcount)


cursor = db['reviews'].find({'rating': 5})
d = []
for document in cursor:
    d.append(document)
    
df = pd.DataFrame(d)
    

df.drop(['_id'], inplace=True, axis=1)

client = MongoClient('localhost')
db=client['local']

db['five_star'].insert_many(df.to_dict('records')) # records indicates how to format the json





