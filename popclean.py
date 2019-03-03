#Match Pop Data with State & County
import sqlite3
import urllib.error
#import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
import requests
import json

conn = sqlite3.connect('pop.sqlite')
cur = conn.cursor()
#GET STATES
stateurl='https://api.datausa.io/attrs/geo/01000US/children/'
statejs = requests.get(stateurl).json()
statedata = [dict(zip(statejs["headers"], d)) for d in statejs["data"]]
#print(statedata)

for substatedata in statedata:
    sindex=substatedata['id']
    state=substatedata['name']
    # insert into State Table
    cur.execute('''INSERT OR IGNORE INTO States
    (Sindex, State ) VALUES ( ? , ? )''',(sindex,state))
    cur.execute('''SELECT id FROM States WHERE Sindex=?''',(sindex, ))
    conn.commit()
    state_id=cur.fetchone()[0]

    #GET COUNTIES
    countyurl='http://api.datausa.io/attrs/geo/'+str(sindex)+'/children/'
    countyjs = requests.get(countyurl.encode()).json()
    countydata = [dict(zip(countyjs["headers"], d)) for d in countyjs["data"]]
    #print(countydata)

    for subcountydata in countydata:
        cindex=subcountydata['id']
        county=subcountydata['name']
        # update County Table
        cur.execute('''UPDATE Counties SET County=? ,state_id=?
        WHERE Cindex=? ''',(county,state_id,cindex))
    conn.commit()

cur.close()
print('Database completed and cleand.')
print('You may now process the data using popdump.py, popdata.py or popjson.py')
