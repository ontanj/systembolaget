from item import SysItem

class SysResults:

    def __init__(self, print_length=20):
        self.items = []
        self.print_length = print_length

    def set_print_length(self, length):
        self.print_length = length

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

    def __repr__(self):
        return "SysResults" + str(self.items)

    def __str__(self):
        i = 1
        string = ""
        for item in self.items:
            if i > self.print_length:
                break
            string += str(i) + ": " + item.__str__() + "\n"
            i += 1
        diff = len(self.items) - i + 1
        string += "and {diff} stycken till...\n"
        return string