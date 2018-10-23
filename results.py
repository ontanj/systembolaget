from item import SysItem

class SysResults:

    def __init__(self):
        self.items = []

    def add_item(self, item):
        if not isinstance(item, SysItem):
            raise TypeError("Not a SysItem.")
        self.items.append(item)
        return self
    
    def __iter__(self):
        return iter(self.items)

    def sort(self, key="apk", reverse=False):
        if key == "apk":
            reverse = not reverse
        self.items.sort(key=lambda x: x[key], reverse=reverse)

    def __getitem__(self,index):
        return self.items[index]


    