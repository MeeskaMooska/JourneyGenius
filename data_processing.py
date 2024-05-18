import pandas as pd

def process_airport_data():
    # Load the data
    airport_data = pd.read_csv('data/processed_airports.csv')
    
    # Drop the columns we don't need
    airport_data = airport_data.drop(columns=['municipality', 'scheduled_service', 'gps_code', 'local_code', 'elevation_ft'])

    # Drop rows with closed airports, small airports, and heliports
    airport_data = airport_data[~airport_data['type'].isin(['closed', 'small_airport', 'heliport'])]

    # Drop rows where longitude or latitude is missing
    airport_data = airport_data.dropna(subset=['latitude_deg', 'longitude_deg'])

    # Rename longitude and latitude columns
    airport_data = airport_data.rename(columns={
        'latitude_deg': 'latitude',
        'longitude_deg': 'longitude'
    })
    
    # Convert NaN continent values to NA
    airport_data['continent'] = airport_data['continent'].fillna('NA')

    airport_data.to_csv('data/processed_airports.csv', index=False)

def process_hotel_data():
    # Load the data
    hotel_data = pd.read_csv('data/processed_hotels.csv')

    # Split the Map column into latitude and longitude
    hotel_data[['latitude', 'longitude']] = hotel_data['Map'].str.split('|', expand=True)
    hotel_data['latitude'] = hotel_data['latitude'].astype(float)
    hotel_data['longitude'] = hotel_data['longitude'].astype(float)

    hotel_data = hotel_data.drop(columns='Map')
    '''hotel_data.columns = hotel_data.columns.str.strip()
    
    # Drop the columns we don't need
    columns_to_drop = ['cityCode', 'FaxNumber', 'PinCode', 'Description', 'Map']
    hotel_data = hotel_data.drop(columns=columns_to_drop)

    # Drop rows with 1 and 2 star ratings
    hotel_data = hotel_data[~hotel_data['HotelRating'].isin(['OneStar', 'TwoStar'])]

    hotel_data.to_csv('data/processed_hotels.csv', index=False)

    print(len(hotel_data))'''

    # Rename columns
    hotel_data = hotel_data.rename(columns={
        'HotelName': 'name',
        'HotelRating': 'rating',
        'HotelCode': 'code',
        'Address': 'address',
        'countyCode': 'country_code',
        'countyName': 'country',
        'cityName': 'city',
        'PhoneNumber': 'phone_number',
        'HotelWebsiteUrl': 'website_url',
        'Attractions': 'attractions',
        'HotelFacilities': 'facilities',
    })

    hotel_data.to_csv('data/processed_hotels.csv', index=False)

def process_landmark_data():
    # Load the data
    landmark_data = pd.read_csv('data/wonders_of_world.csv')

    # Drop the columns we don't need
    landmark_data = landmark_data.drop(columns=['Build in year'])

    # Rename columns to lower with underscores: Name,Type,Latitude,Longitude,Location,Wikipedia link,Picture link,Build in year
    landmark_data = landmark_data.rename(columns={
        'Name': 'name',
        'Type': 'type',
        'Latitude': 'latitude',
        'Longitude': 'longitude',
        'Location': 'location',
        'Wikipedia link': 'wikipedia_link',
        'Picture link': 'picture_link',
    })

    landmark_data.to_csv('data/processed_landmarks.csv', index=False)

process_landmark_data()