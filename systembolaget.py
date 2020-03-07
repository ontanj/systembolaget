import os
import sys
import json
import requests

class APKounter:

    def go(self):
        req_string = "https://api-extern.systembolaget.se/product/v1/product"
        products = requests.get(req_string, headers={"Ocp-Apim-Subscription-Key":os.environ["api_key"]}).json()
        self.products = [{**item, "apk": self._calculate_apk(item)} for item in products if not item["IsCompletelyOutOfStock"] and not item["IsTemporaryOutOfStock"]]
        self.products.sort(key=lambda item: item["apk"], reverse=True)

    def stringify(self, index):
        string = self.products[index]["ProductNameBold"]
        if self.products[index]["ProductNameThin"]:
            string += " - " + self.products[index]["ProductNameThin"]
        string += f', {int(self.products[index]["Volume"])} ml, {self.products[index]["AlcoholPercentage"]} %, {self.products[index]["Price"]} kr, {self.products[index]["BeverageDescriptionShort"]}'
        return string

    def _calculate_apk(self, item):
        if item["Price"] == 0.0:
            return 0.0
        apk = item["AlcoholPercentage"] * item["Volume"] / item["Price"] / 100
        return round(apk, 3)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Error: Wrong number of arguments.", file=sys.stderr)
    apk = APKounter()
    apk.go()
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'w') as file:
            file.write(json.dumps(apk.products, ensure_ascii=False, indent=2))
        print(f'Successfully saved {len(apk.products)} entries to {sys.argv[1]}!')
    else:
        for index in range(0,10):
            print(str(index+1) + ": " + apk.stringify(index))

