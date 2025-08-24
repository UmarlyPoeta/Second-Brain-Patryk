# 📈 Pandas - DataFrame.drop_duplicates() - Usuwanie duplikatów

## 📚 Co to jest drop_duplicates()?

`drop_duplicates()` to funkcja, która usuwa duplikaty wierszy z DataFrame. To jak sprzątanie szafy - zostawiasz tylko jeden egzemplarz każdej rzeczy! 🧹

## 🔧 Podstawowa składnia

```python
DataFrame.drop_duplicates(
    subset=None,      # kolumny do sprawdzenia
    keep='first',     # który duplikat zachować  
    inplace=False,    # czy zmienić oryginalny DF
    ignore_index=False # czy zresetować indeks
)
```

## 💻 Podstawowe przykłady

```python
import pandas as pd
import numpy as np

# DataFrame z duplikatami
dane = pd.DataFrame({
    'imie': ['Anna', 'Jan', 'Anna', 'Maria', 'Jan', 'Piotr', 'Anna'],
    'wiek': [25, 30, 25, 35, 30, 40, 26],  # Anna ma różne wieki!
    'miasto': ['Warszawa', 'Kraków', 'Warszawa', 'Gdańsk', 'Kraków', 'Poznań', 'Wrocław']
})

print("Dane z duplikatami:")
print(dane)

# Znajdź duplikaty
print(f"\nDuplikaty (wszystkie kolumny):")
print(dane.duplicated())  # True = duplikat

# Usuń duplikaty
bez_duplikatow = dane.drop_duplicates()
print(f"\nBez duplikatów (zachowaj pierwsze):")
print(bez_duplikatow)

# Zachowaj ostatni duplikat
ostatnie = dane.drop_duplicates(keep='last')
print(f"\nZachowaj ostatnie:")
print(ostatnie)

# Usuń WSZYSTKIE duplikaty (nawet oryginał)
zadne = dane.drop_duplicates(keep=False)
print(f"\nUsuń wszystkie (nawet oryginały):")
print(zadne)
```

## 🎯 Praktyczne przypadki

### 📊 Czyszczenie danych klientów

```python
# Symulacja bazy klientów z duplikatami
np.random.seed(42)

klienci_brudne = pd.DataFrame({
    'email': ['anna@email.com', 'jan@email.com', 'anna@email.com', 
              'maria@email.com', 'piotr@email.com', 'jan@email.com',
              'ewa@email.com', 'anna@email.com'],
    'imie': ['Anna', 'Jan', 'Anna', 'Maria', 'Piotr', 'Jan', 'Ewa', 'Anna'],
    'telefon': ['123456789', '987654321', '123456789', '555666777', 
                '111222333', '987654321', '444555666', '999888777'],  # Anna ma różne tel.
    'data_rejestracji': pd.to_datetime(['2023-01-15', '2023-02-20', '2023-01-15',
                                       '2023-03-10', '2023-04-05', '2023-02-20',
                                       '2023-05-12', '2023-06-08'])
})

print("=== CZYSZCZENIE BAZY KLIENTÓW ===")
print("Brudne dane:")
print(klienci_brudne)

# Sprawdź duplikaty różnie
print(f"\nDuplikaty - wszystkie kolumny: {klienci_brudne.duplicated().sum()}")
print(f"Duplikaty - tylko email: {klienci_brudne.duplicated(subset=['email']).sum()}")
print(f"Duplikaty - email + imię: {klienci_brudne.duplicated(subset=['email', 'imie']).sum()}")

# Strategia: email to klucz unikalny
print(f"\nDuplikaty według email:")
email_dups = klienci_brudne[klienci_brudne.duplicated(subset=['email'], keep=False)]
print(email_dups.sort_values('email'))

# Usuń duplikaty email, zachowaj najnowszy
klienci_czyste = klienci_brudne.sort_values('data_rejestracji').drop_duplicates(
    subset=['email'], keep='last'
)

print(f"\nPo czyszczeniu (najnowsze rejestracje):")
print(klienci_czyste.sort_values('email'))

print(f"\nPodsumowanie:")
print(f"Przed: {len(klienci_brudne)} rekordów")
print(f"Po: {len(klienci_czyste)} rekordów") 
print(f"Usunięto: {len(klienci_brudne) - len(klienci_czyste)} duplikatów")
```

### 📈 Dane transakcyjne

