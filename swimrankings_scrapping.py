from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from fake_useragent import UserAgent
import random
import re

fullnames = []
times = []
years = []
countries = []
lists_of_splits = []
split_pattern = re.compile(r"split2[\\][']>(.....)")
dates = []
from_place = 1

base_url = "https://www.swimrankings.net/index.php"
start_website_url = "https://www.swimrankings.net/index.php?page=rankingDetail&rankingClubId=110032779&firstPlace="

referers = ["http://ltuswimming.com/", "https://zwemfed.be/", "http://mwchallenge.lv/", "https://swimming.lv/",
            "https://winterswimming-bled.com/", "https://www.google.pl/", "https://www.google.com/",
            "https://www.facebook.com/", "https://www.facebook.pl/", "https://www.youtube.com/"]

headers = {"User-Agent": UserAgent().random,
           "Referer": random.choice(referers)}


req = request.Request(start_website_url+"1", headers=headers)
site = BeautifulSoup(request.urlopen(req).read(), "html.parser")

# To get number of all results for each year - the element from the navigation i.e. "Places from 1 to 474"
navigation_elements = site.findAll("td", attrs= {"class": "navigation"})
number_of_places = int(navigation_elements[9].text.split()[4])

# 25 is a number of results for each page
number_of_pages = int(number_of_places/25)

for page in range(number_of_pages+1):
    for row in site.findAll("tr", attrs = {"class": ["rankingList0", "rankingList1"]}):
        fullname_class = row.find("td", attrs = {"class": "fullname"})
        fullname = fullname_class.find("a", href = True)
        year = row.find("td", attrs = {"class": "rankingPlace"})
        country = row.find("td", attrs={"class": "name"})
        time = row.find("a", href = True, attrs = {"class": "time"})
        date = row.find("td", attrs = {"class": "date"})
        onmouseover = time["onmouseover"]
        splits = split_pattern.findall(onmouseover)
        if fullname is not None:
            fullnames.append(fullname.text)
        else:
            fullnames.append("")
        years.append(year.text)
        countries.append(country.text)
        times.append(time.text)
        lists_of_splits.append(splits)
        dates.append(date.text)

    from_place += 25

    headers = {"User-Agent": UserAgent().random,
               "Referer": random.choice(referers)}
    next_page_url = start_website_url+str(from_place)
    next_page_req = request.Request(next_page_url, headers=headers)
    site = BeautifulSoup(request.urlopen(next_page_req).read(), "html.parser")

    delays = [1, 2, 3, 4, 5]
    delay = np.random.choice(delays)
    sleep(delay)

    print("Page ", page+1)
    print("To place ", from_place)

df = pd.DataFrame({"Swimmer name":fullnames,
                   "Year of birth":years,
                   "Country":countries,
                   "Time":times,
                   "Splits":lists_of_splits,
                   "Date":dates})

df.to_csv("swimmers6.csv", index = False)