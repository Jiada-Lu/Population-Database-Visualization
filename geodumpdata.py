#Write statepoplocate.data
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
cur.execute('''SELECT Years.Year, States.State, SUM(Population.Pop) AS Poptot,
     States.Lat, States.Lng FROM Population
     JOIN Counties ON Population.county_id = Counties.id
     JOIN States ON Counties.state_id = States.id
     JOIN Years ON Population.year_id = Years.year
     WHERE Years.Year=?
     GROUP BY States.State
     ORDER BY Years.Year DESC, States.State ,
     Counties.County , Population.Pop DESC''', (y, ))
#'w': write
#'state.data'
fhand = codecs.open('statepoplocate.data', 'w', "utf-8")
count=0
for row in cur :
    #fhand.write(row[1]+'\n')
    fhand.write(row[1]+', '+str(row[2])+', '+str(row[3])+', '+str(row[4])+'\n')
    count=count+1
cur.close()
fhand.close()
print(count, "records written to statepoplocate.data")
print("Run visualization.py to plot scatter&color pop density map.")
