#Write State.data & County.data with or without PopData
#Prepare for Retrieving the Lat & Lng Data from Google Map API
import sqlite3
import json
import codecs

conn = sqlite3.connect('pop.sqlite')
cur = conn.cursor()

cur.execute('''SELECT Year FROM Years ''')

y=input('Select a year from:'+str([y[0] for y in cur])+' ')
#cur.execute('''SELECT Years.Year, States.State, Population.Pop
#     FROM Population
#     JOIN Counties ON Population.county_id = Counties.id
#     JOIN States ON Counties.state_id = States.id
#     JOIN Years ON Population.year_id = Years.year
#     WHERE Years.Year=?
#     GROUP BY States.State
#     ORDER BY Years.Year DESC, States.State ,
#     Counties.County , Population.Pop DESC''', (y, ))
cur.execute('''SELECT Years.Year, States.State, SUM(Population.Pop) AS Poptot
     FROM Population
     JOIN Counties ON Population.county_id = Counties.id
     JOIN States ON Counties.state_id = States.id
     JOIN Years ON Population.year_id = Years.year
     WHERE Years.Year=?
     GROUP BY States.State
     ORDER BY Years.Year DESC, States.State ,
     Counties.County , Population.Pop DESC''', (y, ))
#'w': write
#'state.data'
fhand = codecs.open('statepop.data', 'w', "utf-8")
count=0
for row in cur :
    #fhand.write(row[1]+'\n')
    fhand.write(row[1]+', '+str(row[2])+'\n')
    count=count+1
cur.close()
fhand.close()
print(count, "records written to data file")
print("(1)Run geojson.py to read the Lat and Lng DATA.")
print("(2)Run geoload.py to insert the Lat and Lng DATA into database.")
print("(3)Run visualization.py to plot color pop density map.")
