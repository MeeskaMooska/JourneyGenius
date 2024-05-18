import pandas as pd
from geopy.distance import geodesic
import numpy as np

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

airports_df = pd.DataFrame(data)

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).km

def find_airports_within_slice(airports_df, center, radius, angle_center, angle_range):
    def within_slice(row):
        point = (row['latitude'], row['longitude'])
        distance = calculate_distance(center, point)
        if distance > radius:
            return False
        angle = np.degrees(np.arctan2(point[1] - center[1], point[0] - center[0]))
        angle = (angle + 360) % 360
        return abs(angle - angle_center) <= angle_range / 2
    
    return airports_df[airports_df.apply(within_slice, axis=1)]

def find_airport_along_line(airports_df, departure, destination, radius, sliver_angle, visited_airports):
    angle_center = np.degrees(np.arctan2(destination[1] - departure[1], destination[0] - departure[0]))
    angle_center = (angle_center + 360) % 360
    
    for angle_range in np.arange(sliver_angle, 360, sliver_angle):
        possible_airports = find_airports_within_slice(airports_df, departure, radius, angle_center, angle_range)
        possible_airports = possible_airports[~possible_airports.index.isin(visited_airports)]
        
        if not possible_airports.empty:
            return possible_airports.iloc[-1]  # Return the furthest airport in this slice
    
    return None

def find_route(airports_df, departure_airport, destination_airport, radius):
    departure = (departure_airport['latitude'], departure_airport['longitude'])
    destination = (destination_airport['latitude'], destination_airport['longitude'])
    
    if calculate_distance(departure, destination) <= radius:
        return [departure_airport, destination_airport]
    
    current_airport = departure_airport
    route = [current_airport]
    visited_airports = set()
    visited_airports.add(current_airport.name)
    
    while calculate_distance((current_airport['latitude'], current_airport['longitude']), destination) > radius:
        next_airport = find_airport_along_line(
            airports_df,
            (current_airport['latitude'], current_airport['longitude']),
            destination,
            radius,
            sliver_angle=36,  # 10% slice (360 degrees / 10 slices)
            visited_airports=visited_airports
        )
        if next_airport is None:
            raise Exception("No route found within the given radius")
        
        route.append(next_airport)
        visited_airports.add(next_airport.name)
        current_airport = next_airport
    
    route.append(destination_airport)
    return route

# Define departure and destination airports
departure_airport = airports_df.iloc[0]
destination_airport = airports_df.iloc[-2]

# Define radius in km
radius = 600  # Example maximum range

# Find the route
try:
    order = []
    route = find_route(airports_df, departure_airport, destination_airport, radius)
    for airport in route:
        order.append(airport['name'])
except Exception as e:
    print(e)

print(order)