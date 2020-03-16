from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from fake_useragent import UserAgent
import random
import re

# Lists to append values for a dataframe
fullnames = []
times = []
years = []
countries = []
lists_of_splits = []
dates = []

# List with available seasons on swimrankings
seasons = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

# Regex to find split times in HTML text in "onmouseover" element
split_pattern = re.compile(r"split2[\\][']>(.....)")

# Random sleeping after each page and season to avoid being blocked
page_delays = [1, 2, 3, 4, 5]
season_delays = [2, 4, 6, 8, 10]

# Setting random referers and User-Agents for requests to avoid being blocked
referers = ["http://ltuswimming.com/", "https://zwemfed.be/", "http://mwchallenge.lv/", "https://swimming.lv/",
            "https://winterswimming-bled.com/", "https://www.google.pl/", "https://www.google.com/",
            "https://www.facebook.com/", "https://www.facebook.pl/", "https://www.youtube.com/"]

headers = {"User-Agent": UserAgent().random,
           "Referer": random.choice(referers)}

base_url = "https://www.swimrankings.net/index.php"
base_season_url = "https://www.swimrankings.net/index.php?page=rankingDetail&clubId=1&gender=1&course=LCM&agegroup=X_X&stroke=0&season="

# Iterating through seasons 2005 - 2020
for season in seasons:
    print("Scrapping data from season: ", season)
    from_place = 1 # To get ranking page from 1 place

    # Getting page with best results in season
    season_req = request.Request(base_season_url+str(season), headers=headers)
    season_site = BeautifulSoup(request.urlopen(season_req).read(), "html.parser")

    # Getting page with 200 IM best results in season
    grey_rows = season_site.findAll("tr", attrs={"class": "rankingList1"}) # List with distances has white and grey rows
    im_style = grey_rows[7].find("td", attrs={"class": "swimstyle"}) # 200 IM distance is 8th grey row
    piece_im_style_url = im_style.find("a", href=True) # Address to 200 IM after base_url
    im_style_url = base_url + piece_im_style_url["href"]
    im_style_base_url = im_style_url[:-1] # Delete "1" from the address to concatenate my from_place value
    req = request.Request(im_style_url, headers=headers)
    site = BeautifulSoup(request.urlopen(req).read(), "html.parser")

    # Getting number of all results for season - the element from the navigation i.e. "Places from 1 to 474"
    navigation_elements = site.findAll("td", attrs={"class": "navigation"})
    number_of_places = int(navigation_elements[9].text.split()[4])

    # 25 is a number of results for each page
    number_of_pages = int(number_of_places/25)

    # Iterating through all pages in season
    for page in range(number_of_pages+1):
        print("Page: ", page + 1)
        print("From place: ", from_place)
        for row in site.findAll("tr", attrs={"class": ["rankingList0", "rankingList1"]}):
            fullname = row.find("td", attrs={"class": "fullname"})
            year = row.find("td", attrs={"class": "rankingPlace"})
            country = row.find("td", attrs={"class": "name"})
            time = row.find("td", attrs={"class": "time"})
            date = row.find("td", attrs={"class": "date"})

            # To get split times from onmouseover attribute avoiding frequent requesting url with split times
            time_onmouseover = row.find("a", href=True, attrs={"class": "time"})
            if time_onmouseover is not None:
                onmouseover = time_onmouseover["onmouseover"]
            else:
                onmouseover = ""
            splits = split_pattern.findall(onmouseover)

            # Appending all values to lists
            fullnames.append(fullname.text)
            years.append(year.text)
            countries.append(country.text)
            times.append(time.text)
            lists_of_splits.append(splits)
            dates.append(date.text)

        # Requesting next page in season
        from_place += 25

        headers = {"User-Agent": UserAgent().random,
                   "Referer": random.choice(referers)}
        next_page_url = im_style_base_url+str(from_place)
        next_page_req = request.Request(next_page_url, headers=headers)
        site = BeautifulSoup(request.urlopen(next_page_req).read(), "html.parser")

        page_delay = np.random.choice(page_delays)
        sleep(page_delay)

    season_delay = np.random.choice(season_delays)
    sleep(season_delay)

# Creating dataframe with scrapped data
df = pd.DataFrame({"Swimmer name":fullnames,
                   "Year of birth":years,
                   "Country":countries,
                   "Time":times,
                   "Splits":lists_of_splits,
                   "Date":dates})

# Saving dataframe to csv file
df.to_csv("200_IM_results.csv", index=False)