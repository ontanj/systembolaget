# Systembolaget

## Beskrivning

Appen bläddrar igenom hela Systembolagets utbud och sparar information om alla produkter. Den räknar även ut alla produkters alkohol per krona [10 µl/kr].

## Förberedelser

### Webdriver

Chromedriver behöver finnas som `./webdriver/chromedriver`. (Detta kan ändras genom att specificera `browser_path` i `SysCrawler`s konstruktor.)

## Körning

Programmet kan köras genom `python3 systembolaget.py output.json`. Då sparas alla produkter i systembolagets sortiment sorterade i filen `output.json`. Det går även konfigurera programmet för att spara datan direkt i en Postgres-databas.

### Exempel

```
from systembolaget import SysCrawler

sc = SysCrawler(verbose=2) # skapa SysCrawler objekt och skriv ut allt som händer
sc.set_intervals([0,5,10,15,20,25,30]) # sök bara efter produkter som kostar mellan 0 och 30 kronor och i intervaller om 5 kronor (för att begränsa minnesanvändningen).
sc.start() # gör sökningen
sc.results.sort() # sortera resultatet
print(sc.results) # visa resultatet
```

### Metoder

#### Konstruktor

##### Attribut

* `browser_path`, anger sökvägen till webdrivern.
* `verbose`, integer `0`-`2`, anger vilka händelser som ska skrivas ut. `0` är default och visar endast en progress bar.
* `database`, boolean, anger om databas en databas ska användas eller om resultaten ska sparas i minnet. Default är `False`.
* `headless`, boolean, anger om webläsarens fönster inte ska visas. Default är `True`.

#### `set_intervals`

Tar emot en ordnad lista som definerar intervallen som sökningen ska göras i.

#### `start`

Kör sökningen.
