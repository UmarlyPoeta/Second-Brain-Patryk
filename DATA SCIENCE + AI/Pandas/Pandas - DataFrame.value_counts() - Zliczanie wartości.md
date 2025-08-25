# 📊 Pandas - DataFrame.value_counts() - Zliczanie wartości

## 📚 Co to jest value_counts()?

`value_counts()` to funkcja, która liczy ile razy występuje każda unikalna wartość w Series lub kolumnie DataFrame. To jak automatyczny licznik głosów - pokazuje popularność każdej opcji! 🗳️📊

## 🔧 Podstawowa składnia

```python
# Dla Series
Series.value_counts(
    normalize=False,    # czy pokazać proporcje zamiast liczb
    sort=True,         # czy sortować wyniki  
    ascending=False,   # kolejność sortowania
    dropna=True        # czy ignorować NaN
)

# Dla DataFrame (jedna kolumna)
DataFrame['column'].value_counts()
```

## 💻 Praktyczne przykłady

### 1️⃣ Podstawowe zliczanie

```python
import pandas as pd
import numpy as np

# Dane o produktach
produkty = pd.Series(['Laptop', 'Telefon', 'Laptop', 'Tablet', 'Telefon', 
                     'Laptop', 'Słuchawki', 'Telefon', 'Tablet', 'Laptop'])

print("Lista produktów:")
print(produkty)

# Zlicz wystąpienia
liczby = produkty.value_counts()
print(f"\nLiczby produktów:")
print(liczby)

# Z procentami
procenty = produkty.value_counts(normalize=True)
print(f"\nProporcje produktów:")
print(procenty)

# W porcentach (pomnóż przez 100)
procenty_100 = (produkty.value_counts(normalize=True) * 100).round(1)
print(f"\nProcenty produktów:")
for produkt, proc in procenty_100.items():
    print(f"{produkt}: {proc}%")
```

### 2️⃣ Różne opcje sortowania

```python
# Dane ocen
oceny = pd.Series([5, 4, 3, 5, 4, 5, 2, 4, 3, 5, 4, 5, 1, 3, 4])

print("Oceny:", oceny.tolist())

# Domyślnie - malejąco według częstości
domyslne = oceny.value_counts()
print(f"\nDomyślnie (malejąco według częstości):")
print(domyslne)

# Rosnąco według częstości
rosnaco = oceny.value_counts(ascending=True)
print(f"\nRosnąco według częstości:")
print(rosnaco)

# Bez sortowania (kolejność wystąpienia)
bez_sort = oceny.value_counts(sort=False)
print(f"\nBez sortowania:")
print(bez_sort)

# Posortowane według indeksu (wartości ocen)
sort_index = oceny.value_counts().sort_index()
print(f"\nPosortowane według ocen:")
print(sort_index)
```

### 3️⃣ Obsługa wartości NaN

```python
# Dane z brakującymi wartościami
miasto = pd.Series(['Warszawa', 'Kraków', np.nan, 'Gdańsk', 'Warszawa', 
                   np.nan, 'Kraków', 'Poznań', 'Warszawa'])

print("Miasta z NaN:")
print(miasto)

# Domyślnie - ignoruj NaN
bez_nan = miasto.value_counts()
print(f"\nBez NaN (domyślnie):")
print(bez_nan)

# Uwzględnij NaN
z_nan = miasto.value_counts(dropna=False)
print(f"\nZ NaN:")
print(z_nan)

# Policz tylko NaN
liczba_nan = miasto.isna().sum()
print(f"\nLiczba NaN: {liczba_nan}")
```

## 🎯 Praktyczne przypadki użycia

### 📊 Analiza ankiety klientów

