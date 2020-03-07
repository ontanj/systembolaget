# Systembolaget

## Beskrivning

Appen laddar ner hela Systembolagets utbud och räknar ut alla produkters alkohol per krona [10 µl/kr].

## Förberedelse

För att ha tillgång till Systembolagets API behövs en API-nyckel. För att köra programmet ska den finnas som environment variable `export api_key={din nyckel}`.

## Körning

Programmet kan köras genom `python3 systembolaget.py output.json` för att spara alla resultat till `output.json` eller `python3 systembolaget.py` för att skriva ut en topp 10-lista.