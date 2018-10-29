import unittest
from cacheresults import CacheResults
from item import SysItem

class TestCacheResults(unittest.TestCase):

    def test_create(self):
        s = CacheResults()

    def test_add(self):
        r = CacheResults()
        i = {"apk": 6, "price": 9}
        si = SysItem(**i)
        r.add_item(si)
        self.assertEqual(r[0], si)

    def test_sort_by_apk(self):
        r = CacheResults()
        i1 = SysItem(**{"apk": 6, "price": 8})
        i2 = SysItem(**{"apk": 8, "price": 9})
        i3 = SysItem(**{"apk": 4, "price": 10})
        r.add_item(i1).add_item(i2).add_item(i3)
        r.sort(key="apk")
        for index,item in enumerate(r):
            try:
                item2 = r[index+1]
            except IndexError:
                break
            self.assertGreater(item["apk"], item2["apk"])

    def test_sort_by_price(self):
        r = CacheResults()
        i1 = SysItem(**{"apk": 6, "price": 8})
        i2 = SysItem(**{"apk": 8, "price": 5})
        i3 = SysItem(**{"apk": 4, "price": 10})
        r.add_item(i1).add_item(i2).add_item(i3)
        r.sort(key="price")
        for index,item in enumerate(r):
            try:
                item2 = r[index+1]
            except IndexError:
                break
            self.assertLess(item["price"], item2["price"])

if __name__ == "__main__":
    unittest.main()