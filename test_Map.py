
import unittest
from map import Map, City
from map import NoCityFoundError, NoDistanceFoundError
from map import InvalidCityActivationError, InvalidCityDeactivationError

class TestMap(unittest.TestCase):

    def setUp(self):
        self.city1 = City(name="City1", coord_x=0, coord_y=0)
        self.city2 = City(name="City2", coord_x=3, coord_y=4)
        self.city3 = City(name="City3", coord_x=6, coord_y=8)
        self.map = Map(self.city1, self.city2, self.city3)

    def test_init(self):
        result = self.map
        self.assertEqual(len(result.cities), 3)
        self.assertEqual(len(result.active_cities), 0)
        self.assertEqual(len(result.distances), 0)

    def test_get_city_by_city_name(self):
        result = self.map.get_city_by_city_name("City1")
        self.assertEqual(result, self.city1)

    def test_get_city_by_invalid_city_name(self):
        with self.assertRaises(NoCityFoundError):
            self.map.get_city_by_city_name("City4")

    def test_get_active_city_by_active_city_name(self):
        self.map.activate_city("City1")
        result = self.map.get_active_city_by_city_name("City1")
        self.assertEqual(result, self.city1)

    def test_get_active_city_by_invalid_city_name(self):
        self.map.activate_all()
        with self.assertRaises(NoCityFoundError):
            self.map.get_active_city_by_city_name("City4")

    def test_get_active_city_by_inactive_city_name(self):
        with self.assertRaises(NoCityFoundError):
            self.map.get_active_city_by_city_name("City1")

    def test_get_dist_by_city_names(self):
        self.map.activate_all()
        result = self.map.get_dist_by_city_names("City1", "City2")
        self.assertEqual(result.value, 5.0)

    def test_get_dist_by_invalid_city_names(self):
        self.map.activate_all()
        with self.assertRaises(NoDistanceFoundError):
            self.map.get_dist_by_city_names("City1", "City4")
    
    def test_get_dist_by_inactive_city_names(self):
        self.map.activate_all()
        self.map.deactivate_city("City2")
        with self.assertRaises(NoDistanceFoundError):
            self.map.get_dist_by_city_names("City1", "City2")
    
    def test_get_dist_by_same_city_names(self):
        self.map.activate_all()
        with self.assertRaises(NoDistanceFoundError):
            self.map.get_dist_by_city_names("City1", "City1")

    def test_activate_city(self):
        self.map.deactivate_all()
        self.map.activate_city("City1")
        self.assertIn(self.city1, self.map.active_cities)

    def test_activate_active_city(self):
        self.map.activate_all()
        self.map.activate_city("City1")
        self.assertIn(self.city1, self.map.active_cities)

    def test_activate_invalid_city(self):
        with self.assertRaises(InvalidCityActivationError):
            self.map.activate_city("City4")

    def test_deactivate_city(self):
        self.map.activate_all()
        self.map.deactivate_city("City1")
        self.assertNotIn(self.city1, self.map.active_cities)

    def test_deactivate_invalid_city(self):
        self.map.activate_all()
        with self.assertRaises(InvalidCityDeactivationError):
            self.map.deactivate_city("City4")
    
    def test_deactivate_inactive_city(self):
        self.map.activate_all()
        self.map.deactivate_city("City1")
        with self.assertRaises(InvalidCityDeactivationError):
            self.map.deactivate_city("City1")

    def test_activate_n_random_city(self):
        self.map.activate_n_random_city(1)
        self.assertEqual(len(self.map.active_cities), 1)

    def test_activate_zero_random_city(self):
        self.map.activate_n_random_city(0)
        self.assertEqual(len(self.map.active_cities), 1)

    def test_activate_five_random_city(self):
        self.map.activate_n_random_city(5)
        self.assertEqual(len(self.map.active_cities), len(self.map.cities))

    def test_check_completeness(self):
        self.map.activate_all()
        self.assertTrue(self.map.check_completeness())

if __name__ == "__main__":
    unittest.main()
