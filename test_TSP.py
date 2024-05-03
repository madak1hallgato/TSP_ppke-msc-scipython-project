
import unittest
import threading
from map import Map, City
from traveling_salesman_problem import TSP
from traveling_salesman_problem import SolverStopException, InvalidStartCityError, InvalidMapError
from traveling_salesman_problem import InvalidProvidedValueError

class TestTSP(unittest.TestCase):

    def setUp(self):
        self.city1 = City(name="City1", coord_x=0, coord_y=0)
        self.city2 = City(name="City2", coord_x=3, coord_y=8)
        self.city3 = City(name="City3", coord_x=6, coord_y=7)
        self.city4 = City(name="City4", coord_x=2, coord_y=8)
        self.city5 = City(name="City5", coord_x=7, coord_y=1)
        self.city6 = City(name="City6", coord_x=1, coord_y=3)
        self.city7 = City(name="City7", coord_x=9, coord_y=5)
        self.city8 = City(name="City8", coord_x=7, coord_y=2)
        self.map = Map(self.city1, self.city2, self.city3, self.city4, self.city5, self.city6, self.city7, self.city8)

    def test_nearest_neighbor_0_city(self):
        tsp_solver = TSP(self.map, "City1")
        with self.assertRaises(InvalidStartCityError):
            tsp_solver.nearest_neighbor()

    def test_nearest_neighbor_1_city(self):
        self.map.activate_city("City1")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.nearest_neighbor()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_nearest_neighbor_2_city(self):
        self.map.activate_city("City1")
        self.map.activate_city("City2")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.nearest_neighbor()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_nearest_neighbor_3_city(self):
        self.map.activate_n_random_city(city_num=3, specific_city_name="City1")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.nearest_neighbor()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 4)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_nearest_neighbor_8_city(self):
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.nearest_neighbor()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 9)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_nearest_neighbor_invalid_city(self):
        tsp_solver = TSP(self.map, "City9")
        with self.assertRaises(InvalidStartCityError):
            tsp_solver.nearest_neighbor()

    def test_nearest_neighbor_invalid_map(self):
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        tsp_solver.map.active_cities.add(City(name="City9", coord_x=7, coord_y=2))
        with self.assertRaises(InvalidMapError):
            tsp_solver.nearest_neighbor()

    def test_brute_force_0_city(self):
        tsp_solver = TSP(self.map, "City1")
        with self.assertRaises(InvalidStartCityError):
            tsp_solver.brute_force()

    def test_brute_force_1_city(self):
        self.map.activate_city("City1")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.brute_force()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_brute_force_2_city(self):
        self.map.activate_city("City1")
        self.map.activate_city("City2")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.brute_force()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_brute_force_3_city(self):
        self.map.activate_n_random_city(city_num=3, specific_city_name="City1")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.brute_force()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 4)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_brute_force_8_city(self):
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.brute_force()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 9)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_brute_force_invalid_city(self):
        tsp_solver = TSP(self.map, "City9")
        with self.assertRaises(InvalidStartCityError):
            tsp_solver.brute_force()

    def test_brute_force_invalid_map(self):
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        tsp_solver.map.active_cities.add(City(name="City9", coord_x=7, coord_y=2))
        with self.assertRaises(InvalidMapError):
            tsp_solver.brute_force()

    def test_genetic_algorithm_0_city(self):
        tsp_solver = TSP(self.map, "City1")
        with self.assertRaises(InvalidStartCityError):
            tsp_solver.genetic_algorithm()

    def test_genetic_algorithm_1_city(self):
        self.map.activate_city("City1")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.genetic_algorithm()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_genetic_algorithm_2_city(self):
        self.map.activate_city("City1")
        self.map.activate_city("City2")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.genetic_algorithm()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_genetic_algorithm_3_city(self):
        self.map.activate_n_random_city(city_num=3, specific_city_name="City1")
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.genetic_algorithm()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 4)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_genetic_algorithm_8_city(self):
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        result = tsp_solver.genetic_algorithm()
        path = result["path"]
        time_taken = result["time"]
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), 9)
        self.assertEqual(path[0], path[-1])
        self.assertGreaterEqual(time_taken, 0)

    def test_genetic_algorithm_invalid_city(self):
        tsp_solver = TSP(self.map, "City9")
        with self.assertRaises(InvalidStartCityError):
            tsp_solver.genetic_algorithm()

    def test_genetic_algorithm_invalid_map(self):
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        tsp_solver.map.active_cities.add(City(name="City9", coord_x=7, coord_y=2))
        with self.assertRaises(InvalidMapError):
            tsp_solver.genetic_algorithm()

    def test_genetic_algorithm_invalid_population_size(self):
        tsp_solver = TSP(self.map, "City1")
        with self.assertRaises(InvalidProvidedValueError):
            tsp_solver.genetic_algorithm(population_size=1)

    def test_genetic_algorithm_invalid_generations(self):
        tsp_solver = TSP(self.map, "City1")
        with self.assertRaises(InvalidProvidedValueError):
            tsp_solver.genetic_algorithm(generations=-1)

    def test_genetic_algorithm_invalid_mutation_rate_low(self):
        tsp_solver = TSP(self.map, "City1")
        with self.assertRaises(InvalidProvidedValueError):
            tsp_solver.genetic_algorithm(mutation_rate=-0.1)

    def test_genetic_algorithm_invalid_mutation_rate_high(self):
        tsp_solver = TSP(self.map, "City1")
        with self.assertRaises(InvalidProvidedValueError):
            tsp_solver.genetic_algorithm(mutation_rate=1.1)

    def test_stop_solver(self):
        tsp_solver = TSP(self.map, "City1")
        self.assertFalse(tsp_solver.stop_calculation)
        self.assertFalse(tsp_solver.ga_solver.stop_calculation)
        tsp_solver.stop_solver()
        self.assertTrue(tsp_solver.stop_calculation)
        self.assertTrue(tsp_solver.ga_solver.stop_calculation)

    def test_solver_stop_nearest_neighbor(self):
        for i in range(10): 
            self.map.cities.add(City(name=f"City{i+8}", coord_x=7, coord_y=2))
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        self.exception_in_thread = None
        def run_nearest_neighbor():
            try: 
                tsp_solver.nearest_neighbor()
            except SolverStopException as e:
                self.exception_in_thread = e
        nearest_neighbor_thread = threading.Thread(target=run_nearest_neighbor)
        nearest_neighbor_thread.start()
        tsp_solver.stop_solver()
        nearest_neighbor_thread.join()
        self.assertIsInstance(self.exception_in_thread, SolverStopException)

    def test_solver_stop_brute_force(self):
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        self.exception_in_thread = None
        def run_brute_force():
            try: 
                tsp_solver.brute_force()
            except SolverStopException as e:
                self.exception_in_thread = e
        brute_force_thread = threading.Thread(target=run_brute_force)
        brute_force_thread.start()
        tsp_solver.stop_solver()
        brute_force_thread.join()
        self.assertIsInstance(self.exception_in_thread, SolverStopException)

    def test_solver_stop_genetic_algorithm(self):
        self.map.activate_all()
        tsp_solver = TSP(self.map, "City1")
        self.exception_in_thread = None
        def run_genetic_algorithm():
            try: 
                tsp_solver.genetic_algorithm()
            except SolverStopException as e:
                self.exception_in_thread = e
        genetic_algorithm_thread = threading.Thread(target=run_genetic_algorithm)
        genetic_algorithm_thread.start()
        tsp_solver.stop_solver()
        genetic_algorithm_thread.join()
        self.assertIsInstance(self.exception_in_thread, SolverStopException)

    def test_get_estimated_remaining_time(self):
        tsp_solver = TSP(self.map, "City1")
        tsp_solver.estimated_remaining_time = 10.0
        tsp_solver.ga_solver.estimated_remaining_time = 5.0
        self.assertEqual(tsp_solver.get_estimated_remaining_time(), 10.0)
        tsp_solver.ga_solver.estimated_remaining_time = 15.0
        self.assertEqual(tsp_solver.get_estimated_remaining_time(), 15.0)
        tsp_solver.estimated_remaining_time = 20.0
        self.assertEqual(tsp_solver.get_estimated_remaining_time(), 20.0)

if __name__ == '__main__':
    unittest.main()
