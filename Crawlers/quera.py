from bs4 import BeautifulSoup
import requests
from unidecode import unidecode

home_page = requests.get("https://quera.org/magnet/jobs","lxml").content
soup = BeautifulSoup(home_page, 'html.parser')

#print(soup)

# ads = soup.find_all("article",class_="css-150va0z")
# for ad in ads :
#
#     print(ad.text)


def get_boundary():
    home_page = requests.get("https://quera.org/magnet/jobs", "lxml").content
    soup = BeautifulSoup(home_page, 'html.parser')
    boundary = soup.find_all("button", class_="chakra-button css-g3korc")
    pnum = []
    for b in boundary:
        pnum.append(b.text)
    return int(unidecode(pnum[-2]))

get_boundary()

def quera_crawl():
    _employer = []
    _title = []
    _source = []
    _description = []
    _tags = []
    _link = []
    _date = []

    for i in range(1,3):
        home_page = "https://quera.org/magnet/jobs?page={}".format(i)
        result = requests.get(home_page,timeout=5).content
        soup = BeautifulSoup(result, 'html.parser')
        jobs = soup.find_all("article",class_="css-150va0z")
        for job in jobs:
            employer = job.find("p",class_="chakra-text css-1m52y4d").text
            title = job.find("a",class_="chakra-link css-spn4bz").text
            tags = job.find("div",class_="chakra-stack css-1iyteef")
            for tag in tags:
                print(tag.text)

quera_crawl()