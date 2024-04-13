from dataclasses import dataclass, field
import math

@dataclass(frozen=True)
class City:
    name: str
    x_pos: float
    y_pos: float

@dataclass(frozen=True)
class Distance:
    city_a: City
    city_b: City
    value: float = field(init=False)
    def __post_init__(self):
        object.__setattr__(self, 'value', math.dist(
            [self.city_a.x_pos, self.city_a.y_pos], 
            [self.city_b.x_pos, self.city_b.y_pos]))

class Map:
    def __init__(self, *distances: Distance):
        self.cities = set()
        self.distances = set()
        for dist in distances:
            self.add_dist(dist)

    def add_dist(self, dist: Distance):
        self.cities.add(dist.city_a)
        self.cities.add(dist.city_b)
        self.distances.add(dist)

    def get_city_by_name(self, c_name: str) -> City:
        target_city = next((city for city in self.cities if city.name == c_name), None)
        if target_city == None:
            print("W - No city found with the name of", c_name, "! - Return None!")
        return target_city
    
    def get_dist_value_by_city_names(self, c_name_a: str, c_name_b: str) -> float:
        city_a = self.get_city_by_name(c_name=c_name_a)
        city_b = self.get_city_by_name(c_name=c_name_b)
        if city_a is not None and city_b is not None:
            for dist in self.distances:
                if (dist.city_a == city_a and dist.city_b == city_b) or (dist.city_a == city_b and dist.city_b == city_a): 
                    return dist.value
        print("W - No distance found between", c_name_a, "and", c_name_b, "! - Return 0.0 as distance!")
        return 0.0
        
    def clear_all(self):
        self.cities = set()
        self.distances = set()

    def print_cities(self):
        for city in self.cities: 
            print(city.name)
            print(" - x =", city.x_pos)
            print(" - y =", city.y_pos)

    def print_distances(self):
        for dist in self.distances:
            print(dist.city_a.name, "-", dist.city_b.name)
            print(" - dist:", dist.value)
