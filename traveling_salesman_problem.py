
# Imports
from typing import List, Dict
import random, time, math
from itertools import permutations
from map import Map, City
from map import NoCityFoundError, MapIsNotCompleteGraphError

# Create exception for the TSP class
class SolverStopException(Exception): pass
class InvalidStartCityError(Exception): pass
class InvalidMapError(Exception): pass

# TSP (Traveling Salesmen Problem) class
# - This class is a TSP solver, with 3 different algorithm
#   - NN (Nearest Neighbor)  - Not always optimal, but fast
#   - BF (Brute Force)       - Always optimal, but could be very slow
#   - GA (Genetic Algorithm) - Could be optimal and much faster then BF (if there are a lot of cities)
class TSP:

    # Constructor (with map and starting city)
    # - Set the complete map and the name of the starting city
    # - Set estimated remaining time to zero by default
    # - Set stop calculation to false by default
    # - Initial GA solver
    def __init__(self, complete_map: Map, start_city_name: str):
        self.map = complete_map
        self.start_city_name = start_city_name
        self.estimated_remaining_time = 0.0
        self.stop_calculation = False
        self.ga_solver = GA(self.map, self.start_city_name)

    # Nearest Neighbor
    # - Set stop calculation to false
    # - If the starting city is not inside the active cities, then give a InvalidStartCityError
    # - If the map is not complete, then give a InvalidMapError
    # - Start measuring time
    # - If only just one city, then we are done
    # - Always select the nearest not visited city and create a path (Greedy algorithm - Fast)
    #   - Meanwhile calculate the remaining run time
    #   - And check stop variable
    #   - If stop is true, then give a SolverStopException
    # - Reset estimated remaining time
    # - Return with the path (Not always the shortest) and the calculation time
    def nearest_neighbor(self) -> Dict[List[City], float]:
        self.stop_calculation = False
        try: start_city = self.map.get_active_city_by_city_name(self.start_city_name)
        except NoCityFoundError as e: raise InvalidStartCityError(f"Invalid starting city name provided! {e}")
        try: self.map.check_completeness()
        except MapIsNotCompleteGraphError as e: raise InvalidMapError(e)
        start_time = time.time()
        num_active_cities = len(self.map.active_cities)
        if num_active_cities == 1:
            shortest_path = list(self.map.active_cities)
            end_time = time.time()
            calc_time = end_time - start_time
            return {"path": shortest_path, "time": calc_time}
        visited = set()
        path = [start_city]
        visited.add(start_city)
        all_it = num_active_cities
        it_num = 0
        while len(path) < num_active_cities:
            it_num += 1
            act_city = path[-1]
            nearest_city = None
            min_dist = float("inf")
            for city in self.map.active_cities:
                if city not in visited:
                    dist = self.map.get_dist_by_city_names(act_city.name, city.name)
                    if dist.value < min_dist:
                        nearest_city = city
                        min_dist = dist.value
            path.append(nearest_city)
            visited.add(nearest_city)
            act_time = time.time() - start_time
            estimated_run_time = act_time/(it_num+1) * all_it 
            self.estimated_remaining_time = estimated_run_time - act_time
            if self.stop_calculation: 
                self.estimated_remaining_time = 0.0
                raise SolverStopException("The solver stopped!")
        path.append(start_city)
        end_time = time.time()
        self.estimated_remaining_time = 0.0
        calc_time = end_time - start_time 
        return {"path": path, "time": calc_time}
    
    # Brute Force
    # - Set stop calculation to false
    # - If the starting city is not inside the active cities, then give a InvalidStartCityError
    # - If the map is not complete, then give a InvalidMapError
    # - Start measuring time
    # - If only just one city, then we are done
    # - Check all possibilities and calculate the total distances for each (Slow)
    #   - Meanwhile calculate the remaining run time
    #   - And check stop variable
    #   - If stop is true, then give a SolverStopException
    # - Reset estimated remaining time
    # - Return with the path (Always the shortest) and the calculation time
    def brute_force(self) -> Dict[List[City], float]:
        self.stop_calculation = False
        try: start_city = self.map.get_active_city_by_city_name(self.start_city_name)
        except NoCityFoundError as e: raise InvalidStartCityError(f"Invalid starting city name provided! {e}")
        try: self.map.check_completeness()
        except MapIsNotCompleteGraphError as e: raise InvalidMapError(e)
        start_time = time.time()
        active_cities = list(self.map.active_cities)
        if len(active_cities) == 1:
            shortest_path = active_cities
            end_time = time.time()
            calc_time = end_time - start_time
            return {"path": shortest_path, "time": calc_time}
        active_cities.remove(start_city)
        shortest_path = None
        min_distance = float('inf')
        all_it = math.factorial(len(active_cities))
        for it_num, perm in enumerate(permutations(active_cities)):
            path = [start_city] + list(perm) + [start_city]
            total_distance = 0
            for i in range(len(path) - 1):
                dist = self.map.get_dist_by_city_names(path[i].name, path[i + 1].name)
                total_distance += dist.value
            if total_distance < min_distance:
                min_distance = total_distance
                shortest_path = path
            act_time = time.time() - start_time
            estimated_run_time = act_time/(it_num+1) * all_it 
            self.estimated_remaining_time = estimated_run_time - act_time
            if self.stop_calculation: 
                self.estimated_remaining_time = 0.0
                raise SolverStopException("The solver stopped!")
        end_time = time.time()
        self.estimated_remaining_time = 0.0
        calc_time = end_time - start_time
        return {"path": shortest_path, "time": calc_time}
    
    # Genetic Algorithm (with population size, generations and mutation rate)
    # - Try to return with the the solution (Could be the shortest) and the calculation time
    # - If the solver has been stoped, then give a SolverStopException
    # - If the provided start city is not inside the active cities, then give a InvalidStartCityError
    # - If the provided map is not a complete graph, then give a InvalidMapError
    def genetic_algorithm(self, population_size:int=50, generations:int=100, mutation_rate:float=0.01) -> Dict[List[City], float]:
        try: return self.ga_solver.solve(population_size, generations, mutation_rate)
        except SolverStopException: raise SolverStopException("The solver stopped!")
        except InvalidStartCityError as e: raise InvalidStartCityError(e)
        except InvalidMapError as e: raise InvalidMapError(e)

    # Stop solver
    # - Set the stop calculation variable to true
    # - Set the stop calculation variable to true for the GA
    def stop_solver(self):
        self.stop_calculation = True
        self.ga_solver.stop_calculation = True

    # Estimated remaining time getter
    # - Always get the correct Estimated remaining time
    def get_estimated_remaining_time(self):
        if self.estimated_remaining_time > self.ga_solver.estimated_remaining_time:
            return self.estimated_remaining_time 
        else:
            return self.ga_solver.estimated_remaining_time
        
