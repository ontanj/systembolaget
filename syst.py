import psycopg2
from multiprocessing import Process
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import *
import os

def eighteen_or_above(browser):
    browser.find_element_by_id("modal-agecheck").find_element_by_class_name("content").find_elements_by_class_name("action")[1].click()

def convert_price(result):
    price = result["price"]
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
    result.update({'price': price})

def separate_name_and_id(result):
    name = result["name"]
    separation_index = name.find("Nr")
    product_id = name[(separation_index+3):]
    name = name[:(separation_index-1)]
    result.update({'name': name, 'product_id': product_id})

def volume_and_package(result):
    volume = result["volume"]
    values = volume.split()
    packaging = values[0].strip(",")
    if values[-1] != "ml":
        raise ValueError("Inte milliliter: " + volume)
    result.update({'volume': int(values[-2]), "packaging": packaging})

def find_percentage(result):
    percentage = result["percentage"]
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
    percentage = int(values[0]) + decimals
    result.update({'percentage': percentage})

def fetch_values(page):
    price = page.find_element_by_class_name("price").text
    name = page.find_element_by_class_name("name").text
    volume = page.find_element_by_class_name("packaging").text
    percentage = page.find_element_by_id("destopview").find_elements_by_tag_name("li")[1].find_element_by_tag_name("p").text
    try:
        typ = page.find_element_by_id("keyword-init-1").text
    except NoSuchElementException:
        typ = page.find_element_by_class_name("category").text
    return {"type": typ, "price": price, "name": name, "volume": volume, "percentage": percentage}

def calculate_apk(values):
    apk = values["percentage"] * values["volume"] / values["price"]
    values.update({'apk': round(apk)})
    return values

def insert_to_database(values):
    conn = psycopg2.connect("dbname=systembolaget user=" + os.environ["DB_USER"] + " password=" + os.environ["DB_PW"] + " host=localhost")
    conn.cursor().execute("insert into products (name, product_id, price, volume, percentage, apk, packaging, type) values (%s, %s, %s, %s, %s, %s, %s, %s) on conflict (product_id) do update set price=%s, apk=%s;", (values["name"], values["product_id"], values["price"], values["volume"], values["percentage"], values["apk"], values["packaging"], values["type"], values["price"], values["apk"]))
    conn.commit()
    conn.close()

def show_more(browser):
    browser.find_element_by_class_name("cmp-btn--show-more").click()

def show_all(browser):
    while True:
        sleep(3)
        try:
            show_more(browser)
        except ElementNotVisibleException as e:
            break

def find_links(page):
    a = page.find_elements_by_tag_name("a")
    drink_links = []
    for link in a:
        path = link.get_attribute("href")
        if isinstance(path, str):
            if path.find("https://www.systembolaget.se/dryck/") != -1:
                drink_links.append(path)
    return drink_links    

def calculate_and_insert(result):
    convert_price(result)
    separate_name_and_id(result)
    volume_and_package(result)
    find_percentage(result)
    calculate_apk(result)
    insert_to_database(result)

def interval(browser, lower, upper):
    browser.get("https://www.systembolaget.se/sok-dryck/?pricefrom=" + str(lower) + "&priceto=" + str(upper) + "&fullassortment=1")

def default_intervals():
    intervals = []
    intervals.extend(range(0,200,5))
    intervals.extend(range(200,2000,20))
    intervals.extend(range(2000,52000,2000))
    return intervals

def browse_intervals(browser, intervals):
    for i in range(len(intervals)-1):
        lower = intervals[i]
        upper = intervals[i+1]
        print("\nIndexerar intervallet " + str(lower) + " kr - " + str(upper) + " kr.")
        interval(browser, lower, upper)
        show_all(browser)
        links = find_links(browser)
        num = len(links)
        print(str(num) + " produkter i intervallet.")
        if num % 30 == 0:
            print("Antalet produkter är jämnt delbart med 30, något kan vara fel. Fortsätter...")
        for l in links:
            try: 
                browser.get(l)
                result = fetch_values(browser)
            except Exception:
                print("Fel på " + l)
                continue
            p = Process(target=calculate_and_insert, args=(result,))
            p.start()    

def browse_all(browser):
    intervals = default_intervals()
    browse_intervals(browser, intervals)
    
def instantiate():
    #browser = webdriver.Firefox(executable_path="webdriver/geckodriver")
    browser = webdriver.Chrome(executable_path="webdriver/chromedriver")
    browser.get("https://www.systembolaget.se/sok-dryck/")
    eighteen_or_above(browser)
    return browser
    
if __name__ == "__main__":
    browser = instantiate()
    browse_all(browser)
