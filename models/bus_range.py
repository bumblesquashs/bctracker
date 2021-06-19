
from enum import Enum

class BusRangeDescription(Enum):
    ARTIC = "Artic"
    CONVENTIONAL_30 = "30' Conventional"
    CONVENTIONAL_35 = "35' Conventional"
    CONVENTIONAL_40 = "40' Conventional"
    DECKER = "Double Decker"
    SHUTTLE = "Shuttle"
    SUBURBAN_30 = "30' Suburban"
    SUBURBAN_35 = "35' Suburban"
    SUBURBAN_40 = "40' Suburban"
    UNKNOWN = "Unknown"

class BusRange:
    def __init__(self, low, high, year, model, description):
        self.low = low
        self.high = high
        self.year = year
        self.model = model
        self.description = description

        self.size = (high - low) + 1

    def __str__(self):
        return f'{self.year} {self.model}'
    
    def __eq__(self, other):
        return self.low == other.low and self.high == other.high
    
    def contains(self, number):
        return self.low <= number <= self.high

def get(number):
    for bus_range in bus_ranges:
        if bus_range.contains(number):
            return bus_range
    return unknown_range

def is_valid(number):
    for bus_range in bus_ranges:
        if bus_range.contains(number):
            return True
    return False

unknown_range = BusRange(0, 0, '', 'Unknown', BusRangeDescription.UNKNOWN)