```python
# Symulacja odpowiedzi ankiety
np.random.seed(42)
n_respondents = 1000

ankieta_data = pd.DataFrame({
    'wiek_grupa': np.random.choice(['18-25', '26-35', '36-45', '46-60', '60+'], n_respondents, 
                                  p=[0.15, 0.25, 0.25, 0.25, 0.1]),
    'wykształcenie': np.random.choice(['Podstawowe', 'Średnie', 'Wyższe'], n_respondents,
                                     p=[0.1, 0.4, 0.5]),
    'zadowolenie': np.random.choice(['Bardzo zadowolony', 'Zadowolony', 'Neutralny', 
                                    'Niezadowolony', 'Bardzo niezadowolony'], n_respondents,
                                   p=[0.3, 0.4, 0.2, 0.08, 0.02]),
    'miasto_typ': np.random.choice(['Duże miasto', 'Średnie miasto', 'Małe miasto', 'Wieś'], 
                                  n_respondents, p=[0.3, 0.25, 0.25, 0.2])
})

print(f"Ankieta - {len(ankieta_data)} respondentów")
print("\nRozkład grup wiekowych:")
print(ankieta_data['wiek_grupa'].value_counts())

print("\nWykształcenie (z procentami):")
wyksztalcenie_stats = ankieta_data['wykształcenie'].value_counts()
for level, count in wyksztalcenie_stats.items():
    procent = count / len(ankieta_data) * 100
    print(f"{level}: {count} ({procent:.1f}%)")

print("\nZadowolenie klientów:")
zadowolenie = ankieta_data['zadowolenie'].value_counts()
print(zadowolenie)

# Zadowoleni vs niezadowoleni
zadowoleni = zadowolenie[['Bardzo zadowolony', 'Zadowolony']].sum()
niezadowoleni = zadowolenie[['Niezadowolony', 'Bardzo niezadowolony']].sum()
print(f"\nPodsumowanie:")
print(f"Zadowoleni: {zadowoleni} ({zadowoleni/len(ankieta_data)*100:.1f}%)")
print(f"Niezadowoleni: {niezadowoleni} ({niezadowoleni/len(ankieta_data)*100:.1f}%)")
```

### 🏥 Analiza danych medycznych

```python
# Dane pacjentów
pacjenci = pd.DataFrame({
    'grupa_krwi': np.random.choice(['A', 'B', 'AB', '0'], 500, p=[0.37, 0.12, 0.05, 0.46]),
    'Rh': np.random.choice(['+', '-'], 500, p=[0.85, 0.15]),
    'płeć': np.random.choice(['M', 'K'], 500),
    'palenie': np.random.choice(['Tak', 'Nie', 'Rzucił/a'], 500, p=[0.2, 0.65, 0.15]),
    'BMI_kategoria': np.random.choice(['Niedowaga', 'Norma', 'Nadwaga', 'Otyłość'], 500,
                                     p=[0.05, 0.45, 0.35, 0.15])
})

print("=== ANALIZA DANYCH MEDYCZNYCH ===")
print(f"Liczba pacjentów: {len(pacjenci)}")

print("\n1. Grupy krwi:")
grupy_krwi = pacjenci['grupa_krwi'].value_counts().sort_index()
for grupa, liczba in grupy_krwi.items():
    procent = liczba / len(pacjenci) * 100
    print(f"   Grupa {grupa}: {liczba:3} ({procent:4.1f}%)")

print("\n2. Czynnik Rh:")
rh_stats = pacjenci['Rh'].value_counts()
for rh, liczba in rh_stats.items():
    procent = liczba / len(pacjenci) * 100
    print(f"   Rh{rh}: {liczba:3} ({procent:4.1f}%)")

print("\n3. Palenie papierosów:")
palenie = pacjenci['palenie'].value_counts()
for status, liczba in palenie.items():
    procent = liczba / len(pacjenci) * 100
    print(f"   {status}: {liczba:3} ({procent:4.1f}%)")

print("\n4. BMI kategorie:")
bmi = pacjenci['BMI_kategoria'].value_counts()
for kat, liczba in bmi.items():
    procent = liczba / len(pacjenci) * 100
    print(f"   {kat}: {liczba:3} ({procent:4.1f}%)")

# Kombinacje grupa_krwi + Rh
pacjenci['krew_pelna'] = pacjenci['grupa_krwi'] + pacjenci['Rh']
print("\n5. Pełne grupy krwi (top 8):")
pełne_grupy = pacjenci['krew_pelna'].value_counts().head(8)
for grupa, liczba in pełne_grupy.items():
    procent = liczba / len(pacjenci) * 100
    print(f"   {grupa}: {liczba:2} ({procent:4.1f}%)")
```

### 🛒 Analiza e-commerce

