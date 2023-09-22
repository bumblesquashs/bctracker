from models.bcf_order import BcfOrder
from models.bcf_ferry import BcfFerry
from helpers.model import find as model_find
from helpers.bcf_scraper import VesselInfo

bcf_orders = []

def load():
    global bcf_orders
    bcf_orders = [
      BcfOrder(['Island Gwawis','Island Kwigwis', "Island K`ulut`a", 'Island Nagalis'], '2020-2021', model_find('island_class')),
      BcfOrder(['Island Aurora','Island Discovery'], '2017-2019', model_find('island_class')),
      BcfOrder(['Spirit of British Columbia', 'Spirit of Vancouver Island'], '1991-1992', model_find('s_class')),
      BcfOrder(['Coastal Renaissance', 'Coastal Inspiration', 'Coastal Celebration'], '2007', model_find('coastal_class')),
      BcfOrder(['Queen of Coquitlam', 'Queen of Cowichan', 'Queen of Alberni'], '1976', model_find('c_class')),
      BcfOrder(['Queen of Oak Bay', 'Queen of Surrey'], '1981', model_find('c_class')),
      BcfOrder(['Queen of New Westminster'], '1964', model_find('nw_class')),
      BcfOrder(['Salish Orca', 'Salish Eagle', 'Salish Raven'], '2016', model_find('salish_class')),
      BcfOrder(['Salish Heron'], '2020', model_find('salish_class')),
      BcfOrder(['Northern Expedition'], '2009', model_find('unclassed')),
      BcfOrder(['Northern Adventure'], '2009', model_find('unclassed')),
      BcfOrder(['Northern Sea Wolf'], '2000', model_find('unclassed')),
      BcfOrder(['Queen of Capilano', 'Queen of Cumberland'], '1991-1992', model_find('i_class')),
      BcfOrder(['Malaspina Sky'], '2008', model_find('i_class')),
      BcfOrder(['Skeena Queen'], '1997', model_find('century_class')),
      BcfOrder(['Quinitsa'], '1977', model_find('q_class')),
      BcfOrder(['Quinsam'], '1982', model_find('q_class')),
      BcfOrder(['Baynes Sound Connector'], '2015', model_find('unclassed')),
      BcfOrder(['Quadra Queen II', 'Tachek'], '1969', model_find('t_class')),
      BcfOrder(['Klitsa', 'Kahloke', 'Kwuna'], '1972-1975', model_find('k_class')),
      BcfOrder(['Kuper'], '1985', model_find('k_class')),
      BcfOrder(["Spirit of Lax Kw' alaams"], '1960', model_find('n_class'))
    ]

def get_order(name):
    for order in bcf_orders:
        if order.contains(name):
            return order
    return None

def all_bcf_orders():
    return bcf_orders
    
def vessel_to_bcf_ferry(vessel_name):
    return BcfFerry(vessel_name, get_order(vessel_name))
    
def create_positions(bcf_vessels, vessel_infos): 
    for bcf_vessel, vessel_info in zip(bcf_vessels, vessel_infos):
        print(f'Generated vessel: {bcf_vessel} {bcf_vessel.order} {vessel_info.status} {vessel_info.destination} {vessel_info.route_number}')
        
    
    