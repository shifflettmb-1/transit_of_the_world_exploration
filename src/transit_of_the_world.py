#Jacquelynnes Code 
import pandas as pd 
import numpy as np
import os 
import seaborn as sns
import pylab as pl
import folium
from folium import plugins
from folium.plugins import MarkerCluster
import matplotlib.patches as mpatches
import plotly.express as px
import matplotlib.pyplot as plt

# import CSVs
cities_df= pd.read_csv("../data/cities.csv")
lines_df=pd.read_csv("../data/lines.csv")
station_lines_df=pd.read_csv("../data/station_lines.csv")
stations_df=pd.read_csv("../data/stations.csv")
systems_df=pd.read_csv("../data/systems.csv")
track_lines_df=pd.read_csv("../data/track_lines.csv")
tracks_df=pd.read_csv("../data/tracks.csv")

#Data Cleaning Cities DF
cities_df["city_long"] = cities_df["coords"].apply(lambda x: x.split('POINT(')[1].split(' ')[0])
cities_df["city_lat"] = cities_df["coords"].apply(lambda x: x.split('POINT(')[1].split(' ')[1].split(")")[0])
cities_df["start_year"] = cities_df["start_year"].fillna(0)
cities_df["city_id"] = cities_df["id"]
cities_df["city_name"] = cities_df["name"]
cities_df["city_url_name"] = cities_df["url_name"]
cities_df = cities_df.drop(["country_state", "coords", "id", "name", "url_name"], axis = 1)
cities_df.head(5)

# split lat/long list in tracks_df
#Data Cleaning track_df
tracks_df["track_id"] = tracks_df["id"]

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
tracks_df = tracks_df.drop(["id", "geometry"], axis = 1)

#merge tracks with cities df by city id
merged_t_c_df = pd.merge(tracks_df, cities_df[["city_id","city_name","country"]], on="city_id", how ="left")
merged_t_c_df

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
top_tracks = (tracks_df.groupby('track_id')['length'].sum() / 1000).sort_values(ascending=False)[:10]
top_tracks.sort_values().plot.barh()
plt.ylabel('Track ID')
plt.xlabel('Length (km)')
plt.title("Top 10 longest tracks in London", size=20)

# London Top 10 shortest tracks (Km)
plt.subplot(2, 2, 3)
shortest_tracks = (tracks_df.groupby('track_id')['length'].sum() / 1000).sort_values().head(10)
shortest_tracks.plot.barh(color='lightcoral')
plt.ylabel('Track ID')
plt.xlabel('Length (km)')
plt.title("Shortest 10 tracks in London", size=20)
plt.tight_layout()
plt.show()

#Data Cleaning Lines DF
lines_df["lines_id"] = lines_df['id']
lines_df["lines_name"] = lines_df["name"]
lines_df["lines_url_name"] = lines_df["url_name"]
lines_df = lines_df.drop(["id", "name", "url_name"], axis = 1)

#Merged city id, city name, country by city id between line/city
merged_line_city = pd.merge(lines_df, cities_df[["city_id","city_name","country"]], on="city_id", how ="left")

#Data Cleaning station lines df
station_lines_df["station_lines_id"] = station_lines_df["id"]
station_lines_df = station_lines_df.drop(["id"], axis = 1)
#merged lines df, cities df, station lines df by city id
merged_l_c_stl_df = pd.merge(station_lines_df, merged_line_city, on="city_id", how="left")

#Data Cleaning stations df
stations_df["stations_name"] = stations_df["name"]
stations_df["stations_id"] = stations_df["id"]
stations_df["stations_long"] = stations_df["geometry"].apply(lambda x: x.split('POINT(')[1].split(' ')[0])
stations_df["stations_lat"] = stations_df["geometry"].apply(lambda x: x.split('POINT(')[1].split(' ')[1].split(")")[0])

#merged city id, city name, country by city id between stations/city
stations_df = stations_df.drop(["id", "name","geometry"], axis = 1)
merged_st_c_df = pd.merge(stations_df, cities_df[["city_id","city_name","country"]], on="city_id", how ="left")


