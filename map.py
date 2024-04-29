
# Imports
from typing_extensions import Self
from dataclasses import dataclass, field
import numpy as np
import json

# Create exception for the Map class
class NoCityFoundError(Exception): pass
class NoDistanceFoundError(Exception): pass
class InvalidCityActivationError(Exception): pass
class InvalidCityDeactivationError(Exception): pass

# City data class
# - This data class store the city name and the coordinates
@dataclass(frozen=True)
class City:
    name: str
    coord_x: float
    coord_y: float

# Distance data class
# - This data class store the distance between two cities
# - Where the distance calculate automatically between the two provided cities
@dataclass(frozen=True)
class Distance:
    city_a: City
    city_b: City
    value: float = field(init=False)
    def __post_init__(self) -> None:
        a_coords = np.array([self.city_a.coord_x, self.city_a.coord_y])
        b_coords = np.array([self.city_b.coord_x, self.city_b.coord_y])
        object.__setattr__(self, 'value', np.linalg.norm(a_coords - b_coords))

# Map class
# - This class is a complete graph
# - Where the active cities are the vertecies
# - And the distances (between active cities) are the edges
class Map:

    # Constructor (with cities)
    # - Fill cities with the provided cities
    # - Create an empty set for active cities
    # - Create an empty set for distances (between active cities)
    def __init__(self, *cities: City) -> None:
        self.cities = {city for city in cities}
        self.active_cities = set()
        self.distances = set()

    # City getter (by name)
    # - Try to find the city (from all cities)
    # - If no match, then give a NoCityFoundError
    # - Else return with the desired city
    def get_city_by_city_name(self, city_name: str) -> City:
        target_city = next((city for city in self.cities if city.name == city_name), None)
        if target_city == None: 
            raise NoCityFoundError(f"No city found with the name '{city_name}'!")
        return target_city

    # Active city getter (by name)
    # - Try to find the city (from active cities)
    # - If no match, then give a NoCityFoundError
    # - Else return with the desired active city
    def get_active_city_by_city_name(self, active_city_name: str) -> City:
        target_active_city = next((active_city for active_city in self.active_cities if active_city.name == active_city_name), None)
        if target_active_city == None: 
            raise NoCityFoundError(f"No active city found with the name '{active_city_name}'!")
        return target_active_city
    
    # Distance getter (by two city names)
    # - Try to find the cities (from active cities)
    # - If no match for one of the cities, then give a NoDistanceFoundError
    # - Else try to find a distance, where the cities are equals to the provided cities
    # - If no distance found, then give a NoDistanceFoundError 
    def get_dist_by_city_names(self, active_city_name_a: str, active_city_name_b: str) -> Distance:
        try:
            city_a = self.get_active_city_by_city_name(active_city_name=active_city_name_a)
            city_b = self.get_active_city_by_city_name(active_city_name=active_city_name_b)
        except NoCityFoundError as e:
            error = f"No distance found between '{active_city_name_a}' and '{active_city_name_b}'!"
            trigger = f"Invalid active city name provided! {e}"
            raise NoDistanceFoundError(error, trigger)
        for dist in self.distances:
            if {dist.city_a, dist.city_b} == {city_a, city_b}: 
                return dist
        raise NoDistanceFoundError(f"No distance found between '{active_city_name_a}' and '{active_city_name_b}'!")
    
    # Activate a city (by name)
    # - Try to find the city (from all cities)
    # - If no match, then give a InvalidCityActivationError
    # - Else add the city to the active cities set
    # - Then create distances between the new active city and the active cities
    def activate_city(self, city_name: str) -> None:
        try: 
            target_city = self.get_city_by_city_name(city_name=city_name)
        except NoCityFoundError as e:
            error = f"Cannot be activated the city with the name'{city_name}'!"
            trigger = f"Invalid city name provided! {e}"
            raise InvalidCityActivationError(error, trigger)
        self.active_cities.add(target_city)
        for active_city in self.active_cities:
            if active_city != target_city:
                new_dist = Distance(city_a=active_city, city_b=target_city)
                self.distances.add(new_dist)

    # Deactivate a city (by name)
    # - Try to find the city (from active cities)
    # - If no match, then give a InvalidCityDeactivationError
    # - Else remove the city from the active cities set
    # - Then remove the distances between the removed active city and the remaining active cities
    def deactivate_city(self, active_city_name: str) -> None:
        try: 
            target_active_city = self.get_active_city_by_city_name(active_city_name=active_city_name)
        except NoCityFoundError as e:
            error = f"Cannot be deactivated the city with the name'{active_city_name}'!"
            trigger = f"Invalid active city name provided! {e}"
            raise InvalidCityDeactivationError(error, trigger)
        self.active_cities.remove(target_active_city)
        target_distances = {dist for dist in self.distances if target_active_city in {dist.city_a, dist.city_b}}
        self.distances -= target_distances

    # Activate all cities
    # - Collect the city names (from all cities)
    # - Then call the activate function for each city name
    def activate_all(self) -> None:
        city_names = [city.name for city in self.cities]
        for city_name in city_names:
            self.activate_city(city_name=city_name)

    # Activate all cities
    # - Collect the active city names (from active cities)
    # - Then call the deactivate function for each active city name
    def deactivate_all(self) -> None:
        active_city_names = [active_city.name for active_city in self.active_cities]
        for active_city_name in active_city_names: 
            self.deactivate_city(active_city_name=active_city_name)

    # Activate n random city (where n is the number of cities to activate)
    # - Collect the city names (from all cities)
    # - Check the given city number is smaller (or equal) then zero
    # - If it is smaller or equal, then the city number will be one
    # - Check the given city number is greater then the all cities size
    # - If it is greater, then the city number will be equal to the size of the cities set
    # - Then call the activate function for each city name
    def activate_n_random_city(self, city_num: int) -> None:
        all_city_name = [city.name for city in self.cities]
        if city_num <= 0:
            print("activate_n_random_city - W: city_num is smaller (or equal) then zero -> city_num = 1")
            city_num = 1
        if city_num > len(all_city_name):
            print("activate_n_random_city - W: city_num is greater then the number of the cities -> city_num = number of the cities")
            city_num = len(all_city_name)
        for i in range(city_num):
            self.activate_city(city_name=all_city_name[i])

    # Check completeness
    # - Check distance between active cities one-by-one
    # - If there are distances between all active cities then return True
    # - Else return False
    def check_completeness(self) -> bool:
        for city_a in self.active_cities:
            for city_b in self.active_cities:
                if city_a != city_b:
                    try:
                        self.get_dist_by_city_names(city_a.name, city_b.name)
                    except NoDistanceFoundError:
                        return False
        return True

    # Print cities
    # - It print the details of the cities to the console
    def print_cities(self) -> None:
        for city in self.cities:
            print(city.name)
            print(" - x =", city.coord_x)
            print(" - y =", city.coord_y)

    # Print active cities
    # - It print the details of the active cities to the console
    def print_active_cities(self) -> None:
        for active_city in self.active_cities:
            print(active_city.name)
            print(" - x =", active_city.coord_x)
            print(" - y =", active_city.coord_y)

    # Print distances
    # - It print the details of the distances to the console
    def print_distances(self) -> None:
        for dist in self.distances:
            print(dist.city_a.name, "-", dist.city_b.name)
            print(" - dist:", dist.value)

# Map File Manager class
# - This context manager is ...
#   - Open a map json file
#   - Can create a map from the file
#   - Then close the file when exit
class MapFileManager:

    # Constructor (with file path)
    # - Store the file path in a class variable
    # - And set the map file, map class variables to none
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.map_file = None
        self.map = None

    # Enter
    # - Open the json file (always in read mode)
    # - And return whith this class (the user can call the functions of this class)
    def __enter__(self) -> Self:
        self.map_file = open(self.file_path, mode='r')
        return self
    
    # Exit
    # - Close the map file when exit
    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.map_file.close()
        
    # Create map (from file)
    # - Load the json file
    # - Create cities by the values of the map file
    # - Create a map by the created cities
    def create_map_from_file(self) -> None:
        cities = []
        city_coordinates = json.load(self.map_file)
        for city_name, coords in city_coordinates.items():
            city = City(name=city_name, coord_x=coords['x'], coord_y=coords['y'])
            cities.append(city)
        self.map = Map(*cities)
    
    # Map getter
    # - Return with the map
    # - If the map is None, then create the map
    def get_map(self) -> Map:
        if self.map == None:
            print("get_map - W: No map found -> Creat map from file")
            self.create_map_from_file()
        return self.map
