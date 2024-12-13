from bs4 import BeautifulSoup
import requests
import db_manager
import os
from dotenv import load_dotenv

load_dotenv()

server_connection = db_manager.create_server_connection(os.getenv("HOST_NAME"), os.getenv("USER_NAME"), os.getenv("USER_PASSWORD"))

create_database_query = "CREATE DATABASE countries"

db_manager.create_database(server_connection, create_database_query)
database_connection = db_manager.connect_to_database(os.getenv("HOST_NAME"), os.getenv("USER_NAME"), os.getenv("USER_PASSWORD"), "countries")

create_country_table = """
CREATE TABLE country (
    country_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    country_population INT,
    country_area INT
)
"""

db_manager.execute_query(database_connection, create_country_table)


#Creates web scraper and stores the data in the variables
page_countries_area_population = requests.get("https://www.scrapethissite.com/pages/simple/")
soup = BeautifulSoup(page_countries_area_population.text, "html.parser")
country_names = soup.findAll("h3", attrs={"class": "country-name"})
country_populations = soup.findAll("span", attrs={"class": "country-population"})
country_areas = soup.findAll("span", attrs={"class": "country-area"})

#Populates db with the data scraped
populate_country = []

for country_name, country_population, country_area in zip(country_names, country_populations, country_areas):
    item = (country_name.text.strip(), country_population.text, country_area.text)
    populate_country.append(item)

populate_country_query = """
INSERT INTO country (country_name, country_population, country_area) VALUES
(%s, %s, %s)
"""

db_manager.executemany_query(database_connection, populate_country_query, populate_country)

#Dump the data into a csv file for analysis

retrieve_country_data = """
SELECT 
* 
FROM countries.country
INTO OUTFILE "C:/ProgramData/MySQL/MySQL Server 9.1/Uploads/country.csv"
FIELDS ENCLOSED BY '"'
TERMINATED BY ';'
ESCAPED BY '"'
LINES TERMINATED BY '\r\n';
"""

db_manager.execute_query(database_connection, retrieve_country_data)
