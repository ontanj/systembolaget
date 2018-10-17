import unittest
from results import SysResults
from item import SysItem

class TestResults(unittest.TestCase):

    def test_create(self):
        s = SysResults()

    def test_add(self):
        r = SysResults()
        i = {"apk": 6, "price": 9}
        si = SysItem(**i)
        r.add_item(si)
        self.assertEqual(r.items[0], si)

    def test_sort_by_apk(self):
        r = SysResults()
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
            self.assertGreater(item.data["apk"], item2)

if __name__ == "__main__":
    unittest.main()