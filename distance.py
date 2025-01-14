import pandas as pd
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from math import radians, cos, sin, sqrt, atan2
import time

def read_data(file_path):
    print(f"Reading data from file: {file_path}")
    df = pd.read_excel(file_path, header=None)

    data = []
    i = 0
    while i < len(df):
        if (
            pd.isna(df.iloc[i, 0]) and
            i + 1 < len(df) and
            df.iloc[i + 1, 2] == "Patienten"
        ):
            print(f"Reached end of table at line {i}. Stopping.")
            break

        if (
            pd.isna(df.iloc[i, 0]) and
            df.iloc[i + 1, 1] == "Patientenliste"
        ):
            print(f"Ignored lines {i}-{i+2} (unwanted separator block).")
            i += 3
            continue

        patient_id = df.iloc[i, 1]
        last_name = df.iloc[i, 2]
        first_name = df.iloc[i, 3]
        postal_code = str(df.iloc[i+1, 1]).strip()

        city_parts = []
        col = 2
        while col < df.shape[1]:
            value = str(df.iloc[i+1, col]).strip()
            if "," in value:
                city_parts.append(value.split(",")[0])
                break
            if value and value.lower() != "nan":
                city_parts.append(value)
            col += 1

        city = " ".join(city_parts)

        address_parts = []
        for remaining_col in range(col + 1, df.shape[1]):
            value = str(df.iloc[i+1, remaining_col]).strip()
            if value and value.lower() != "nan":
                address_parts.append(value)

        address = " ".join(address_parts)

        data.append({
            'patient_id': patient_id,
            'name': f"{last_name} {first_name}",
            'postal_code': postal_code,
            'address': f"{address}, {postal_code} {city}"
        })
        print(f"Processed patient: {last_name} {first_name}, Address: {address}, Postal Code: {postal_code}")

        i += 2

    return pd.DataFrame(data)

def get_coordinates(address):
    geolocator = Nominatim(user_agent="patient_locator")
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Could not geocode address: {address}")
            return None, None
    except GeopyError as e:
        print(f"Error during geocoding: {e}")
        return None, None

def add_coordinates(data):
    print("Adding coordinates to patient data...")
    data['latitude'] = None
    data['longitude'] = None

    for index, row in data.iterrows():
        address = row['address']
        latitude, longitude = get_coordinates(address)
        data.at[index, 'latitude'] = latitude
        data.at[index, 'longitude'] = longitude
        time.sleep(1)

    return data

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def plot_histogram(data):
    print("Plotting distance histogram...")
    plt.hist(data['distance'], bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel('Distance to Practice (km)')
    plt.ylabel('Number of Patients')
    plt.title('Distribution of Patient Distances to Practice')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def main():
    file_path = input("Enter the path to the raw data file: ")
    practice_address = input("Enter the address of the practice: ")

    data = read_data(file_path)
    practice_lat, practice_lon = get_coordinates(practice_address)
    if practice_lat is None or practice_lon is None:
        print("Could not geocode the practice address. Exiting.")
        return

    data = add_coordinates(data)
    data['distance'] = data.apply(
        lambda row: calculate_distance(practice_lat, practice_lon, row['latitude'], row['longitude']) \
        if row['latitude'] and row['longitude'] else None, axis=1
    )

    print(data[['name', 'address', 'distance']])
    plot_histogram(data.dropna(subset=['distance']))

if __name__ == "__main__":
    main()
