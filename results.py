class SysResults:

    def __init__(self, print_length=20):
        self.print_length = print_length
        self.errors = []

    def set_print_length(self, length):
        self.print_length = length

    def add_item(self, item):
        raise NotImplementedError("To be implemented by subclass")

    def sort(sort, key, reverse):
        raise NotImplementedError("To be implemented by subclass")

    def __iter__(self):
        raise NotImplementedError("To be implemented by subclass")

    def __getitem__(self, index):
        raise NotImplementedError("To be implemented by subclass")

    def __repr__(self):
        raise NotImplementedError("To be implemented by subclass")

    def __str__(self):
        raise NotImplementedError("To be implemented by subclass")

    def add_error(self, link):
        self.errors.append(link)