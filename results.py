from item import SysItem

class SysResults:

    def __init__(self):
        self.items = []

    def add_item(self, item):
        if not isinstance(item, SysItem):
            raise TypeError("Not a SysItem.")
        self.items.append(item)
    
    def __iter__(self):
        return iter(self.items)

    def sort(self, key="apk"):
        self.item.sort(key=lambda x: x[key])


    