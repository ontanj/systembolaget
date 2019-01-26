import psycopg2
from item import SysItem
from results import SysResults
import time

class DatabaseResults(SysResults):

    def __init__(self, print_length=20, database_credentials=None):
        self.print_length = print_length
        self.set_database(*database_credentials)
        self.time = time.time()
        self.sort_key = "apk"
        self.reverse = False
        self.all_time = False
        super().__init__(print_length=print_length)

    def set_all_time(self, all_time):
        self.all_time = all_time

    def set_database(self, database, user, pw):
        self.conn = psycopg2.connect(database=database, user=user, password=pw, host="localhost")
        self.cur = self.conn.cursor()

    def close_database(self):
        self.cur.close
        self.conn.close

    def add_item(self, item):
        self.cur.execute('insert into products '
                            '(name, product_id, price, volume, percentage, apk, packaging, type, subtype, subsubtype, time) '
                            'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) '
                            'on conflict (product_id) do update set name=%s, price=%s, volume=%s, percentage=%s, '
                            'apk=%s, packaging=%s, type=%s, subtype=%s, subsubtype=%s, time=%s;',
                            (item.name, item.product_id, item.price, item.volume,
                            item.percentage, item.apk, item.packaging, item.type,
                            item.subtype, item.subsubtype, self.time, item.name, item.price, item.volume,
                            item.percentage, item.apk, item.packaging, item.type,
                            item.subtype, item.subsubtype, self.time))
        self.conn.commit()
        return self
    
    def __iter__(self):
        items = self._get_from_database(0)
        for i in items:
            yield i 

    def sort(self, key="apk", reverse=False):
        self.sort_key = key
        self.reverse = reverse

    def __getitem__(self,index):
        items = self._get_from_database(index)
        return items[0]

    def _get_from_database(self, index):
        if self.all_time:
            where = ""
        else:
            where = f"where time = {self.time}"
        if self.reverse:
            if self.sort_key == "apk":
                desc = ""
            else:
                desc = "desc"
        else:
            if self.sort_key == "apk":
                desc = "desc"
            else:
                desc = ""
        fields = ("name", "volume", "packaging", "percentage", "price", "product_id", "type", "subtype", "subsubtype", "apk")
        self.cur.execute('select "name", "volume", "packaging", "percentage", "price", "product_id", "type", "subtype", "subsubtype", "apk" from products ' + where + ' order by ' + self.sort_key + ' ' + desc + ' offset %s limit %s;', (index,self.print_length))
        item_array = []
        rows = self.cur.fetchmany(self.print_length)
        for data in rows:
            d = dict([(fields[i], data[i]) for i in range(len(fields))])
            item_array.append(SysItem(**d))
        return item_array


    def _result_to_item(result):
        return result

    def __repr__(self):
        if self.all_time:
            return "DatabaseResults All-Time"
        else:
            return "DatabaseResults at ({self.time})"

    def __str__(self):
        rows = self._get_from_database(0)
        string = ""
        for (i,item) in enumerate(rows,1):
            string += str(i) + ": " + item.__str__() + "\n"
        if i >= self.print_length:
            string += "och fler...\n"
        return string