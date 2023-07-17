from enum import Enum

class Url(Enum):
    USJ = "https://www.usj.edu.lb"

class Path(Enum):
    Links = "../data/links.txt"
    ScrapedLinks = "../data/scraped_links.pkl"
    ScrapedText = "../data/text_data.txt"