```python
# Dane zamówień e-commerce
zamowienia = pd.DataFrame({
    'kategoria': np.random.choice(['Elektronika', 'Odzież', 'Dom', 'Sport', 'Książki'], 2000,
                                 p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    'status': np.random.choice(['Dostarczone', 'W trakcie', 'Anulowane', 'Zwrócone'], 2000,
                              p=[0.85, 0.1, 0.03, 0.02]),
    'metoda_platnosci': np.random.choice(['Karta', 'BLIK', 'Przelew', 'Gotówka'], 2000,
                                        p=[0.5, 0.3, 0.15, 0.05]),
    'ocena': np.random.choice([1, 2, 3, 4, 5, np.nan], 2000, p=[0.02, 0.03, 0.1, 0.35, 0.4, 0.1])
})

print("=== ANALIZA E-COMMERCE ===")
print(f"Zamówienia: {len(zamowienia)}")

print("\n📦 Kategorie produktów:")
kategorie = zamowienia['kategoria'].value_counts()
for kat, liczba in kategorie.items():
    procent = liczba / len(zamowienia) * 100
    print(f"   {kat:12}: {liczba:4} ({procent:4.1f}%)")

print("\n🚚 Status zamówień:")
status = zamowienia['status'].value_counts()
for st, liczba in status.items():
    procent = liczba / len(zamowienia) * 100
    print(f"   {st:12}: {liczba:4} ({procent:4.1f}%)")

print("\n💳 Metody płatności:")
platnosci = zamowienia['metoda_platnosci'].value_counts()
for metoda, liczba in platnosci.items():
    procent = liczba / len(zamowienia) * 100
    print(f"   {metoda:12}: {liczba:4} ({procent:4.1f}%)")

print("\n⭐ Oceny (bez uwzględnienia NaN):")
oceny = zamowienia['ocena'].value_counts().sort_index()
for ocena, liczba in oceny.items():
    procent = liczba / zamowienia['ocena'].notna().sum() * 100
    gwiazdki = '★' * int(ocena)
    print(f"   {gwiazdki} ({ocena}): {liczba:4} ({procent:4.1f}%)")

# Średnia ocena
srednia_ocena = zamowienia['ocena'].mean()
print(f"\nŚrednia ocena: {srednia_ocena:.2f}/5")
```

## 🔍 Zaawansowane użycie

### 1️⃣ Łączenie z crosstab

```python
# Analiza krzyżowa
print("Metoda płatności vs Status zamówienia:")
crosstab = pd.crosstab(zamowienia['metoda_platnosci'], 
                       zamowienia['status'], 
                       normalize='index') * 100

print(crosstab.round(1))
```

### 2️⃣ Top N wartości

```python
# Top 3 kategorie z dodatkowymi informacjami
print("Top 3 kategorie z detalami:")
top_kategorie = zamowienia['kategoria'].value_counts().head(3)

for i, (kategoria, liczba) in enumerate(top_kategorie.items(), 1):
    procent = liczba / len(zamowienia) * 100
    avg_ocena = zamowienia[zamowienia['kategoria'] == kategoria]['ocena'].mean()
    print(f"{i}. {kategoria}: {liczba} zamówień ({procent:.1f}%), średnia ocena: {avg_ocena:.2f}")
```

## ⚠️ Uwagi i pułapki

```python
# 1. value_counts() vs nunique()
seria = pd.Series(['A', 'B', 'A', 'C', 'B', 'A'])

print("value_counts() - ile razy występuje każda wartość:")
print(seria.value_counts())

print(f"\nnunique() - ile unikalnych wartości: {seria.nunique()}")

# 2. Sortowanie można kombinować
print("\nRóżne sortowania:")
counts = seria.value_counts()
print("Według częstości (domyślnie):")
print(counts)

print("Według nazw (indeks):")
print(counts.sort_index())

print("Według częstości rosnąco:")
print(counts.sort_values())
```

## 📝 Podsumowanie

`value_counts()` to podstawowe narzędzie eksploracji danych:

- 📊 Liczy częstość wystąpień każdej unikalnej wartości
- 📈 `normalize=True` dla proporcji zamiast liczb
- 🔄 `sort=True/False` i `ascending=True/False` dla sortowania  
- 🚫 `dropna=True/False` dla obsługi NaN
- 🎯 Idealne do kategorii, statusów, grup
- 📋 Podstawa dla analiz rozkładu danych
- 🔍 Świetne do quick insights o danych

To jak automatyczny licznik popularności - od razu widać co jest najczęstsze! 📊✨