/* Each file is made up of a JSON object */
select filename, results from read_json('../../../asset data/*.json', filename=true, ignore_errors=true) limit 6;

select filename, results[1]->'geometry' from read_json('../../../asset data/*.json', filename=true, ignore_errors=true) limit 6;

CREATE TABLE cities AS
SELECT  split_part(split_part(filename,'/',-1),'.',1) AS city
       ,results[1].components.country                 AS country
       ,results[1].geometry.lat                       AS latitude
       ,results[1].geometry.lng                       AS longitude
       ,results[1].components.state state
FROM read_json
('/Users/jeromelefebvre/GitHub/python-1brc/asset data/*.json', filename = true)
WHERE country = 'Japan'
AND state LIKE 'Hokkaido%';

load 'h3ext';

select h3_latlng_to_cell(43.1954132, 140.7835618, 1);

select *, h3_latlng_to_cell(latitude, longitude,1) as cell from cities;

select any_value(city), h3_latlng_to_cell(latitude, longitude, 2) as cell from cities group by cell;

CREATE TABLE allcities AS
SELECT  split_part(split_part(filename,'/',-1),'.',1) AS city
       ,results[1].components.country                 AS country
       ,results[1].geometry.lat                       AS latitude
       ,results[1].geometry.lng                       AS longitude
       ,results[1].components.state state
FROM read_json
('/Users/jeromelefebvre/GitHub/python-1brc/asset data/*.json', filename = true)

CREATE or replace TABLE allcities AS
SELECT *
FROM read_json
('/Users/jeromelefebvre/GitHub/python-1brc/asset data/*.json', ignore_errors= true, filename = true);