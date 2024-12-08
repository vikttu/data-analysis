from bs4 import BeautifulSoup
import requests

page_countries_area_population = requests.get("https://www.scrapethissite.com/pages/simple/")
soup = BeautifulSoup(page_countries_area_population.text, "html.parser")
country_names = soup.findAll("h3", attrs={"class": "country-name"})
country_populations = soup.findAll("span", attrs={"class": "country-population"})
country_areas = soup.findAll("span", attrs={"class": "country-area"})

for country_name, country_population, country_area in zip(country_names, country_populations, country_areas):
    print(country_name.text + " - " + country_population.text + " - " + country_area.text)
