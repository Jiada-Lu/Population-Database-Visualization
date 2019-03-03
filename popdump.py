#Dump Pop Data
import sqlite3

conn = sqlite3.connect('pop.sqlite')
cur = conn.cursor()

cur.execute('''SELECT Years.Year, States.State, Counties.County, Population.Pop
     FROM Population
     JOIN Counties ON Population.county_id = Counties.id
     JOIN States ON Counties.state_id = States.id
     JOIN Years ON Population.year_id = Years.year
     ORDER BY Years.Year DESC, States.State ,
     Counties.County , Population.Pop DESC''')

#total counts
count = 0
for row in cur :
    print(row)
    count = count + 1
print(count, 'rows.')
cur.close()
