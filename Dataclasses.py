from dataclasses import dataclass

@dataclass
class AdvertisementData:
    ad_id: int
    title: str
    link: str
    housing: str
    housing_category: str
    city_area: str
    housing_type: str
    housing_state: str
    price: str
    living_area: str
    land_area: str
    price_per_meter: str
    lat: str
    long: str
    date: any



