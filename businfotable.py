TYPE_UNKNOWN = 0
TYPE_CONVENTIONAL = 1
TYPE_DECKER = 2
TYPE_SHUTTLE = 3
TYPE_30FOOT = 4
TYPE_35FOOT = 5
TYPE_SUBURBAN = 6
TYPE_ARTIC = 7


class BusRange:
    def __init__(self, low_num, high_num, year, model, type):
        self.low_num = low_num
        self.high_num = high_num
        self.year = year
        self.model = model
        self.type = type
        self.size = (high_num - low_num) + 1

    def get_yearnum(self):
        if '-' in self.year:
            return int(self.year.split('-')[0])
        else:
            return int(self.year)

    def is_in_range(self, fleetnum):
        if(type(fleetnum) == str):
            fleetnum = int(fleetnum)
        return (fleetnum >= self.low_num and fleetnum <= self.high_num)

def get_bus_range(fleet_num):
    for range in all_ranges:
        if(range.is_in_range(fleet_num)):
            return range
    return BusRange(0, 0, '0', 'Unknown Bus Type', TYPE_UNKNOWN)


all_ranges = [
    BusRange(1, 18, '2000', 'Dennis Dart SLF (35 foot)', TYPE_35FOOT),
    BusRange(101, 116, '2001', 'Dennis Dart SLF (35 foot)', TYPE_35FOOT),
    BusRange(221, 237, '2002', 'Dennis Dart SLF (35 foot)', TYPE_35FOOT),
    BusRange(221, 237, '2001', 'Dennis Dart SLF (35 foot)', TYPE_35FOOT),

    BusRange(1020, 1044, '2013', 'New Flyer XN40', TYPE_CONVENTIONAL),
    BusRange(1045, 1069, '2015', 'New Flyer XN40', TYPE_CONVENTIONAL),
    BusRange(1070, 1114, '2016', 'New Flyer XN40', TYPE_CONVENTIONAL),
    BusRange(1115, 1139, '2017', 'New Flyer XN40', TYPE_CONVENTIONAL),
    BusRange(1140, 1147, '2018', 'New Flyer XN40', TYPE_CONVENTIONAL),
    BusRange(1148, 1185, '2019', 'New Flyer XN40', TYPE_CONVENTIONAL),

    BusRange(2173, 2240, '2009', 'Ford/CBB E-450/Polar V', TYPE_SHUTTLE),
    BusRange(2311, 2315, '2010', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2316, 2339, '2012', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2340, 2341, '2012', 'Mercedes-Benz Sprinter MiniBus', TYPE_SHUTTLE),
    BusRange(2342, 2344, '2012', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2345, 2346, '2012', 'Mercedes-Benz Sprinter MiniBus', TYPE_SHUTTLE),
    BusRange(2347, 2367, '2012', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2368, 2368, '2012', 'Mercedes-Benz Sprinter MiniBus', TYPE_SHUTTLE),
    BusRange(2369, 2377, '2012', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2378, 2449, '2013', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2450, 2450, '2011', 'Mercedes-Benz Sprinter MiniBus', TYPE_SHUTTLE),
    BusRange(2451, 2557, '2014', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2558, 2618, '2015', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2619, 2624, '2015', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2625, 2636, '2016', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2637, 2640, '2016', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2641, 2662, '2017', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),
    BusRange(2663, 2687, '2018', 'Chevrolet/Arboc 4500/SOM28D', TYPE_SHUTTLE),

    BusRange(3001, 3005, '2013', 'Grande West Vicinity (27.5 foot)', TYPE_30FOOT),
    BusRange(3016, 3023, '2015',
             'International/ElDorado 3200/Aero Elite', TYPE_SHUTTLE),
    BusRange(3024, 3028, '2018',
             'International/ElDorado 3200/Aero Elite', TYPE_SHUTTLE),

    BusRange(4007, 4061, '2017', 'Grande West Vicinity (30 foot)', TYPE_30FOOT),
    BusRange(4062, 4070, '2017', 'Grande West Vicinity (30 foot)', TYPE_30FOOT),
    BusRange(4071, 4073, '2018', 'Grande West Vicinity (30 foot)', TYPE_30FOOT),
    BusRange(4400, 4432, '2017', 'Grande West Vicinity (35 foot)', TYPE_35FOOT),
    BusRange(4433, 4474, '2018', 'Grande West Vicinity (35 foot)', TYPE_35FOOT),

    BusRange(6000, 6029, '2017', 'Nova Bus LFS', TYPE_CONVENTIONAL),

    BusRange(8095, 8117, '1996', 'New Flyer D40LF', TYPE_CONVENTIONAL),

    BusRange(9001, 9010, '2000', 'Dennis Trident', TYPE_DECKER),
    BusRange(9021, 9039, '2002', 'TransBus Trident', TYPE_DECKER),
    BusRange(9041, 9049, '2004', 'Alexander Dennis Enviro500', TYPE_DECKER),
    BusRange(9051, 9078, '2000', 'Dennis Dart SLF (35 foot)', TYPE_35FOOT),
    BusRange(9081, 9085, '2001', 'Dennis Dart SLF (35 foot)', TYPE_35FOOT),
    BusRange(9101, 9106, '2005', 'New Flyer DE40LF', TYPE_CONVENTIONAL),
    BusRange(9201, 9210, '2006', 'Nova Bus LFS', TYPE_CONVENTIONAL),
    BusRange(9211, 9231, '2006', 'Nova Bus LFS', TYPE_CONVENTIONAL),
    BusRange(9232, 9267, '2007', 'Nova Bus LFS', TYPE_CONVENTIONAL),
    BusRange(9268, 9289, '2008', 'Nova Bus LFS', TYPE_CONVENTIONAL),
    BusRange(9290, 9300, '2008', 'Nova Bus LFS', TYPE_SUBURBAN),
    BusRange(9301, 9318, '2008', 'Nova Bus LFS', TYPE_CONVENTIONAL),
    BusRange(9319, 9433, '2009', 'Nova Bus LFS', TYPE_CONVENTIONAL),
    BusRange(9434, 9446, '2012-2013', 'Nova Bus LFS', TYPE_CONVENTIONAL),
    BusRange(9447, 9486, '2015', 'Nova Bus LFS', TYPE_CONVENTIONAL),
    BusRange(9501, 9526, '2008', 'Alexander Dennis Enviro500', TYPE_DECKER),
    BusRange(9527, 9527, '2008',
             'Alexander Dennis Enviro500H (Hybrid)', TYPE_DECKER),
    BusRange(9528, 9528, '2007', 'Alexander Dennis Enviro500', TYPE_DECKER),
    BusRange(9529, 9531, '2008', 'Alexander Dennis Enviro500', TYPE_DECKER),
    BusRange(9529, 9531, '2008', 'Alexander Dennis Enviro500', TYPE_DECKER),
    BusRange(9701, 9749, '1996-1997', 'New Flyer D40LF', TYPE_CONVENTIONAL),
    BusRange(9750, 9760, '1995-1996', 'New Flyer D40LF', TYPE_CONVENTIONAL),
    BusRange(9815, 9828, '1998', 'New Flyer D40LF', TYPE_CONVENTIONAL),
    BusRange(9831, 9856, '1998', 'New Flyer D40LF', TYPE_CONVENTIONAL),
    BusRange(9861, 9878, '1998', 'New Flyer D40LF', TYPE_CONVENTIONAL),
    BusRange(9881, 9891, '1998', 'New Flyer D40LF', TYPE_CONVENTIONAL),
]
