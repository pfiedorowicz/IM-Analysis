from urllib import request
from bs4 import BeautifulSoup
import pandas as pd

names = []
times = []
split_times = []

base_url = "https://www.swimrankings.net/index.php"
start_website_url = "https://www.swimrankings.net/index.php?page=rankingDetail&rankingClubId=110032779&firstPlace=1"
site = BeautifulSoup(request.urlopen(start_website_url).read(), "html.parser")

for row in site.findAll("tr", attrs = {"class": ["rankingList0", "rankingList1"]}):
    for fullname in row.findAll("td", attrs = {"class": "fullname"}):
        name = fullname.find("a", href = True)
    time = row.find("a", href = True, attrs = {"class": "time"})
    names.append(name.text)
    times.append(time.text)
    splits_website_url = base_url + time["href"]
    splits = []
    splits_site = BeautifulSoup(request.urlopen(splits_website_url).read(), "html.parser")
    for splitRow in splits_site.findAll("tr", attrs = {"class": ["splitInfo0", "splitInfo1"]}):
        for splitTime in splitRow.findAll("td", attrs = {"class": "splitTime"}):
            splits.append(splitTime.text)
    split_times.append(splits)

df = pd.DataFrame({"Swimmer name":names, "Time":times, "Splits":split_times})
df.to_csv('swimmers.csv', index=False, encoding='utf-8')

print(df)
