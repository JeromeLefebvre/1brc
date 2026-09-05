import requests
def ow_current(city,state):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state}&units=metric&appid={api_key}"
    response = requests.request("GET", url, headers={}, data={})
    return response.text

db.create_function("ow_current", ow_current, [VARCHAR,VARCHAR], VARCHAR)

db.sql("select any_value(city), h3_latlng_to_cell(latitude, longitude,4) as h3cell, cast(ow_current(any_value(city),'Hokkaido')->'main'->'temp' as double) as temp from cities group by h3cell order by temp desc")