```python
# Symulacja błędów w systemie płatności (podwójne transakcje)
transakcje = pd.DataFrame({
    'transaction_id': ['T001', 'T002', 'T001', 'T003', 'T004', 'T002', 'T005'],
    'user_id': ['U123', 'U456', 'U123', 'U789', 'U123', 'U456', 'U999'],
    'kwota': [100.00, 250.50, 100.00, 75.25, 300.00, 250.50, 150.75],
    'timestamp': pd.to_datetime(['2023-01-01 10:00:00', '2023-01-01 11:30:00',
                                '2023-01-01 10:00:01', '2023-01-01 12:15:00',
                                '2023-01-01 13:45:00', '2023-01-01 11:30:02',
                                '2023-01-01 14:20:00']),
    'status': ['SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS', 'SUCCESS']
})

print("=== ANALIZA DUPLIKATÓW TRANSAKCJI ===")
print("Wszystkie transakcje:")
print(transakcje)

# Identyfikuj potencjalne duplikaty
print(f"\nDuplikaty transaction_id:")
tid_dups = transakcje[transakcje.duplicated(subset=['transaction_id'], keep=False)]
print(tid_dups.sort_values('transaction_id'))

# Analiza duplikatów per user + kwota (podejrzane)
user_amount_dups = transakcje[
    transakcje.duplicated(subset=['user_id', 'kwota'], keep=False)
]
print(f"\nPodejrzane: ten sam user + ta sama kwota:")
print(user_amount_dups.sort_values(['user_id', 'kwota', 'timestamp']))

# Strategia czyszczenia: usuń duplikaty transaction_id (zachowaj pierwsze)
transakcje_czyste = transakcje.drop_duplicates(subset=['transaction_id'], keep='first')

print(f"\nPo usunięciu duplikatów transaction_id:")
print(transakcje_czyste.sort_values('timestamp'))

# Podsumowanie finansowe
suma_przed = transakcje['kwota'].sum()
suma_po = transakcje_czyste['kwota'].sum()
print(f"\nWpływ na finanse:")
print(f"Suma przed czyszczeniem: {suma_przed:.2f} PLN")
print(f"Suma po czyszczeniu: {suma_po:.2f} PLN")
print(f"Zaoszczędzono: {suma_przed - suma_po:.2f} PLN (duplikaty)")
```

### 🛒 Analiza produktów e-commerce

```python
# Dane produktów z różnych źródeł (duplikaty z różnymi cenami)
produkty = pd.DataFrame({
    'nazwa': ['iPhone 13', 'Samsung Galaxy', 'iPhone 13', 'MacBook Pro',
              'iPad Air', 'Samsung Galaxy', 'MacBook Pro', 'iPhone 13'],
    'cena': [3999, 2499, 3899, 8999, 2799, 2599, 8999, 4199],
    'sklep': ['Apple Store', 'MediaMarkt', 'x-kom', 'Apple Store',
              'MediaMarkt', 'RTV Euro AGD', 'x-kom', 'MediaExpert'],
    'data_aktualizacji': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-01',
                                        '2023-06-03', '2023-06-02', '2023-06-01',
                                        '2023-06-03', '2023-06-04'])
})

print("=== ANALIZA CEN PRODUKTÓW ===")
print("Wszystkie oferty:")
print(produkty.sort_values(['nazwa', 'cena']))

# Znajdź duplikaty nazw (różne ceny!)
nazwa_dups = produkty[produkty.duplicated(subset=['nazwa'], keep=False)]
print(f"\nProdukty z wieloma ofertami:")
print(nazwa_dups.sort_values(['nazwa', 'cena']))

# Analiza cen per produkt
print(f"\nRóżnice cenowe:")
for nazwa in produkty['nazwa'].unique():
    product_offers = produkty[produkty['nazwa'] == nazwa]
    if len(product_offers) > 1:
        min_price = product_offers['cena'].min()
        max_price = product_offers['cena'].max()
        savings = max_price - min_price
        print(f"{nazwa:15}: {min_price:4.0f} - {max_price:4.0f} PLN (oszczędność: {savings:4.0f})")

# Strategia: zostaw najtańszą ofertę każdego produktu
najtansze = produkty.loc[produkty.groupby('nazwa')['cena'].idxmin()]

print(f"\nNajtańsze oferty:")
print(najtansze.sort_values('cena'))

# Alternatywnie: najnowsze ceny
najnowsze = produkty.sort_values('data_aktualizacji').drop_duplicates(
    subset=['nazwa'], keep='last'
)

print(f"\nNajnowsze ceny:")
print(najnowsze.sort_values('nazwa'))
```

## 🔍 Zaawansowane techniki

### 1️⃣ Duplikaty z tolerancją

