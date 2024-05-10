
import unittest, os, json
from map import MapFileManager

class TestMapFileManager(unittest.TestCase):

    def setUp(self):
        self.test_file_path = "test_cities.json"
        with open(self.test_file_path, 'w') as f:
            data = {"A": {"x": 1, "y": 2}, "B": {"x": 3, "y": 4}}
            json.dump(data, f)

    def tearDown(self):
        os.remove(self.test_file_path)

    def test_invalid_path(self):
        invalid_path = "invalid_map.json"
        with self.assertRaises(FileNotFoundError):
            with MapFileManager(file_path=invalid_path) as _: pass

    def test_invalid_json_format(self):
        invalid_format_path = "invalid_format_map.json"
        with open(invalid_format_path, 'w') as file:
            file.write("invalid_json_content")
        with self.assertRaises(ValueError):
            with MapFileManager(file_path=invalid_format_path) as map_file_manager:
                map_file_manager.create_map_from_file()
        os.remove(invalid_format_path)

    def test_enter(self):
        with MapFileManager(file_path=self.test_file_path) as map_file_manager:
            self.assertIsInstance(map_file_manager, MapFileManager)
            self.assertFalse(map_file_manager.map_file.closed)

    def test_exit(self):
        map_file_manager = MapFileManager(file_path=self.test_file_path)
        with map_file_manager: pass
        self.assertTrue(map_file_manager.map_file.closed)
        
    def test_create_map_from_file_and_get_map(self):
        with MapFileManager(file_path=self.test_file_path) as map_file_manager:
            map_file_manager.create_map_from_file()
            result = map_file_manager.get_map()
        self.assertIsNotNone(result)
        self.assertEqual(len(result.cities), 2)

    def test_get_map_with_and_without_create(self):
        with MapFileManager(file_path=self.test_file_path) as map_file_manager:
            result_without = map_file_manager.get_map()
        self.assertIsNotNone(result_without)
        self.assertEqual(len(result_without.cities), 2)

if __name__ == "__main__":
    unittest.main()