class InvalidProvidedValueError(Exception): pass

# GA (Genetic Algorithm) class
# - This class is a GA solver, which use ...
#   - Total distance as Fitness score
#   - Tournament selection to select parents (individuals)
#   - Crossover to combine genetic information from two parents to produce offspring (new individuals)
#   - Swap mutation to introduce diversity into the population
class GA:

    # Constructor (with map and starting city)
    # - Set the complete map and the name of the starting city
    # - Set estimated remaining time to zero by default
    # - Set stop calculation to false by default
    def __init__(self, complete_map: Map, start_city_name: str) -> None:
        self.map = complete_map
        self.start_city_name = start_city_name
        self.estimated_remaining_time = 0.0
        self.stop_calculation = False

    # Solver (with population size, generations and mutation rate)
    # - If one of provided values is invalid, then give a InvalidProvidedValueError
    # - Set stop calculation to false
    # - If the starting city is not inside the active cities, then give a InvalidStartCityError
    # - If the map is not complete, then give a InvalidMapError
    # - Start measuring time
    # - If only just one city, then we are done
    # - Generate population (random paths)
    # - Iterate through the generations
    #   - Evaluate fitness of each individual in the population (fitness = total distance)
    #   - Select parents for crossover by tournament selection
    #   - Perform crossover to create new generation
    #   - Perform swap mutation
    #   - Create the new population by the new generation
    #   - Calculate the remaining run time
    #   - Check stop variable
    #   - If stop is true, then give a SolverStopException
    # - Select the best individual from the final population
    # - Reset estimated remaining time
    # - Return the best path and the calculation time
    def solve(self, population_size: int, generations: int, mutation_rate: float) -> Dict[List[City], float]:
        if population_size < 2: raise InvalidProvidedValueError("Invalid population size! Population size should be greater than 1!")
        if generations < 0: raise InvalidProvidedValueError("Invalid generation size! Generation size should be positive number!")
        if 0 > mutation_rate or mutation_rate > 1: raise InvalidProvidedValueError("Invalid mutation rate! Mutation rate should be between 0 and 1!")
        self.stop_calculation = False
        try: self.start_city = self.map.get_active_city_by_city_name(self.start_city_name)
        except NoCityFoundError as e: raise InvalidStartCityError(f"Invalid starting city name provided! {e}")
        try: self.map.check_completeness()
        except MapIsNotCompleteGraphError as e: raise InvalidMapError(e)
        start_time = time.time()
        active_cities = list(self.map.active_cities)
        if len(active_cities) == 1:
            shortest_path = active_cities
            end_time = time.time()
            calc_time = end_time - start_time
            return {"path": shortest_path, "time": calc_time}
        population = [self.generate_random_path() for _ in range(population_size)]
        all_it = generations
        for it_num in range(generations):
            fitness_scores = [self.calculate_path_distance(path) for path in population]
            parents = self.select_parents(population, fitness_scores)
            new_generation = self.crossover(parents, population_size)
            for i in range(population_size):
                if random.random() < mutation_rate:
                    new_generation[i] = self.mutate(new_generation[i])
            population = new_generation
            act_time = time.time() - start_time
            estimated_run_time = act_time/(it_num+1) * all_it 
            self.estimated_remaining_time = estimated_run_time - act_time
            if self.stop_calculation: 
                self.estimated_remaining_time = 0.0
                raise SolverStopException()
        best_path = min(population, key=self.calculate_path_distance)
        end_time = time.time()
        self.estimated_remaining_time = 0.0
        calc_time = end_time - start_time 
        return {"path": best_path, "time": calc_time}

    # Generate random path
    # - Collect active cities
    # - Remove the starting city
    # - Create a random path from the active cities (without start city)
    # - return a random path, which start and finish with the start city
    def generate_random_path(self) -> List[City]:
        active_cities = list(self.map.active_cities)
        active_cities.remove(self.start_city)
        random.shuffle(active_cities)
        return [self.start_city] + active_cities + [self.start_city]
    
    # Calculate path distance (with path)
    # - Calculate the total distance for the provided path
    def calculate_path_distance(self, path: List[City]) -> int:
        total_distance = 0
        for i in range(len(path) - 1):
            dist = self.map.get_dist_by_city_names(path[i].name, path[i + 1].name)
            total_distance += dist.value
        return total_distance

    # Select parents (Tournament selection)
    # - Set the tournament size to five (five parents will be compare)
    # - Select the most fit parents from the five racers 
    # - Return with the most fit parents (population size many parents)
    def select_parents(self, population: List[City], fitness_scores: List[int]) -> List[City]:
        tournament_size = 5 if len(population) > 5 else len(population)
        selected_parents = []
        for _ in range(len(population)):
            tournament_indices = random.sample(range(len(population)), tournament_size)
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]
            winner_index = tournament_indices[tournament_fitness.index(min(tournament_fitness))]
            selected_parents.append(population[winner_index])
        return selected_parents

    # Crossover
    # - Select two random parents
    # - The child start with the first "half" of parent1, and finish with parent2 (plus start city)
    # - Return with the created the new generation
    def crossover(self, parents: List[City], population_size: int) -> List[City]:
        new_generation = []
        for _ in range(population_size):
            parent1, parent2 = random.sample(parents, 2)
            crossover_point = random.randint(1, len(parent1) - 1)
            child = parent1[:crossover_point] + [city for city in parent2 if city not in parent1[:crossover_point]] + [parent1[0]]
            new_generation.append(child)
        return new_generation

    # Mutate (Swap mutation)
    # - Swap two elements in the path
    # - Return with the changed path
    def mutate(self, path: List[City]) -> List[City]:
        if len(path) < 4: return path
        index1, index2 = random.sample(range(1, len(path) - 1), 2)
        path[index1], path[index2] = path[index2], path[index1]
        return path
    