```python
# Dane z małymi różnicami (np. błędy zaokrągleń)
dane_numeryczne = pd.DataFrame({
    'id': ['A', 'B', 'A', 'C', 'B'],
    'wartość': [10.00, 20.50, 10.01, 30.75, 20.49],  # małe różnice
    'kategoria': ['X', 'Y', 'X', 'Z', 'Y']
})

print("=== DUPLIKATY Z TOLERANCJĄ ===")
print("Dane z małymi różnicami:")
print(dane_numeryczne)

# Standardowy drop_duplicates nie znajdzie duplikatów
standard = dane_numeryczne.drop_duplicates()
print(f"\nStandardowo (bez zmian): {len(standard)} rekordów")

# Zaokrąglij przed sprawdzeniem duplikatów
dane_rounded = dane_numeryczne.copy()
dane_rounded['wartość_rounded'] = dane_rounded['wartość'].round(0)

duplikaty_rounded = dane_rounded.drop_duplicates(subset=['id', 'wartość_rounded', 'kategoria'])
print(f"\nPo zaokrągleniu: {len(duplikaty_rounded)} rekordów")
print(duplikaty_rounded.drop('wartość_rounded', axis=1))
```

### 2️⃣ Analiza przed usunięciem

```python
def analyze_duplicates(df, subset=None):
    """Szczegółowa analiza duplikatów przed usunięciem"""
    
    print("=== ANALIZA DUPLIKATÓW ===")
    
    # Ogólne info
    total_rows = len(df)
    duplicated_rows = df.duplicated(subset=subset).sum()
    unique_rows = total_rows - duplicated_rows
    
    print(f"Wszystkie wiersze: {total_rows}")
    print(f"Duplikaty: {duplicated_rows} ({duplicated_rows/total_rows:.1%})")
    print(f"Unikalne: {unique_rows} ({unique_rows/total_rows:.1%})")
    
    if duplicated_rows > 0:
        # Pokaż przykłady duplikatów
        print(f"\nPrzykłady duplikatów:")
        dups = df[df.duplicated(subset=subset, keep=False)]
        if subset:
            print(dups.sort_values(subset).head(10))
        else:
            print(dups.head(10))
        
        # Ile grup duplikatów?
        if subset:
            groups = df.groupby(subset).size()
            dup_groups = groups[groups > 1]
            print(f"\nGrup duplikatów: {len(dup_groups)}")
            print(f"Największa grupa: {dup_groups.max()} duplikatów")
    
    return {
        'total': total_rows,
        'duplicates': duplicated_rows,
        'unique': unique_rows,
        'dup_percentage': duplicated_rows/total_rows
    }

# Test na danych klientów
stats = analyze_duplicates(klienci_brudne, subset=['email'])
```

## ⚠️ Częste problemy

```python
print("=== CZĘSTE PROBLEMY ===")

# 1. Zapomnienie o subset
df_test = pd.DataFrame({
    'id': [1, 2, 1, 3],
    'name': ['A', 'B', 'A', 'C'],
    'value': [10, 20, 15, 30]  # różne wartości dla id=1
})

print("1. Problem z subset:")
print("Dane:")
print(df_test)

print(f"\nBez subset - nie znajdzie duplikatów:")
print(df_test.drop_duplicates())  # różne wartości -> nie duplikat

print(f"\nZ subset=['id'] - znajdzie:")  
print(df_test.drop_duplicates(subset=['id']))

# 2. Resetowanie indeksu
print(f"\n2. Problem z indeksem:")
df_with_gaps = df_test.drop_duplicates(subset=['id'])
print("Indeks z lukami:")
print(df_with_gaps)

print("Po reset_index:")
print(df_with_gaps.reset_index(drop=True))

# Lub od razu:
clean_df = df_test.drop_duplicates(subset=['id'], ignore_index=True)
print("Z ignore_index=True:")
print(clean_df)
```

## 📝 Podsumowanie

`drop_duplicates()` to niezbędne narzędzie data cleaningu:

- 🧹 Usuwa identyczne wiersze z DataFrame
- 🎯 `subset=` określa kolumny do porównania
- 🔄 `keep='first'/'last'/False` kontroluje które duplikaty zachować
- 📊 `inplace=True` modyfikuje oryginalny DataFrame
- 🔢 `ignore_index=True` resetuje indeks automatycznie
- ⚠️ Zawsze analizuj duplikaty przed usunięciem
- 💡 Może być częścią większego procesu ETL

To jak Marie Kondo dla danych - zostaw tylko to, co potrzebne! ✨🧹