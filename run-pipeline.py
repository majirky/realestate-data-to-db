from bs4 import BeautifulSoup
from Excract.Excract import Excract
from Excract.Website import *
from Load.Load import *
#from Load.MongoDatabase import *
from Transform.Transform import Transform
import requests
from dataclasses import asdict

class Pipeline:

    def __init__(self, city: str, pages_limit, debug = False):
        self.city = city.lower()
        self.pages_limit = pages_limit
        self.debug = debug

        self.excractor = Excract(self.city)
        self.transformer = Transform()
        self.loader = Load(self.city)

        self.data = []


    def data_to_db(self) -> None:
        """main script to exctract data from nehnutelnosti.sk.     
        With provided City and page limit in class initialization it iterates over available pages and uses scrap_advertisements_container method.
        """

        # ============= EXTRACT PART================
        for current_page in range(1, self.pages_limit):
            print(f"extracting page {current_page} ....")
            url = f"https://www.nehnutelnosti.sk/{self.city}/?p[page]={current_page}"
            web_page = requests.get(url)
            self.data.append(
                self.excractor.website.scrape_advertisements_container(
                    BeautifulSoup(web_page.content, 'html.parser'),
                    self.debug
                )
            )
            
        # ============ TRANSFORM PART==========
        print("transforming data....")
        self.data = self.transformer.convert_data(self.data)
        
        # ============LOAD PART============
        print("loading data into databases......")
        #self.data = [asdict(ad_data) for ad_data in self.data]
        self.loader.load_data(self.data)


if __name__ == "__main__":

    # if debug==true, scraper scrapes only 1 ad
    pipeline = Pipeline("kosice", 30, debug=False)
    pipeline.data_to_db()
        
