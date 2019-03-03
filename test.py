from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np

fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
map = Basemap(projection='stere',lat_0=90,lon_0=-105,\
            llcrnrlat=23.41 ,urcrnrlat=45.44,\
            llcrnrlon=-118.67,urcrnrlon=-64.52,\
            rsphere=6371200.,resolution='l',area_thresh=10000)

map.drawmapboundary()
#map.fillcontinents()
map.drawstates()
map.drawcoastlines()
map.drawcountries()
#map.drawcounties()
#draw lat
parallels = np.arange(0.,90,10.)
map.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
#draw lng
meridians = np.arange(-110.,-60.,10.)
map.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
shp_info = map.readshapefile("C:\\Users\\asus\\Desktop\\Python File\\AccessWebData\\Project\\gadm36_USA_shp\\gadm36_USA_1",'states',drawbounds=True)
#print(map.states_info)
#cmap = plt.cm.hot # use 'hot' colormap
hd=open('statepoplocate.data')

Lpop=list()
Llat=list()
Llng=list()
maxpop=0
minpop=0
for row in hd:
    state=row.split(',')[0]
    pop=int(row.split(',')[1])
    lat=float(row.split(',')[2])
    lng=float(row.split(',')[3])
    if maxpop is None or maxpop < pop: maxpop = pop
    if minpop is None or minpop > pop: minpop = pop
    Lpop.append(pop)
    Llat.append(lat)
    Llng.append(lng)
print(Llng,Llat)