#create df with just london values
London = stations_df[stations_df["city_id"]==69]
#lat long of london
london_lat = cities_df[cities_df["city_id"] == 69]["city_lat"]
london_long = cities_df[cities_df["city_id"] == 69]["city_long"]
Lat = london_lat.iloc[0]
Long = london_long.iloc[0]

#map London
london_map=folium.Map([Lat,Long],zoom_start=12)

# Create the MarkerCluster and add it to the map
marker_cluster = MarkerCluster().add_to(london_map)

# Add markers to the *MarkerCluster*
for lat, lon, label in zip(London.stations_lat, London.stations_long, London.stations_name):
    folium.Marker(location=[lat, lon], popup=label).add_to(marker_cluster)

#london_map

#Data Cleaning systems_df
systems_df["systems_id"] = systems_df["id"]
systems_df["systems_name"] = systems_df["name"]
systems_df = systems_df.drop(["id", "name"], axis = 1)

merged_sys_c_df = pd.merge(systems_df, cities_df[["city_id","city_name","country"]], on="city_id", how ="left")

#Data Cleaning track_lines_df
track_lines_df["track_lines_id"] = track_lines_df["id"]
track_lines_df = track_lines_df.drop(["id"], axis = 1)
merged_tl_c_df = pd.merge(track_lines_df, cities_df[["city_id","city_name","country"]], on="city_id", how ="left")


"""
Creating Graph of each of the dataframes showing the number of transportation venues based on the city name

"""


grp_one = merged_l_c_stl_df.groupby("city_name")["station_lines_id"].count()
grp_two = merged_st_c_df.groupby("city_name")["stations_id"].count()
grp_three = merged_sys_c_df.groupby("city_name")["systems_id"].count()
grp_four = merged_tl_c_df.groupby("city_name")["track_lines_id"].count()
grp_five = merged_t_c_df.groupby("city_name")["track_id"].count()
grp_six = merged_l_c_stl_df.groupby("city_name")["lines_id"].count()

fig, axs = plt.subplots(5,1, figsize=(20,20))

#Bar graphs
axs[0].bar(grp_one.index, grp_one.values, color = "blue")
axs[1].bar(grp_two.index, grp_two.values, color = "green")
axs[2].bar(grp_four.index, grp_four.values, color = "orange")
axs[3].bar(grp_five.index, grp_five.values, color = "yellow")
axs[4].bar(grp_six.index, grp_six.values, color = "brown")

titles = ["Number of station lines by city", "Number of stations by city", "Number of track lines by city", "Number of tracks by city", "Number of lines by city"]
#Create multiple legend bars that correspond to the colors of the bar
blue_patch = mpatches.Patch(color='blue', label='stations_lines')
green_patch = mpatches.Patch(color='green', label='stations_id')
green_patch = mpatches.Patch(color='green', label='stations_id')


plt.xticks(fontsize=6)
#set the x axis to rotate 60 degrees to be able to read better
plt.setp(axs[0].get_xticklabels(), rotation=60, ha="right",
         rotation_mode="anchor")
plt.setp(axs[1].get_xticklabels(), rotation=60, ha="right",
         rotation_mode="anchor")
plt.setp(axs[2].get_xticklabels(), rotation=60, ha="right",
         rotation_mode="anchor")
plt.setp(axs[3].get_xticklabels(), rotation=60, ha="right",
         rotation_mode="anchor")
plt.setp(axs[4].get_xticklabels(), rotation=60, ha="right",
         rotation_mode="anchor")

for i, v in enumerate(titles):
    axs[i].set_title(v)
#plt.legend()
plt.tight_layout()
plt.show()

#This graph had more city names then the others so I made it individual
fig, axs = plt.subplots(figsize =(30,4))
axs.bar(grp_three.index, grp_three.values, color = "red")
axs.set_title("Number of systems by city")
plt.setp(axs.get_xticklabels(), rotation=60, ha="right",
         rotation_mode="anchor")
plt.tight_layout()
plt.show()