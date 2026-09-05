'''
python3 -m pip install 'duckdb==0.10.1'
python3 -m pip install numpy
python3 -m pip install requests
'''
import duckdb
import requests
from duckdb.typing import *

# configure duckdb
db = duckdb.connect(config={"allow_unsigned_extensions": True})
db.load_extension('h3ext')

# Get all cities in Hokkaido, Japan
db.sql("create table cities as select split_part(split_part(filename,'/', -1), '.', 1) as city, results[1].components.country as country, results[1].geometry.lat as latitude, results[1].geometry.lng as longitude, results[1].components.state state from read_json('/Users/jeromelefebvre/GitHub/python-1brc/asset data/*.json', filename=true) where country = 'Japan' and state Like 'Hokkaido%';")

# View the list
db.sql("from cities");

db.sql("select any_value(city), h3_latlng_to_cell(latitude, longitude,2) as h3cell from cities group by h3cell")

with open('api.key', 'r') as file:
    global api_key
    api_key = file.read().strip() 


def ow_current(lat,lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.request("GET", url, headers={}, data={})
    return response.text


ow_current(43.1954132, 140.7835618)
#db.remove_function("ow_current")
db.create_function("ow_current", ow_current, [DOUBLE,DOUBLE], VARCHAR)

db.sql("select first(city), h3_latlng_to_cell(latitude, longitude,3) as h3cell, cast(ow_current(first(latitude), first(longitude))->'main'->'temp' as double) as temp from cities group by h3cell order by temp desc")


