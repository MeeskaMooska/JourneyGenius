import pandas as pd
import folium

# Sample data
data = {
    'name': [
        'Heathrow Airport', 'Charles de Gaulle Airport', 'Frankfurt Airport', 'Schiphol Airport', 
        'Barajas Airport', 'Leonardo da Vinci–Fiumicino Airport', 'Munich Airport', 'Zurich Airport',
        'Vienna International Airport', 'Copenhagen Airport'
    ],
    'latitude': [
        51.470020, 49.009690, 50.110924, 52.310539,
        40.471926, 41.800278, 48.353783, 47.450001,
        48.110278, 55.618023
    ],
    'longitude': [
        -0.454295, 2.547925, 8.682127, 4.768274,
        -3.566857, 12.238889, 11.786086, 8.570556,
        16.563583, 12.650800
    ]
}

# Create DataFrame
airports_df = pd.DataFrame(data)

# List of airport names to chain together
airport_chain = ['Heathrow Airport', 'Schiphol Airport', 'Frankfurt Airport', 'Munich Airport', 'Vienna International Airport']

# Create a folium map centered around the average latitude and longitude
map_center = [airports_df['latitude'].mean(), airports_df['longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=5, tiles='cartodbpositron')

# Plot all airports on the map
for i, row in airports_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name'],
        icon=folium.Icon(color='green')
    ).add_to(m)

# Draw lines between the airports in the chain
for i in range(len(airport_chain) - 1):
    departure_airport = airports_df[airports_df['name'] == airport_chain[i]].iloc[0]
    destination_airport = airports_df[airports_df['name'] == airport_chain[i + 1]].iloc[0]
    line = folium.PolyLine(
        locations=[
            [departure_airport['latitude'], departure_airport['longitude']],
            [destination_airport['latitude'], destination_airport['longitude']]
        ],
        color='blue',
        weight=3
    ).add_to(m)


def fetch_map():
    return m