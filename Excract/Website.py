from Dataclasses import AdvertisementData
from bs4 import BeautifulSoup
import requests

class Website:
    def __init__(self):
        pass

    
    def scrape_advertisements_container(self, soup: BeautifulSoup, debug: bool) -> list:
        """scrapes container from provided html page, that contains advertisemenets of real estate

        usage: 
        >>> import requests
        >>> from bs4 import BeautifulSoup  
        >>> from Excract.Excract import Excract
        >>> from Excract.Website import *
        >>> exctractor = Exctract()
        >>> web_page = requests.get("https://www.nehnutelnosti.sk/kosice/?p[page]=1")
        >>> data = exctractor.website.scrape_advertisements_container(BeautifulSoup(web_page.content, 'html.parser'))
        >>> print(data)
        [AdvertisementData(ad_id='5062795', title='1,5 IZB. BYT, Ostravská ul., KE - JUH, 3.p., KOMPLETNÁ REKONŠTRUKCIA', link='https://www.nehnutelnosti.sk/5062795/1-5-izb-byt-ostravska-ul-ke-juh-3-p-kompletna-rekonstrukcia/', housing='Byty', housing_category='2 izbový byt', city_area='Slovensko, Košický kraj, okres Košice IV, okres Košice, Košice IV - Juh', housing_type='Predaj', housing_state='Kompletná rekonštrukcia', price='129700', living_area='40', land_area='0', price_per_meter='3242.50', lat='48.7003404', long='21.2537228', date='16.07.2023')]

        Args:
            soup (BeautifulSoup): provided html page
            debug (bool): if true, returns only first advertisements (takes shorter amount of time than scraping whole page)

        Returns:
            list: list of type AdvertisementData dataclass items
        """

        advertisement_items = soup.find_all('div', "advertisement-item")

        page_ads_data = []
        for advertisement_item in advertisement_items:
            page_ads_data.append(self.scrape_advertisement_item(advertisement_item))

            if debug:
                break
            
        return page_ads_data


    def scrape_advertisement_item(self, advertisement_item: BeautifulSoup) -> AdvertisementData:
        """this method scrapes advertisment item one ad from container. It creates dictionary of raw data that is used to create AdvertisementData dataclass.   
        scrapes available info from html item in container. Then, scraper enters link where ad is located and continues scraping data, that were not available from container point of view. 


        Args:
            advertisement_item (BeautifulSoup): provided html item 

        Returns:
            AdvertisementData: AdvertisementData dataclass that is used to store info about ad.
        """

        # creates raw data dict
        self.advertisement_item_data_raw = {}

        title_and_link = advertisement_item.find('a', "advertisement-item--content__title")

        # scrapes info from text of item html element
        self.advertisement_item_data_raw["title"] = title_and_link.text.replace('\xa0', ' ')
        self.advertisement_item_data_raw["link"] = title_and_link["href"]

        # scrapes info from atributes of item html element
        self.advertisement_item_data_raw["price"] = advertisement_item["data-ga4-price"]
        self.advertisement_item_data_raw["housing"] = advertisement_item["data-ga4-category"]
        self.advertisement_item_data_raw["housing_category"] = advertisement_item["data-ga4-category2"]
        self.advertisement_item_data_raw["city_area"] = advertisement_item["data-ga4-category3"]
        # TODO  refractor so only city stays (pomocou split a posledne v liste ulozit)
        self.advertisement_item_data_raw["housing_type"] = advertisement_item["data-ga4-category4"]
        self.advertisement_item_data_raw["housing_state"] = advertisement_item["data-ga4-category5"]

        # enetering link where ad is located
        self.scrape_advertisement(self.advertisement_item_data_raw["link"])

        return AdvertisementData(**self.advertisement_item_data_raw)
    

    def scrape_advertisement(self, link) -> None:
        """opens page of specific ad, and scrapes geolocation date of update and extracts info about specific parameters, that were hidden from container point of view.
        All data that is scraped is saved into raw data dictionary

        Args:
            link (string): url link where ad is located
        """

        page = requests.get(link)
        advertisement = BeautifulSoup(page.content, 'html.parser')

        # geolocation
        try:
            map_div = advertisement.find('div', {"id": "map-detail"})
            self.advertisement_item_data_raw["lat"] = map_div["data-map-lat"]
            self.advertisement_item_data_raw["long"] = map_div["data-map-long"]
        except TypeError:
            self.advertisement_item_data_raw["lat"] = 0.0
            self.advertisement_item_data_raw["long"] = 0.0

        # date of update
        date = advertisement.find('div', "date").text
        self.advertisement_item_data_raw["date"] = date[date.index("ie:") + 3:].replace(' ', '')

        # parameters
        paramter_info = advertisement.find('div', "parameter--info")
        parameters = paramter_info.find_all("li", "col-12 col-sm-6 col-md-4")

        parameters = [parameter.text.replace('\n', '') for parameter in parameters]
        parameters_text = ' '.join(parameters)

        self.scrape_advertisement_parameters(parameters_text)



    def scrape_advertisement_parameters(self, parameter: str) -> None:
        """scrapes info from paraters of item, provided in text form. Finds those that are interesting for us and saves them into raw data dict. 
        Reason why code looks like this is because of structure of those important parameters on website.

        Args:
            parameter (str): bunch of parameters
        """

        if "Úžit. plocha:" in parameter:
            self.advertisement_item_data_raw["living_area"] = parameter[parameter.index("Úžit.") + 14:parameter.index("m2") - 1]
        else:
            self.advertisement_item_data_raw["living_area"] = "0"

        if "Plocha pozemku:" in parameter:
            start = parameter.index("Plocha pozemku:") + 15
            end = parameter.index("m2", start)
            self.advertisement_item_data_raw["land_area"] = parameter[start:end - 1]
        else:
            self.advertisement_item_data_raw["land_area"] = "0"

        if "Cena za m2" in parameter:
            start = parameter.index("Cena za m2") + 12
            end = parameter.index("€/m")
            self.advertisement_item_data_raw["price_per_meter"] = parameter[start:end - 1].replace(',', '.').replace(' ', '')
        else:
            self.advertisement_item_data_raw["price_per_meter"] = "0"

        if "ID inzerátu: " in parameter:
            start = parameter.index("ID inzerátu: ") + 13
            self.advertisement_item_data_raw["ad_id"] = parameter[start:]
        else:
            self.advertisement_item_data_raw["ad_id"] = "0"
            # TODO refractor on dropping data about ad!! (if ad does not have an ID, it is not able to be inserted into DB)