from Dataclasses import AdvertisementData
from datetime import datetime

class Transform:

    def __init__(self) -> None:
        pass

    def convert_data(self, data_to_convert: list) -> list:
        converted_data = []
        for page_data in data_to_convert:
            for ad_data in page_data:
                ad_data.living_area = self.string_to_float(ad_data.living_area)
                ad_data.land_area = self.string_to_float(ad_data.land_area)
                ad_data.price_per_meter = self.string_to_float(ad_data.price_per_meter)
                ad_data.lat = self.string_to_float(ad_data.lat)
                ad_data.long = self.string_to_float(ad_data.long)
                ad_data.price = self.string_to_float(ad_data.price)

                ad_data.date = self.string_to_timestamp(ad_data.date)

                ad_data.city_area = self.location_to_cityarea(ad_data.city_area)

                if ad_data.price == 0.0:
                    continue

                converted_data.append(ad_data)
        
        return converted_data


    def string_to_float(self, string_value: str) -> float:
        try:
            float_value = float(string_value)

        except ValueError:
            float_value = 0.0
        
        return float_value
    
    
    def string_to_timestamp(self, string_value: str) ->int:
        datetime_object = datetime.strptime(string_value, "%d.%m.%Y")
        timestamp = datetime_object.timestamp()

        return int(timestamp)
    
    def location_to_cityarea(self, location: str) -> str:
        try:
            split_string = location.split(",")
            return split_string[-1].strip()
        except:
            return location