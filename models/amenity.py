
from enum import IntEnum

class Amenity(IntEnum):
    ACCESSIBLE = 0
    AIR_CONDITIONED = 1
    USB_CHARGING = 2
    CCTV = 3
    WIFI = 4
    BIKE_RACK = 5
    DINING = 6
    GIFT_SHOP = 7
    CABINS = 8
    KIDS_AREA = 9
    PET_AREA = 10
    WORK_AREA = 11
    
    @property
    def display_name(self) -> str:
        match self:
            case Amenity.ACCESSIBLE:
                return 'Accessible'
            case Amenity.AIR_CONDITIONED:
                return 'Air conditioned'
            case Amenity.USB_CHARGING:
                return 'USB charging'
            case Amenity.CCTV:
                return 'CCTV cameras'
            case Amenity.WIFI:
                return 'WIFI'
            case Amenity.DINING:
                return 'Dining'
            case Amenity.GIFT_SHOP:
                return 'Gift shop'
            case Amenity.CABINS:
                return 'Cabins'
            case Amenity.KIDS_AREA:
                return 'Kids area'
            case Amenity.PET_AREA:
                return 'Pet area'
            case Amenity.WORK_AREA:
                return 'Work area'
    
    @property
    def icon(self) -> str:
        return self.name.lower().replace('_', '-')
    
    def __str__(self):
        return self.display_name
    
    @classmethod
    def parse(cls, obj: dict[str: bool]):
        amenities = set()
        for (key, value) in obj.items():
            if value:
                try:
                    amenities.add(Amenity[key.upper()])
                except:
                    pass
        return sorted(amenities)
