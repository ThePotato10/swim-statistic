import requests
from bs4 import BeautifulSoup
import sqlite3

url = "https://www.swimcloud.com/recruiting/rankings/2025/M/?page=31"
page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

con = sqlite3.connect("correlations.sqlite")
cur = con.cursor()

index = 1
for row in soup.find_all("tr"):
    swimmerLink = row.find("a", class_="u-text-semi")
    try:
        pageLink = swimmerLink['href']

        powerIndexPage = requests.get(f"https://www.swimcloud.com/{pageLink}/powerindex")
        powerIndexSoup = BeautifulSoup(powerIndexPage.content, "html.parser")

        events = powerIndexSoup.find_all("td", class_="u-text-truncate")
        bestEvents = []

        for event in events[:4]:
            bestEvents.append(event.text)

        try:
            cur.execute(f'INSERT INTO events VALUES ("{bestEvents[0]}", "{bestEvents[1]}", "{bestEvents[2]}", "{bestEvents[3]}")')
            
            print("Successfully entered into database: " + str(index))
            index += 1
        except Exception as e:
            print(e)
    except: 
        print("No link found")

con.commit()
con.close()