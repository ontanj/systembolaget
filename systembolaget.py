from selenium import webdriver
from time import sleep
from selenium.common.exceptions import *
import os
from item import SysItem
from cacheresults import CacheResults
from databaseresults import DatabaseResults
import sys
import json


class SysCrawler:
    def __init__(self, browser_path="webdriver/chromedriver", database=False, verbose=0, headless=True):
        self.verbose = verbose
        self._instantiate(browser_path, headless)
        self._verbose("Surfar in på Systembolagets hemsida.", 2)
        self.browser.get("https://www.systembolaget.se/sok-dryck/")
        self._eighteen_or_above()
        self._default_intervals()
        if database:
            self.results = DatabaseResults(database_credentials=(os.environ["DB"], os.environ["DB_USER"], os.environ["DB_PW"]))
        else:
            self.results = CacheResults()

    def _default_intervals(self):
        self.intervals = [0]
        self.intervals.extend(range(10,200,5))
        self.intervals.extend(range(200,2000,20))
        self.intervals.extend(range(2000,52000,2000))

    def set_intervals(self, intervals):
        self.intervals = intervals

    def _instantiate(self, browser_path, headless):
        if headless:
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("headless")
            prefs = {"profile.managed_default_content_settings.images":2}
            chromeOptions.add_experimental_option("prefs",prefs)
        else:
            chromeOptions = None
        self.browser = webdriver.Chrome(executable_path=browser_path, options=chromeOptions)
        
    def _verbose(self, message, level):
        if self.verbose >= level:
            print(message)

    def _eighteen_or_above(self):
        self._verbose("Verifierar över 18 år.", 2)
        self.browser.find_element_by_id("modal-agecheck").find_element_by_class_name("content").find_elements_by_class_name("action")[1].click()

    def goto(self, link):
        self.browser.get(link)

    def start(self):
        self.visited = []
        for i in range(len(self.intervals)-1):
            lower = self.intervals[i]
            upper = self.intervals[i+1]
            self._verbose("\nIndexerar intervallet " + str(lower) + " kr - " + str(upper) + " kr.\n", 1)
            self.interval(lower, upper)
            sleep(3)
            no_items = self.show_all()
            links = self.find_links(no_items)
            num = len(links)
            self._verbose(str(num) + " produkter i intervallet.\n", 1)
            index = 1
            for l in links:
                self.visited.append(l)
                self._verbose("Surfar till " + l, 2)
                try:
                    self.goto(l)
                    si = self._fetch_values()
                except NoSuchElementException as e:
                    self.results.add_error(l)
                    self._verbose("Fel på " + l, 1)
                    self._verbose(str(e), 1)
                    index += 1
                    continue
                self._verbose(str(index) + ": " + si.__str__(), 2)
                self.results.add_item(si)
                index += 1

    
    def interval(self, lower, upper):
        self.goto("https://www.systembolaget.se/sok-dryck/?pricefrom=" + str(lower) + "&priceto=" + str(upper) + "&fullassortment=1")

    def show_more(self):
        self.browser.find_element_by_class_name("cmp-btn--show-more").click()

    def _number_of_items(self):
        amount = self.browser.find_element_by_class_name("all-hits").find_element_by_class_name("ng-binding").text
        amount = amount[1:-1]
        if amount == '':
            return 0
        return int(amount)

    def show_all(self):
        amount = self._number_of_items()
        no_clicks = (amount - 1) // 30
        for i in range(no_clicks):
            self.show_more()
            sleep(3)
        return amount

    def find_links(self, no_items):
        a = self.browser.find_elements_by_tag_name("a")
        drink_links = []
        for link in a:
            path = link.get_attribute("href")
            if isinstance(path, str):
                if path.find("https://www.systembolaget.se/dryck/") != -1:
                    drink_links.append(path)
        return drink_links

    def _fetch_values(self):
        price = self.find_price()
        name, ida = self.find_name_and_id()
        volume, packaging = self.find_volume_and_packaging()
        percentage = self.find_percentage()
        type, subtype, subsubtype = self.find_type()
        apk = self._calculate_apk(percentage, volume, price)
        return SysItem(**{"price": price, "name": name, "product_id": ida, "volume": volume, "packaging": packaging, "percentage": percentage, "type": type, "subtype": subtype, "subsubtype": subsubtype, "apk": apk})

    def find_price(self):
        price = self.browser.find_element_by_class_name("price").text
        index = price.find(":")
        kronor = price[:index]
        try:
            kronor = int(kronor)
        except ValueError:
            kron_val = kronor.split()
            if len(kron_val) > 2:
                raise Exception("För många delar i pris")
            kronor = int(kron_val[0]) * 1000 + int(kron_val[1])
        decimal = price[index+1:]
        try:
            decimal = int(decimal) * 0.01
        except ValueError:
            decimal = 0
        price = kronor + decimal
        return price

    def find_name_and_id(self):
        name = self.browser.find_element_by_class_name("name").text
        separation_index = name.find("Nr")
        product_id = name[(separation_index+3):]
        name = name[:(separation_index-1)]
        return name, product_id

    def find_volume_and_packaging(self):
        volume = self.browser.find_element_by_class_name("packaging").text
        values = volume.split()
        packaging = values[0].strip(",")
        if values[-1] != "ml":
            raise ValueError("Inte milliliter: " + volume)
        volume = int(values[-2])
        return volume, packaging

    
    def _fetch_percentage(self):
        fields = self.browser.find_element_by_id("destopview").text.split(sep="\n")
        found = False
        for field in fields:
            if found:
                return field
            else:
                if field == "Alkoholhalt":
                    found = True

    def find_percentage(self):
        percentage = self._fetch_percentage()
        if percentage == "":
            raise Exception("Inte över 18 år.")
        values = percentage.split()
        if values[-1] != "%":
            raise ValueError("Hittade något annat än alkoholhalt: " + percentage)
        values = values[0].split(sep=",")
        if len(values) != 1:
            if len(values[1]) == 2:
                factor = 0.01
            elif len(values[1]) == 1:
                factor = 0.1
            else:
                raise ValueError("Decimaler i akolholhalt: " + percentage)
            decimals = int(values[1]) * factor
        else:
            decimals = 0
        return int(values[0]) + decimals
        

    def find_type(self):
        types = self.browser.find_element_by_class_name("category").text
        types = types.split(sep=",")
        type = types[0].strip()
        subtype = ""
        subsubtype = ""
        if len(types) >= 2:
            subtype = types[1].strip()
        if len(types) >= 3:
            subsubtype = types[2].strip()
        return type, subtype, subsubtype

    def _calculate_apk(self, percentage, volume, price):
        apk = percentage * volume / price / 100
        apk = round(apk, 3)
        return apk

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of arguments!")
        exit(1)
    sc = SysCrawler()
    sc.start()
    sc.results.sort()
    with open(sys.argv[1], 'w') as file:
        file.write(json.dumps([item.data for item in sc.results], ensure_ascii=False, indent=2))
