# Kosher Dining Menu Information

This Python script allows you to fetch Kosher menu information from various dining halls at The University of Chicago. The script uses the Dine On Campus API to retrieve this information.

## Usage

Command-line usage:

```bash
python3 getKosherDining.py <date> <dining_hall> <meal>
```

Example:

```bash
python3 getKosherDining.py 2023-5-18 'Baker Dining Commons' 'Lunch'
```

Where:
- `<date>` should be in the format `YYYY-[M]M-[D]D` (e.g., `2023-5-18`).
- `<dining_hall>` is the name of the dining hall (e.g., 'Baker Dining Commons').
- `<meal>` is the meal name (e.g., 'Lunch' or 'Dinner').

## Functions

The script includes the following key functions:

- `get_site_id(schoolname='uchicago')` : Get the Site ID for the UChicago Dine On Campus Site.

- `building_of_interest(building_name, list_of_buildings)` : Designate which dining halls to get data from.

- `get_dining_hall_ids(site_id)` : Get Dining Hall IDs for each dining hall.

- `get_dining_hall_mappings(dining_hall_ids, date)` : Build a mapping of Dining Hall Names to IDs and to Meal IDs.

- `get_hall_meal_data(meal, dining_hall, date)` : Get the Kosher Menu for a specific Dining Hall and Meal.

- `filter_kosher_menu(kosher_items)` : Filter the kosher menu for relevant items.

## Dependencies

- `requests`: To make HTTP requests to the Dine On Campus API.
- `json`: To parse the JSON response from the Dine On Campus API.
- `sys`: To handle command-line arguments.

Install these with pip:

```bash
pip install requests
```

Please note that this script is intended for educational purposes and adheres to the terms of use of the Dine On Campus API.
