import unittest
from item import SysItem

class TestItem(unittest.TestCase):

    def test_create(self):
        v = 3
        key = 'volume'
        s = SysItem(**{key: v})
        self.assertEqual(v, s.data[key])
        
    def test_create_invalid_argument(self):
        self.assertRaises(TypeError,SysItem(),**{'vol': 3})

    def test_add_data_to_empty(self):
        v = 3
        key = 'volume'
        s = SysItem()
        s.add_data(**{key: v})
        self.assertEqual(v, s.data[key])
        
    def test_add_data(self):
        v1 = 3
        k1 = 'volume'
        v2 = 19
        k2 = 'price'
        s = SysItem(**{k1: v1})
        s.add_data(**{k2: v2})
        self.assertEqual(v1, s.data[k1])
        self.assertEqual(v2, s.data[k2])

    def test_string_with_name(self):
        k1 = "name"
        v1 = "Bärs"
        k2 = "volume"
        v2 = 330
        i = SysItem(**{k2: v2, k1: v1})
        self.assertEqual(str(i), f"{v1} | {k2}: {v2}")

    def test_string_without_name(self):
        k = "type"
        v = "ÖL"
        i = SysItem(**{k: v})
        self.assertEqual(str(i), f"Okänd dryck | {k}: {v}")

    def test_compare(self):
        i1 = SysItem(apk=3)
        i2 = SysItem(apk=2, price=10)
        self.assertGreater(i1, i2)

if __name__ == "__main__":
    unittest.main()
