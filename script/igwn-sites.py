#!/usr/bin/env python
# coding: utf-8

# In[364]:


import numpy as np
import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="myloc")
f=open("sites.txt", 'r')
f.close()
#location = geolocator.geocode("Pasadena, CA 91125, USA")
#print(location.latitude) ; print(location.longitude)
#location = geolocator.geocode("LIGO Hanford Observatory, USA") ;  print(location.latitude) ; print(location.longitude) 


# In[366]:


lab=[]
institute=[]
address=[]
counter=0
lat=[]
lon=[]
country=[]
with open("sites.txt", 'r') as f:
    for line in f:
        line=line.strip('\n')
        print('raw input:',line)
        a=line.split(',')
        addr=""
        for i in range(1,len(a[1:])+1):
            addr=addr+a[i]
        location = geolocator.geocode(addr)
        result=str(location)
        if(result=='None'):
            #print('warning! initital match failed on counter:',counter)
            addr=""
            for i in range(2,len(a[2:])+1):
                addr=addr+a[i]
                location = geolocator.geocode(addr)
        if a[0] == 'OzGrav':
            lab=lab+['OzGrav']
        else:
            if len(a) <= 4:
                lab=lab+['Local Research Group']
            else:  
                lab=lab+[a[0]]
        excode=0
        for ic in range(0,len(a)):
            if 'Institute' in a[ic] or 'University' in a[ic] or 'Center' in a[ic] or 'College' in a[ic]:
                if 'University of London' in a[ic]:
                    institute=institute+[a[0]+a[ic]]
                else:
                    institute=institute+[a[ic]]
                excode=1
            if excode == 1:
                break
        if excode == 0:
            institute=institute+[a[0]]
                    
        country=country+[a[len(a)-1]]
        lat=lat+[location.latitude]
        lon=lon+[location.longitude]
        address=address+[addr]
        print(counter,lab[counter],institute[counter],lat[counter],lon[counter],country[counter])
        counter+=1
        #if counter==20:
         #   f.close()
          #  break


# In[367]:


f.close()


# In[368]:


import pandas as pd
d = {'Lab': lab, 'Institute': institute, 'Latitude': lat, 'Longtitude': lon, 'Country': country}
print(type(d))
print(type(institute))


# In[370]:


df = pd.DataFrame(d)
df.to_csv('igwn-sites-corrected.csv')


# In[371]:


df.head()


# In[372]:


aa=df['Institute'].unique()
np.size(aa)


# In[373]:


counter=0
for institute in aa:
    df2=df[df['Institute']==institute]
    col0=df2['Lab'].count()
    col1=df2['Institute'].unique()
    col2=df2['Latitude'].unique()
    col3=df2['Longtitude'].unique()
    col4=df2['Country'].unique()
    lat=str(col2[0])
    lon=str(col3[0])
    location = geolocator.reverse(lat+" "+lon, exactly_one=True,language="en-US")
    address = location.raw['address']
    city = address.get('city', '')
    if city == '':
        city = address.get('township','')
        if city == '':
            city = address.get('town','')
            if city == '':
                city = address.get('village','')
                if city == '':
                    city = address.get('hamlet','')
                    if city == '':
                        city = address.get('suburb','')
    if 'USA' in col4[0]:
        city=city+' '+address.get('state','')
    if counter == 83:
        city='Oxford Mississippi'
    #if counter == 59:
    #    break
    print(counter,city)
    col5 = [city]
    d = {'Institute': col1, 'Latitude': col2, 'Longtitude': col3, 'City': col5, 'Country': col4, 'Groups/Labs': col0}
    df3 = pd.DataFrame(d)
    if counter==0:
        df4 = df3
    else:
        df4 = pd.concat([df4, df3], axis=0)
    counter+=1
index=np.arange(len(df4))
df5=df4.set_index(index)


# In[374]:


df5.to_csv('igwn-sites-reduced.csv')
df5.head()


# In[375]:


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# In[376]:


from shapely.geometry import Point
import matplotlib.pyplot as plt


# In[377]:


df5.head(10)


# In[378]:


#method 1
listofpoints=[]
for icount in range(0,len(df5)):  
    lon=df5['Longtitude'][icount]
    lat=df5['Latitude'][icount]
    listofpoints=listofpoints+[Point(lon,lat)]


# In[379]:


s = gpd.GeoSeries(listofpoints,crs="EPSG:4326")
ax2=world.plot(figsize=(15, 10))
s.plot(color='r',ax=ax2)


# In[380]:


#method 2 - modifies df5. Do not reuse df5 above
gdf = gpd.GeoDataFrame(df5, geometry=gpd.points_from_xy(df5['Longtitude'], df5['Latitude']))


# In[382]:


#ax2=world.plot(figsize=(15, 10))
#s.plot(color='r',ax=ax2)
ax3 = world.plot(figsize=(15, 10))
gdf.plot(ax=ax3, color='red')
plt.show()


# In[383]:


#!pip install folium
df5.head()


# In[385]:


#gdf.to_file('igwn-dataframe.shp')  
gdf.to_file('igwn-dataframe.geojson', driver='GeoJSON')  


# In[386]:


world2=world[world.continent == 'North America']
gdf.plot(ax=world2.plot(figsize=(15, 10),color='gray',alpha=0.4,edgecolor="black"), column='Institute')
plt.xlim([-150, -40])
plt.ylim([20,60])
plt.title('IGWN Institutions - North America')
plt.show()


# In[387]:


import folium


# In[418]:


geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry ]
map2=folium.Map(location=[30, 0], zoom_start=2.1,min_zoom=1.8,max_bounds=True,width = '100%',height = '100%')


# In[419]:


i = 0
#from folium import IFrame

text = 'IGWN World Locations'

for coordinates in geo_df_list:
    #assign a color marker for the type of volcano, Strato being the most common
    if 'USA' in gdf.Country[i]:
        type_color = "green"
    elif 'Australia' in gdf.Country[i]:
        type_color = "blue"
    elif 'India' in gdf.Country[i]:
        type_color = "orange"
    elif 'United Kingdom' in gdf.Country[i]:
        type_color = "red"
    elif 'Canada' in gdf.Country[i]:
        type_color = "lightblue"
    elif 'Japan' in gdf.Country[i] or 'Korea' in gdf.Country[i]:
        type_color = "purple"
    else:
        type_color = "lightred"


    # Place the markers with the popup labels and data
    map2.add_child(folium.Marker(location = coordinates,
                            popup =
                            "Institute: " + str(gdf.Institute[i]) + '<br>' +
                            "City: " + str(gdf.City[i]) + '<br>' +
                            "Country: " + str(gdf.Country[i]) + '<br>'
                            "#Groups: " + str(gdf['Groups/Labs'][i]) + '<br>'
                            "Coordinates: " + str(geo_df_list[i]),
                            icon = folium.Icon(color = "%s" % type_color)))
    i = i + 1
print(type_color)


# In[420]:


map2


# In[421]:


map2.save("igwn-institutes.html")


# In[ ]:




