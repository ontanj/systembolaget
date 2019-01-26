import unittest
from databaseresults import DatabaseResults
from item import SysItem
import os
import time

class TestDatabaseResults(unittest.TestCase):

    def test_create(self):
        s = DatabaseResults(database_credentials=(os.environ["DB_TEST"], os.environ["DB_USER"], os.environ["DB_PW"]))

    def test_add(self):
        r = DatabaseResults(database_credentials=(os.environ["DB_TEST"], os.environ["DB_USER"], os.environ["DB_PW"]))
        i = {"apk": 6, "price": 9}
        si = SysItem(**i)
        r.add_item(si)
        self.assertEqual(r[0], si)

    def test_sort_by_apk(self):
        r = DatabaseResults(database_credentials=(os.environ["DB_TEST"], os.environ["DB_USER"], os.environ["DB_PW"]))
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
        r = DatabaseResults(database_credentials=(os.environ["DB_TEST"], os.environ["DB_USER"], os.environ["DB_PW"]))
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