import requests
import json
import sys

# Get the Site ID for the UChicago Dine On Campus Site
def get_site_id(schoolname='uchicago'):
    response = requests.get('https://api.dineoncampus.com/v1/sites/{}/info'.format(schoolname))
    data = response.json()
    site_id = data['site']['id']
    return site_id

# Designate Which Dining Halls to Get Data From
def building_of_interest(building_name, list_of_buildings=['Bartlett Dining Commons', 'Cathey Dining Commons', 'Baker Dining Commons', 'Woodlawn Dining Commons']):
    return building_name in list_of_buildings

# Get Dining Hall IDs for Each Dining Hall; returns a dict mapping dining hall names to their IDs
def get_dining_hall_ids(site_id):
    '''
    site_id: ID of the UChicago Dine On Campus Site

    returns: dict mapping dining hall names to their IDs
    '''
    all_location_url = 'https://api.dineoncampus.com/v1/locations/all_locations?platform=0&site_id={}&for_menus=true&with_address=false&with_buildings=true'.format(site_id)
    response = requests.get(all_location_url)
    data = response.json()
    
    # Extract Building IDs
    building_ids = {}
    for building in data['buildings']:
        for location in building['locations']:
            # Dining Hall must be: (1) in our target and; (2) actively open
            if building_of_interest(location['name']) and location['active']:
                building_ids[location['name']] = location['id']
    return building_ids


# Build Mapping of Dining Hall Names to IDs and to Meal IDs
def get_dining_hall_mappings(dining_hall_ids, date):
    '''
    dining_hall_ids: dict mapping dining hall names to their IDs
    date: date in form YYYY-[M]M-[D]D
    returns: dict mapping dining hall names to their IDs and to meal IDs
    '''
    dining_hall_mappings = {}
    for building_name, building_id in dining_hall_ids.items():
        period_request_url = 'https://api.dineoncampus.com/v1/location/{}/periods?platform=0&date={}'.format(building_id, date)
        data = requests.get(period_request_url).json()
        if not data['closed']:
            dining_hall_mappings[building_name] = {}
            for period in data['periods']:
                if period['name'] == 'Lunch' or period['name'] == 'Dinner':
                    dining_hall_mappings[building_name][period['name']] = period['id']
                dining_hall_mappings[building_name]['location_id'] = building_id
                
    return dining_hall_mappings

# Gets the Kosher Menu for a Specific Dining Hall and Meal
def get_hall_meal_data(meal, dining_hall, date):
    '''
    meal: meal name (e.g. 'Lunch')
    dining_hall: dining hall name (e.g. 'Bartlett Dining Commons')
    date: date in form YYYY-[M]M-[D]D

    returns: dict mapping food names to their descriptions
    '''

    site_id = get_site_id()
    dining_hall_ids = get_dining_hall_ids(site_id)
    dining_hall_mappings = get_dining_hall_mappings(dining_hall_ids, date)
    
    # Get the Location ID
    location_id = dining_hall_mappings[dining_hall]['location_id']

    # Get the Meal ID
    meal_id = dining_hall_mappings[dining_hall][meal]

    # Build the URL
    request_url = "https://api.dineoncampus.com/v1/location/{}/periods/{}?platform=0&date={}".format(location_id, meal_id, date)

    # Get the Data
    data = requests.get(request_url).json()

    # Extract and Return the Kosher Menu
    for category in data['menu']['periods']['categories']:
        if category['name'] == 'Kosher':
            return category['items']

    return None

def filter_kosher_menu(kosher_items):
    '''
    kosher_menu: dict with food names, descriptions, and other irrelevant information

    returns: dict mapping food names to their descriptions, but only for kosher food
    '''
    relevant_items = []
    for item in kosher_data:
        if item['desc'] != None:
            entry = "{}: {}".format(item['name'], item['desc'])
        else:
            entry = item['name']
        relevant_items.append(entry)
    return relevant_items

if __name__ == '__main__':
    '''
    Example Usage:
    python3 getKosherDining.py <date> <dining_hall> <meal>
    python3 getKosherDining.py 2023-5-18 'Baker Dining Commons' 'Lunch'
    '''
    date = sys.argv[1]
    dining_hall = sys.argv[2]
    meal = sys.argv[3]

    kosher_data = get_hall_meal_data(meal, dining_hall, date)
    filtered_kosher_data = filter_kosher_menu(kosher_data)

    print(filtered_kosher_data)


