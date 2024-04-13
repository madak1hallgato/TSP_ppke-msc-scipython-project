import json
from complete_map import City, Distance, Map

def load_cities_from_file(file_path: str) -> list:
    with open(file_path, 'r') as file:
        city_coordinates = json.load(file)
    cities = []
    for city_name, coordinates in city_coordinates.items():
        city = City(name=city_name, x_pos=coordinates['x'], y_pos=coordinates['y'])
        cities.append(city)
    return cities

def create_distances(cities: list) -> list:
    distances = []
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            distances.append(Distance(city_a=cities[i], city_b=cities[j]))
    return distances

def create_map(path: str) -> Map:
    cities = load_cities_from_file(path)
    distances = create_distances(cities)
    return Map(*distances)

map = create_map(path='city_coordinates.json')
map.print_cities()
map.print_distances()
