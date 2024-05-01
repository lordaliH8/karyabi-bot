from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import pandas as pd


def get_boundary():
    home_page = requests.get("https://quera.org/magnet/jobs", "lxml").content
    soup = BeautifulSoup(home_page, "html.parser")
    boundary = soup.find_all("button", class_="chakra-button css-g3korc")
    pnum = []
    for b in boundary:
        pnum.append(b.text)
    return int(unidecode(pnum[-2]))


def get_description(link):
    result = requests.get(link, timeout=10).text
    soup = BeautifulSoup(result, "lxml")
    description = soup.find("div", class_="css-7viiwh")
    des = ""
    for p in description:
        des += p.text
    return des.replace("\n", " ").replace("\u200c", " ")


def quera_crawl():
    _employer = []
    _title = []
    _link = []
    _description = []
    _tags = []
    _date = []
    _city = []

    for i in range(1, get_boundary() + 1):
        home_page = "https://quera.org/magnet/jobs?page={}".format(i)
        result = requests.get(home_page, timeout=10).content
        soup = BeautifulSoup(result, "html.parser")
        jobs = soup.find_all("article", class_="css-150va0z")

        for job in jobs:
            title = job.find("a", class_="chakra-link css-spn4bz").text
            employer = job.find("p", class_="chakra-text css-1m52y4d").text
            link = "https://quera.org/" + job.find(
                "a", class_="chakra-link css-4a6x12"
            ).get("href")
            description = get_description(link)
            date = (
                job.find("div", class_="chakra-stack css-nm8t2j")
                .find("span")
                .get("title")
            )
            city = ""

            elem = job.find("div", class_="chakra-stack css-5ngv18")
            if elem:
                for span in elem.find("span"):
                    city = span.text
            else:
                city = "unknown"

            tags = []
            main_tags = job.find_all("div", class_="chakra-stack css-1iyteef")
            side_tags = job.find_all("span", class_="css-1qy3adt")
            prime_tags = job.find_all("span", class_="css-h1qgq")

            for tag in side_tags:
                for span in tag.find_all("span"):
                    tags.append(span.text)

            for tag in prime_tags:
                for span in tag.find_all("span"):
                    tags.append(span.text)

            for tag in main_tags:
                for span in tag.find_all("span"):
                    tags.append(span.text.replace("\u200c", " "))

            _employer.append(employer)
            _title.append(title)
            _link.append(link)
            _description.append(description)
            _tags.append(tags)
            _date.append(date)
            _city.append(city)

    columns = ["title", "description", "employer", "link", "tags", "city", "date"]

    dataframe = pd.DataFrame(
        list(zip(_title, _description, _employer, _link, _tags, _city, _date)),
        columns=columns,
    )

    return dataframe
