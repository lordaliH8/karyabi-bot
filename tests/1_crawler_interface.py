from src.crawler import CrawlerInterface


interface = CrawlerInterface()

print(interface.get_quera_jobs())
print(interface.get_jobinja_jobs())
print(interface.get_karboom_jobs())
print(interface.get_jobvision_jobs())
