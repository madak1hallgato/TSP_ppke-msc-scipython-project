import random

from map import MapFileManager
from traveling_salesman_problem import TSP

with MapFileManager(file_path="cities.json") as map_file_manager:
    map_file_manager.create_map_from_file()
    complete_map = map_file_manager.get_map()

city_num = random.randint(2, 9)
complete_map.activate_n_random_city(city_num=city_num, specific_city_name="New York")

tsp_solver = TSP(complete_map=complete_map, start_city_name="New York")

result_nn = tsp_solver.nearest_neighbor()
solution_nearest_neighbor = result_nn["path"]
time_nearest_neighbor = result_nn["time"]
if solution_nearest_neighbor:
    print("Nearest Neighbor solution:")
    print(' -> '.join(city.name for city in solution_nearest_neighbor))
    print(f"Time: {time_nearest_neighbor:.2f} seconds")
else: print("No NN solution found.")

result_bf = tsp_solver.brute_force()
solution_brute_force = result_bf["path"]
time_brute_force = result_bf["time"]
if solution_brute_force:
    print("Brute Force solution:")
    print(' -> '.join(city.name for city in solution_brute_force))
    print(f"Time: {time_brute_force:.2f} seconds")
else: print("No BF solution found.")

result_ga = tsp_solver.genetic_algorithm(population_size=150, generations=150, mutation_rate=0.01)
solution_genetic_algorithm = result_ga["path"]
time_genetic_algorithm = result_ga["time"]
if solution_genetic_algorithm:
    print("Genetic Algorithm solution:")
    print(' -> '.join(city.name for city in solution_genetic_algorithm))
    print(f"Time: {time_genetic_algorithm:.2f} seconds")
else: print("No GA solution found.")
