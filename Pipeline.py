from bs4 import BeautifulSoup
from Excract.Excract import Excract
from Excract.Website import *
import requests

class Pipeline:

    def __init__(self, city, pages_limit, debug = False):
        self.city = city
        self.pages_limit = pages_limit
        self.debug = debug

        self.excractor = Excract()

        self.data = []


    def data_to_db(self) -> None:
        """main script to exctract data from nehnutelnosti.sk.     
        With provided City and page limit in class initialization it iterates over available pages and uses scrap_advertisements_container method.
        """


        for current_page in range(1, self.pages_limit):
            url = f"https://www.nehnutelnosti.sk/{self.city}/?p[page]={current_page}"
            web_page = requests.get(url)
            self.data.append(
                self.excractor.website.scrape_advertisements_container(
                    BeautifulSoup(web_page.content, 'html.parser'),
                    self.debug
                )
            )
            

        for page_data in self.data:
            for ad_data in page_data:
                print(ad_data)
