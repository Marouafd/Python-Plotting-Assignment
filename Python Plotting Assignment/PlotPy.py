import pandas as pd
import folium
import geopy.distance
from folium.plugins import MarkerCluster


df = pd.read_csv('GrowLocations2.csv') #clean data set where the sensortypes with 0 lat and Long are deleted

latitude_col = 'Latitude'
longitude_col = 'Longitude'
sensor_name_col = 'SensorType'


uk_bounding_box = {
    'longitude_min': -10.592,
    'longitude_max': 1.6848,
    'latitude_min': 50.681,
    'latitude_max': 57.985
}

df = df[(df[longitude_col] >= uk_bounding_box['longitude_min']) & (df[longitude_col] <= uk_bounding_box['longitude_max']) &
        (df[latitude_col] >= uk_bounding_box['latitude_min']) & (df[latitude_col] <= uk_bounding_box['latitude_max'])]


map_center_uk = [53.5, -1.5]
# Since our dataset is large I calculated the distances between sensor locations 
# and the center of the expected area to identify the outliers
df['distance_to_center'] = df.apply(lambda row: geopy.distance.distance((row['Latitude'], row['Longitude']), map_center_uk).km, axis=1)

distance_threshold_km = 100  
outliers = df[df['distance_to_center'] > distance_threshold_km]
uk_map = folium.Map(location=map_center_uk, zoom_start=7)
folium.CircleMarker(
    location=map_center_uk,
    radius=15,  # Adjust the radius as needed
    color='red',
    fill=True,
    fill_color='red',
    fill_opacity=0.7,
    popup="Center of the Map",
).add_to(uk_map)

for index, row in df.iterrows():
    
    folium.CircleMarker(
        location=[row[latitude_col], row[longitude_col]],
        radius=10,  
        color='blue',  
        fill=True,
        fill_color='blue',
        fill_opacity=0.7,
        popup=f"Sensor: {row['SensorType']}<br>Distance to Center: {row['distance_to_center']:.2f} km", 
        tooltip=row['SensorType'],  
    ).add_to(uk_map)


uk_map.save("sensor_locations_uk_map.html")

print("Map created successfully. Check 'sensor_locations_uk_map.html'")
