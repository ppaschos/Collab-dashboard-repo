#!/usr/bin/env python
# coding: utf-8

# In[78]:


import numpy as np
import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="myloc")


# In[141]:


df=pd.read_csv('igwn-pool.csv')
df.head(37)


# In[142]:


aa=df['Institute Site'].unique()
np.size(aa)


# In[143]:


counter=0
for institute in aa:
    df2=df[df['Institute Site']==institute]
    countgpu=0
    for iscan in range(0,len(df2)):
        if 'gpu' in df2['COMPUTE ENTRY POINT (CE)'].values[iscan]:
            countgpu+=1
        countcpu=len(df2)-countgpu
        if countcpu == 0:
            col6=['gpu']
        elif countcpu == len(df2):
            col6=['cpu']
        else:
            col6=['cpu/gpu']
        if df2['COMPUTE ENTRY POINT (CE)'].values[iscan] == 'LIGO_US_LSU-QB2-CE1':
            col6=['gpu']
    col0=[len(df2)]
    col1=df2['Latitude'].unique()
    col2=df2['Longtitude'].unique()
    col3=df2['Hosted CE'].unique()
    col=df2['Institute Site'].unique()
    lat=str(col1[0])
    lon=str(col2[0])
    #if counter == 22:
    #    break
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
                    city = address.get('county','')
                    if city == '':
                        city = address.get('hamlet','')
                        if city == '':
                            city = address.get('suburb','')
    col4=[city]
    country=address.get('country', '')
    col5=[country]
    print(counter,institute,city,country,col3[0])
    d = {'Institute': col, 'Latitude': col1, 'Longtitude': col2, 'Type': col6, 'Number of EP': col0,'Hosted CE': col3,'City': col4, 'Country': col5}
    df3 = pd.DataFrame(d)
    if counter==0:
        df4 = df3
    else:
        df4 = pd.concat([df4, df3], axis=0)
    counter+=1
index=np.arange(len(df4))
df5=df4.set_index(index)
    


# In[144]:


df5


# In[145]:


#df5.to_csv('igwn-sites-reduced.csv')
df5.head()


# In[146]:


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# In[147]:


from shapely.geometry import Point
import matplotlib.pyplot as plt


# In[148]:


df5.head(10)


# In[149]:


#method 1
listofpoints=[]
for icount in range(0,len(df5)):  
    lon=df5['Longtitude'][icount]
    lat=df5['Latitude'][icount]
    listofpoints=listofpoints+[Point(lon,lat)]


# In[150]:


s = gpd.GeoSeries(listofpoints,crs="EPSG:4326")
ax2=world.plot(figsize=(15, 10))
s.plot(color='r',ax=ax2)


# In[151]:


#method 2 - modifies df5. Do not reuse df5 above
gdf = gpd.GeoDataFrame(df5, geometry=gpd.points_from_xy(df5['Longtitude'], df5['Latitude']))


# In[152]:


#ax2=world.plot(figsize=(15, 10))
#s.plot(color='r',ax=ax2)
#ax3 = world.plot(figsize=(15, 10))
#gdf.plot(ax=ax3, color='red')
#plt.show()


# In[153]:


#!pip install folium
df5.head()


# In[154]:


#gdf.to_file('igwn-dataframe.shp')  
gdf.to_file('igwn-pool-dataframe.geojson', driver='GeoJSON')  


# In[155]:


#world2=world[world.continent == 'North America']
#gdf.plot(ax=world2.plot(figsize=(15, 10),color='gray',alpha=0.4,edgecolor="black"), column='Institute')
#plt.xlim([-150, -40])
#plt.ylim([20,60])
#plt.title('IGWN Pool sites - North America')
#plt.show()


# In[169]:


import folium


# In[185]:


geo_df_list = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry ]
map2=folium.Map(location=[30, 0], zoom_start=2.1,min_zoom=1.8,max_bounds=True,width = '100%',height = '100%')


# In[186]:


i = 0
#from folium import IFrame

text = 'IGWN pool Locations'

for coordinates in geo_df_list:
    #assign a color marker for the type of volcano, Strato being the most common
    if 'United States' in gdf.Country[i]:
        type_color = "green"
    elif 'Australia' in gdf.Country[i]:
        type_color = "blue"
    elif 'India' in gdf.Country[i]:
        type_color = "orange"
    elif 'United Kingdom' in gdf.Country[i]:
        type_color = "red"
    elif 'Canada' in gdf.Country[i]:
        type_color = "lightblue"
    elif 'Taiwan' in gdf.Country[i] or 'Korea' in gdf.Country[i]:
        type_color = "purple"
    else:
        type_color = "lightred"


    # Place the markers with the popup labels and data
    map2.add_child(folium.Marker(location = coordinates,
                            popup =
                            "Institute: " + str(gdf.Institute[i]) + '<br>' +
                            "City: " + str(gdf.City[i]) + '<br>' +
                            "Country: " + str(gdf.Country[i]) + '<br>'
                            "EP: " + str(gdf['Number of EP'][i]) + '<br>'
                            "Hosted: " + str(gdf['Hosted CE'][i]) + '<br>'
                            "Type: " + str(gdf['Type'][i]) + '<br>'
                            "Coordinates: " + str(geo_df_list[i]),
                            icon = folium.Icon(color = "%s" % type_color)))
    i = i + 1


# In[187]:


map2


# In[188]:


map2.save("igwn-pool.html")


# In[ ]:




