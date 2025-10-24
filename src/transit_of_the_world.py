#Jacquelynnes Code 
import pandas as pd 
import numpy as np
import os 
import seaborn as sns
import pylab as pl
import folium
from folium import plugins

# import CSVs
cities_df= pd.read_csv("../data/cities.csv")
lines_df=pd.read_csv("../data/lines.csv")
station_lines_df=pd.read_csv("../data/station_lines.csv")
stations_df=pd.read_csv("../data/stations.csv")
systems_df=pd.read_csv("../data/systems.csv")
track_lines_df=pd.read_csv("../data/track_lines.csv")
tracks_df=pd.read_csv("../data/tracks.csv")

# Get coordinates for lat long in cities
cities_df['Long']=cities_df['coords'].apply(lambda x: x.split('POINT(')[1].split(' ')[0])
cities_df['Lat']=cities_df['coords'].apply(lambda x: x.split('POINT(')[1].split(' ')[1].split(')')[0])
cities_df=cities_df.drop('coords', axis=1)
cities_df.head()

# split lat/long list in tracks_df


tracks_df.info()
tracks_df.head(10)
tracks_df[tracks_df["city_id"] == 69]
tracks_df["geometry"][0]

#tracks_df["Long"] = tracks_df["coords"].apply(lambda x: x.split('Line(')[1].split(' ')[0])
#tracks_df["Lat"] = tracks_df["coords"].apply(lambda x: x.split('POINT(')[1].split(' ')[1].split(")")[0])

def get_lat_long(x):
    if x == "LINESTRING Z EMPTY":
        return []
    else:
        x = x[:-1]
        lat_long_string= x.split('LINESTRING(')[1]
        lat_long_list = lat_long_string.split(",")
        lst = []
        for item in lat_long_list:
            lst.append(item.split(" "))
        return lst
    
tracks_df["Lat Long List"] = tracks_df["geometry"].apply(get_lat_long)
tracks_df["Lat Long List"].head(10)


# Get max min len of tracks in London 
import pandas as pd
import matplotlib.pyplot as plt

# Convert 'length' to numeric, coercing errors to NaN
tracks_df['length'] = pd.to_numeric(tracks_df['length'], errors='coerce')
# Drop rows with NaN in 'length'
tracks_df = tracks_df.dropna(subset=['length'])

plt.figure(figsize=(15, 10))

# London Top 10 longest tracks (Km)
plt.subplot(2, 2, 1)
top_tracks = (tracks_df.groupby('id')['length'].sum() / 1000).sort_values(ascending=False)[:10]
top_tracks.sort_values().plot.barh()
plt.ylabel('Track ID')
plt.xlabel('Length (km)')
plt.title("Top 10 longest tracks in London", size=20)

# London Top 10 shortest tracks (Km)
plt.subplot(2, 2, 3)
shortest_tracks = (tracks_df.groupby('id')['length'].sum() / 1000).sort_values().head(10)
shortest_tracks.plot.barh(color='lightcoral')
plt.ylabel('Track ID')
plt.xlabel('Length (km)')
plt.title("Shortest 10 tracks in London", size=20)

plt.tight_layout()
plt.show()