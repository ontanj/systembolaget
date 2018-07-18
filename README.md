# Systembolaget

## Beskrivning

Appen bläddrar igenom hela Systembolagets utbud och sparar information om alla produkter i en postgres-databas.  
Den räknar även ut alla produkters alkohol per krona [10 µl/kr].

## Förberedelser

### PostgresQL

```sql
CREATE DATABASE systembolaget;

CREATE TABLE products COLUMNS(
    integer product_id,
    float price,
    varchar name,
    integer volume,
    float percentage,
    integer apk,
    varchar packaging,
    varchar type
)
```

### Webdriver

Chromedriver (eller valfri) behöver finnas i ./webdriver/

### Python

Programmet är skrivet i Python 3. Selenium från PyPi krävs.

## Bakgrund

Detta var mitt första projekt i Python och mitt sätt att lära mig språket.
