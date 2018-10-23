class SysItem:

    allowed_args = ("name", "volume", "packaging", "percentage", "price", "product_id", "type", "subtype", "subsubtype", "apk", "time")

    def __init__(self, **kwargs):
        self._check_args(**kwargs)
        self.data = kwargs

    def add_data(self, **kwargs):
        self._check_args(**kwargs)
        self.data.update(kwargs)
                
    def _check_args(self, **kwargs):
        for i in kwargs:
            if i not in self.allowed_args:
                raise TypeError("Argument " + i + " not recognised")
            
    def __repr__(self):
        return "SysItem" + str(self.data)

    def __str__(self):
        s = ""
        for i,k in enumerate(sorted(self.data, key=self._arg_sort)):
            if i == 0:
                if k == "name":
                    s = self.data[k]
                    continue
                else:
                    s = "Okänd dryck"
            s += " | " + k + ": " + str(self.data[k])
        return s

    def __lt__(self, other):
        return self.data["apk"] < other.data["apk"]

    def __le__(self, other):
        return self.data["apk"] <= other.data["apk"]

    def __eq__(self, other):
        return self.data["apk"] == other.data["apk"]

    def __ne__(self, other):
        return self.data["apk"] != other.data["apk"]

    def __gt__(self, other):
        return self.data["apk"] > other.data["apk"]

    def __ge__(self, other):
        return self.data["apk"] >= other.data["apk"]

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            if name in self.allowed_args:
                return None
            raise

    def _arg_sort(self, arg):
        return self.allowed_args.index(arg)

    def __getitem__(self, index):
        return self.__getattr__(index)