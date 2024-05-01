import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_description(href):
    link = requests.get(href,timeout = 10).content
    soup = BeautifulSoup(link,'html.parser')
    if soup.find('div',class_="o-box__text s-jobDesc c-pr40p"):
        return soup.find('div',class_="o-box__text s-jobDesc c-pr40p").text
def get_tags(href):
    link = requests.get(href,timeout = 10).content
    soup = BeautifulSoup(link,'html.parser')
    tags = []
    for i in soup.find_all('span',class_="black"):
        temp = i.text
        tags.append(temp.replace("\n","").replace("  ","").replace("مهم نیست","").replace("u200c",""))
    return tags


def jobinja_crawl():
    _employer = []
    _title = []
    _link = []
    _description = []
    _tags = []
    _date = []
    _city = []
    for i in range(1, 5): ## for simplicity i limited the number of crawled pages
        website = "https://jobinja.ir/jobs/latest-job-post-%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85%DB%8C-%D8%AC%D8%AF%DB%8C%D8%AF?&page={}&preferred_before=1714466106&sort_by=published_at_desc".format(
            i)

        result = requests.get(website, timeout=10).content
        soup = BeautifulSoup(result, 'html.parser')

        jobs = soup.find_all('div', class_="o-listView__itemWrap c-jobListView__itemWrap u-clearFix")
        for job in jobs:
            title = job.find('a', class_="c-jobListView__titleLink").text
            date = job.find("span", class_="c-jobListView__passedDays").text
            temp = []
            land = job.find_all('li', class_="c-jobListView__metaItem")
            for i in land:
                for j in i.find_all('span'):
                    temp.append(j.text.replace(" ", ""))
            employer = temp[0]
            city = temp[1]

            link = job.find('a', class_="c-jobListView__titleLink").get('href')
            description = get_description(link)
            tags = get_tags(link)

            _employer.append(employer)
            _title.append(title)
            _link.append(link)
            _description.append(description)
            _tags.append(tags)
            _date.append(date)
            _city.append(city)

    columns = ['title', 'description', 'employer', 'link', 'tags', 'city', 'date']

    dataframe = pd.DataFrame(list(zip(_title, _description, _employer, _link, _tags, _city, _date)), columns=columns)
    return dataframe
