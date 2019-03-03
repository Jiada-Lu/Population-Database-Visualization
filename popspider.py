# Parse Pop Data
import sqlite3
import urllib.error
#import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
import requests
import json

# Ignore SSL certificate errors
#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE

datausa_url='https://api.datausa.io/api/?'


conn = sqlite3.connect('pop.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Population
    (id INTEGER PRIMARY KEY, Pop INTEGER,
    year_id INTEGER, county_id INTEGER )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Years
(Year INTEGER UNIQUE, RAWDATA TEXT  )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Counties
   (id INTEGER PRIMARY KEY, Cindex INTEGER UNIQUE, County TEXT , state_id INTEGER )''')

cur.execute('''CREATE TABLE IF NOT EXISTS States
(id INTEGER PRIMARY KEY,Sindex INTEGER UNIQUE, State TEXT UNIQUE ,
Lat FLOAT, Lng FLOAT)''')

while True:
    #check  which year has been parsed
    cur.execute('''SELECT year FROM Years ''')
    print('These years have been parsed:',[y[0] for y in cur])
    year=input('Enter the Year to search population: (year<2017) ')
    if len(year)<1: break
    try:
        year=int(year)
    except:
        print('Not a Number, Try Again.')
        continue

    #check if the year has been parsed



#https://api.datausa.io/api/?show=geo&sumlevel=County&year=2016&required=pop
    parms = dict()
    parms["show"]="geo"
    parms["sumlevel"]="County"
    parms["year"] = year
    parms["required"]="pop"
    url = datausa_url + urllib.parse.urlencode(parms)

    print('Retrieving', url)

    js = requests.get(url).json()

    #CHECK if data exists?
    if len(js['data'])==0:
        print("data doesn't exist, try again.")
        continue
    print('Retrieved', len(js['data']), 'characters')


    cur.execute('''INSERT OR IGNORE INTO Years (Year, RAWDATA)
            VALUES ( ?, ? )''', (year, json.dumps(js, indent=4)))
    conn.commit()

    #list of counties' dictionaries
    data = [dict(zip(js["headers"], d)) for d in js["data"]]
    #print(data)

    #get specific county data
    for subdata in data:
        county=subdata['geo']
        pop=subdata['pop']

        # insert into Population Table
        cur.execute('''INSERT OR IGNORE INTO Counties
        (Cindex ) VALUES ( ? )''',(county, ))
        cur.execute('''SELECT id FROM Counties WHERE Cindex=?''',(county, ))
        county_id=cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO Population
        (Pop, year_id, county_id) VALUES ( ?, ?, ? )''', (pop,year,county_id))
    conn.commit()
cur.close()
print('Run popclean.py to read the DATA & clean the databases.')
