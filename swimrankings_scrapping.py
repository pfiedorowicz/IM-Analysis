from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from fake_useragent import UserAgent
import random

# from torrequest import TorRequest

names = []
times = []
split_times = []
from_place = 1

# tr = TorRequest(password="scrappingpswrdswim")

base_url = "https://www.swimrankings.net/index.php"
start_website_url = "https://www.swimrankings.net/index.php?page=rankingDetail&rankingClubId=110032779&firstPlace="

# response = tr.get(start_website_url+"1")
# site = BeautifulSoup(response.content, "html.parser")
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
        for fullname in row.findAll("td", attrs = {"class": "fullname"}):
            name = fullname.find("a", href = True)
        time = row.find("a", href = True, attrs = {"class": "time"})
        names.append(name.text)
        times.append(time.text)
        splits_website_url = base_url + time["href"]
        splits = []
        # splits_response = tr.get(splits_website_url)
        # headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
        headers = {"User-Agent": UserAgent().random,
                   "Referer": random.choice(referers)}
        splits_req = request.Request(splits_website_url, headers=headers)
        splits_site = BeautifulSoup(request.urlopen(splits_req).read(), "html.parser")
        for splitRow in splits_site.findAll("tr", attrs = {"class": ["splitInfo0", "splitInfo1"]}):
            for splitTime in splitRow.findAll("td", attrs = {"class": "splitTime"}):
                splits.append(splitTime.text)
        split_times.append(splits)
        delays = [1, 0.8, 0.6, 1.2, 0.3, 0.5]
        delay = np.random.choice(delays)
        sleep(delay)

    df = pd.DataFrame({"Swimmer name":names,
                       "Time":times,
                       "Splits":split_times})
    print(df)
    from_place += 25
    # tr.reset_identity()
    # next_page_response = tr.get(start_website_url+str(from_place))
    # next_page_url = base_url + navigation_elements[6].find("a")["href"]
    # headers = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
    headers = {"User-Agent": UserAgent().random,
               "Referer": random.choice(referers)}
    next_page_url = start_website_url+str(from_place)
    next_page_req = request.Request(next_page_url, headers=headers)
    site = BeautifulSoup(request.urlopen(next_page_req).read(), "html.parser")
    delays = [3, 4, 5, 6, 7, 8]
    if page % 4 == 0:
        print("Sleep for 40 secs!")
        sleep(38)
        print("Go ahead!")
        sleep(2)
    else:
        delay = np.random.choice(delays)
        sleep(delay)
    print("Page ", page+1)
    print("To place ", from_place)

df.to_csv("swimmers4.csv")

