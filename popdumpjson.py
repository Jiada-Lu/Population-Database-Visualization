import sqlite3
import json
import codecs

conn = sqlite3.connect('pop.sqlite')
cur = conn.cursor()

#'w': write
fhand = codecs.open('countypop.json', 'w', "utf-8")
fhand.write('{\n')
num=0
cur.execute('''SELECT Year FROM Years ''')
for y in [y[0] for y in cur]:
    if num>0:
         fhand.write('],\n')
    cur.execute('''SELECT States.State, Counties.County,
     Population.Pop FROM Population
     JOIN Counties ON Population.county_id = Counties.id
     JOIN States ON Counties.state_id = States.id
     WHERE Population.year_id=?
     ORDER BY States.State ,
     Counties.County , Population.Pop DESC ''',(y, ))

    pops = list()
    maxpop = None
    minpop = None
    for row in cur :
        pops.append(row)
        pop = row[2]
        if maxpop is None or maxpop < pop: maxpop = pop
        if minpop is None or minpop > pop: minpop = pop

    if maxpop == minpop or maxpop is None or minpop is None:
        print(maxpop,minpop)
        print("Error - please run previous codes to complete database.")
        quit()
    #print(pops)
    fhand.write('"'+str(y)+'":\n[\n')
    count = 0
    for row in pops :
        if count > 0 : fhand.write(',\n')
        # print row
        pop = row[2]
        #normalize the rank to be color of the pop
        pop = 19 * ( (pop - minpop) / (maxpop - minpop) )
        fhand.write('{\n'+'"State":"'+str(row[0])+'",\n"County":"'+str(row[1])+'",\n')
        fhand.write('"popcolor":'+str(pop)+'\n}')
        count = count + 1
    num=num+1
fhand.write(']\n}\n')
fhand.close()
print('countypop.json created.')
