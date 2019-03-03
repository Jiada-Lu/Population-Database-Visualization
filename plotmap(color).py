from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
from matplotlib import cm
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex

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
shp_info = map.readshapefile("C:\\Users\\asus\\Desktop\\Python File\\AccessWebData\\Project\\gadm36_USA_1",'states',drawbounds=True)
#print(map.states_info)
cmap = plt.cm.hot # use 'hot' colormap
hd=open('statepop.data')

lst=list()
maxpop=0
minpop=0
for row in hd:
    state=row.split(',')[0]
    pop=int(row.split(',')[1])
    if maxpop is None or maxpop < pop: maxpop = pop
    if minpop is None or minpop > pop: minpop = pop
    lst.append((state,pop))

for row in lst:
    state=row[0]
    pop=row[1]

    for info, shp in zip(map.states_info, map.states):
        statename = info['NAME_1']
        if statename == state:
            normal=float((pop-minpop))/(maxpop-minpop)
            colors = cmap(1.-np.sqrt(normal))[:3]
            colors=rgb2hex(colors)
            poly = Polygon(shp,facecolor=colors,edgecolor=colors, lw=3)
            ax1.add_patch(poly)

map.shadedrelief()

#State Polygons filled by Population Density
plt.title('Population distribution in America')
#plt.show()
plt.savefig('Population Distribution Map')
print('Run popdumpdata.py to choose another year.' )