bus_ranges = [
    BusRange(1, 18, '2000', 'Dennis Dart SLF (35 foot)', BusRangeDescription.CONVENTIONAL_35),
    BusRange(101, 116, '2001', 'Dennis Dart SLF (35 foot)', BusRangeDescription.CONVENTIONAL_35),
    BusRange(221, 237, '2002', 'Dennis Dart SLF (35 foot)', BusRangeDescription.CONVENTIONAL_35),
    BusRange(1020, 1044, '2013', 'New Flyer XN40', BusRangeDescription.CONVENTIONAL_40),
    BusRange(1045, 1069, '2015', 'New Flyer XN40', BusRangeDescription.CONVENTIONAL_40),
    BusRange(1070, 1114, '2016', 'New Flyer XN40', BusRangeDescription.CONVENTIONAL_40),
    BusRange(1115, 1139, '2017', 'New Flyer XN40', BusRangeDescription.CONVENTIONAL_40),
    BusRange(1140, 1147, '2018', 'New Flyer XN40', BusRangeDescription.CONVENTIONAL_40),
    BusRange(1148, 1185, '2019', 'New Flyer XN40', BusRangeDescription.CONVENTIONAL_40),
    BusRange(1186, 1202, '2020', 'New Flyer XN40', BusRangeDescription.CONVENTIONAL_40),
    BusRange(2173, 2240, '2009', 'Ford/CBB E-450/Polar V', BusRangeDescription.SHUTTLE),
    BusRange(2311, 2315, '2010', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2316, 2339, '2012', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2340, 2341, '2012', 'Mercedes-Benz Sprinter MiniBus', BusRangeDescription.SHUTTLE),
    BusRange(2342, 2344, '2012', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2345, 2346, '2012', 'Mercedes-Benz Sprinter MiniBus', BusRangeDescription.SHUTTLE),
    BusRange(2347, 2367, '2012', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2368, 2368, '2012', 'Mercedes-Benz Sprinter MiniBus', BusRangeDescription.SHUTTLE),
    BusRange(2369, 2377, '2012', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2378, 2449, '2013', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2450, 2450, '2011', 'Mercedes-Benz Sprinter MiniBus', BusRangeDescription.SHUTTLE),
    BusRange(2451, 2557, '2014', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2558, 2618, '2015', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2619, 2624, '2015', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2625, 2636, '2016', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2637, 2640, '2016', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2641, 2662, '2017', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2663, 2687, '2018', 'Chevrolet/Arboc 4500/SOM28D', BusRangeDescription.SHUTTLE),
    BusRange(2688, 2722, '2020', 'Chevrolet/Girardin 4500/Micro Bird G5', BusRangeDescription.SHUTTLE),
    BusRange(2723, 2756, '2020', 'Chevrolet/Arboc 4500/SOF26G', BusRangeDescription.SHUTTLE),
    BusRange(2757, 2773, '2021', 'Chevrolet/Girardin 4500/Micro Bird G5', BusRangeDescription.SHUTTLE),
    BusRange(3001, 3015, '2013', 'Grande West Vicinity (27.5 foot)', BusRangeDescription.CONVENTIONAL_30),
    BusRange(3016, 3023, '2015', 'International/ElDorado 3200/Aero Elite', BusRangeDescription.SHUTTLE),
    BusRange(3024, 3028, '2018', 'International/ElDorado 3200/Aero Elite', BusRangeDescription.SHUTTLE),
    BusRange(4007, 4061, '2017', 'Grande West Vicinity (30 foot)', BusRangeDescription.CONVENTIONAL_30),
    BusRange(4062, 4070, '2017', 'Grande West Vicinity (30 foot)', BusRangeDescription.CONVENTIONAL_30),
    BusRange(4071, 4073, '2018', 'Grande West Vicinity (30 foot)', BusRangeDescription.CONVENTIONAL_30),
    BusRange(4200, 4231, '2020', 'Grande West Vicinity CNG (30 foot)', BusRangeDescription.CONVENTIONAL_30),
    BusRange(4400, 4432, '2017', 'Grande West Vicinity (35 foot)', BusRangeDescription.CONVENTIONAL_35),
    BusRange(4433, 4474, '2018', 'Grande West Vicinity (35 foot)', BusRangeDescription.CONVENTIONAL_35),
    BusRange(6000, 6029, '2017', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(8095, 8117, '1996', 'New Flyer D40LF', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9001, 9010, '2000', 'Dennis Trident', BusRangeDescription.DECKER),
    BusRange(9021, 9039, '2002', 'TransBus Trident', BusRangeDescription.DECKER),
    BusRange(9041, 9049, '2004', 'Alexander Dennis Enviro500', BusRangeDescription.DECKER),
    BusRange(9051, 9078, '2000', 'Dennis Dart SLF (35 foot)', BusRangeDescription.CONVENTIONAL_35),
    BusRange(9081, 9085, '2001', 'Dennis Dart SLF (35 foot)', BusRangeDescription.CONVENTIONAL_35),
    BusRange(9101, 9106, '2005', 'New Flyer DE40LF', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9201, 9210, '2006', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9211, 9231, '2006', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9232, 9267, '2007', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9268, 9289, '2008', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9290, 9300, '2008', 'Nova Bus LFS', BusRangeDescription.SUBURBAN_40),
    BusRange(9301, 9318, '2008', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9319, 9433, '2009', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9434, 9446, '2012-2013', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9447, 9486, '2015', 'Nova Bus LFS', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9501, 9526, '2008', 'Alexander Dennis Enviro500', BusRangeDescription.DECKER),
    BusRange(9527, 9527, '2008', 'Alexander Dennis Enviro500H (Hybrid)', BusRangeDescription.DECKER),
    BusRange(9528, 9528, '2007', 'Alexander Dennis Enviro500', BusRangeDescription.DECKER),
    BusRange(9529, 9531, '2008', 'Alexander Dennis Enviro500', BusRangeDescription.DECKER),
    BusRange(9532, 9542, '2020', 'Alexander Dennis Enviro500 MMC', BusRangeDescription.DECKER),
    BusRange(9701, 9749, '1996-1997', 'New Flyer D40LF', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9750, 9760, '1995-1996', 'New Flyer D40LF', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9815, 9828, '1998', 'New Flyer D40LF', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9831, 9856, '1998', 'New Flyer D40LF', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9861, 9878, '1998', 'New Flyer D40LF', BusRangeDescription.CONVENTIONAL_40),
    BusRange(9881, 9891, '1998', 'New Flyer D40LF', BusRangeDescription.CONVENTIONAL_40),
]