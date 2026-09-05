import requests
import time
import json
import os
import sys

def build_weather_station_name_list():
    """
    Grabs the weather station names from example data provided in repo and dedups
    """
    station_names = []
    with open('/Users/jeromelefebvre/GitHub/python-1brc/data/weather_stations.csv', 'r') as file:
        file_contents = file.read()
    for station in file_contents.splitlines():
        if "#" in station or "/" in station:
            next
        else:
            station_names.append(station.split(';')[0])
    return list(set(station_names))
    #return sorted(list(set(station_names)))

def downloadDetails(city):
    api_key = '' # add API key
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key}'
    path = f'/Users/jeromelefebvre/GitHub/python-1brc/asset data/{city}.json'
    if os.path.exists(path):
        print(f'{city} is already downloaded')
        return
    response = requests.get(url)
    
    with open(path, 'w') as file:
        file.write(json.dumps(response.json(), indent=4))
    
    print(response.json()['rate']['remaining'])
    if int(response.json()['rate']['remaining']) < 2:
        print(response.json()['rate'])
        sys.exit()
    time.sleep(1)
    

# cities = ["Sagastyr", "Zemlya Bunge", "Agapa", "Tukchi", "Numto"]
cities = build_weather_station_name_list()

for city in cities:
    downloadDetails(city)
