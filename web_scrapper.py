from bs4 import BeautifulSoup
import requests
import db_manager    

db_manager.create_server_connection()
db_manager.create_database()
db_manager.connect_to_database()

#Creates web scraper and stores the data in the variables
page_countries_area_population = requests.get("https://www.scrapethissite.com/pages/simple/")
soup = BeautifulSoup(page_countries_area_population.text, "html.parser")
country_names = soup.findAll("h3", attrs={"class": "country-name"})
country_populations = soup.findAll("span", attrs={"class": "country-population"})
country_areas = soup.findAll("span", attrs={"class": "country-area"})

#Populates db with the data scraped
for country_name, country_population, country_area in zip(country_names, country_populations, country_areas):
    print(country_name.text + " - " + country_population.text + " - " + country_area.text)

#Dump the data into a csv file for analysis
