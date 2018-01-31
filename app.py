__author__ = "Riccardo Brue"
__date__ = "$10-01-2018 17:14$"
######################################
# start of imports
import os
import requests
from bs4 import BeautifulSoup

# end of imports
######################################
#=====================================
"""
filename="name_list.txt"
try:
    os.remove(filename)
except OSError:
    pass

f=open(filename,"w+")

while True:
    name = input("Write your name: ")
    surname = input("Write your surname: ")
    print('Hello', name, surname)

    f.write(name+" "+surname+"\n")

    control=input("DO you want to continue? [y/n] ")
    if (control!="y" and control!="Y"):
        f.close()
        break
"""
#=====================================
"""
page = requests.get("http://www.bbc.co.uk/weather/2643743")
data = page.text
soup = BeautifulSoup(data, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))
"""
#=====================================
page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id="seven-day-forecast")
forecast_items = seven_day.find_all(class_="tombstone-container")
tonight = forecast_items[0]
#print(tonight.prettify())

period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

print(period)
print(short_desc)
print(temp)

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

print(short_descs)
print(temps)
print(descs)

