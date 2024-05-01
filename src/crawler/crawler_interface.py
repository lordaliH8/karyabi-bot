from src.crawler.quera import quera_crawl
from src.crawler.karboom import karboom_crawler
from src.crawler.jobinja import jobinja_crawl
from src.crawler.jobvision import jobvision


class CrawlerInterface:

    def __init__(self):
        pass

    def get_quera_jobs(self):
        return quera_crawl()

    def get_jobinja_jobs(self):
        return jobinja_crawl()

    def get_karboom_jobs(self):
        return karboom_crawler()

    def get_jobvision_jobs(self):
        return jobvision()
