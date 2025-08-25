# 🎯 Pandas - DataFrame.loc[] - Selekcja oparta na etykietach

## 📚 Co to jest DataFrame.loc[]?

`DataFrame.loc[]` to podstawowe narzędzie w Pandas do selekcji danych opartej na **etykietach** (nazwach indeksów i kolumn). To jak GPS dla danych - podajesz dokładny adres i dostajesz to czego potrzebujesz! 🗺️

## 🔧 Podstawowa składnia

```python
import pandas as pd

# Podstawowa składnia
df.loc[row_indexer, column_indexer]
df.loc[row_indexer]  # tylko wiersze, wszystkie kolumny
```

## 💻 Praktyczne przykłady

### 1️⃣ Podstawowa selekcja

```python
import pandas as pd

# Przykładowy DataFrame
dane = {
    'Imie': ['Anna', 'Jan', 'Maria', 'Piotr', 'Ewa'],
    'Wiek': [25, 30, 35, 28, 32],
    'Miasto': ['Warszawa', 'Kraków', 'Gdańsk', 'Poznań', 'Wrocław'],
    'Pensja': [5000, 6000, 7000, 5500, 6500]
}

df = pd.DataFrame(dane, index=['P001', 'P002', 'P003', 'P004', 'P005'])
print("DataFrame:")
print(df)

# Jeden wiersz
wiersz_P003 = df.loc['P003']
print(f"\nWiersz P003:")
print(wiersz_P003)

# Jedna kolumna dla jednego wiersza
pensja_P003 = df.loc['P003', 'Pensja']
print(f"\nPensja P003: {pensja_P003}")

# Jeden wiersz, kilka kolumn
podstawowe_P003 = df.loc['P003', ['Imie', 'Wiek']]
print(f"\nPodstawowe info P003:")
print(podstawowe_P003)
```

### 2️⃣ Selekcja zakresów

```python
# Kilka wierszy (zakres)
kilka_wierszy = df.loc['P002':'P004']
print("Wiersze P002 do P004:")
print(kilka_wierszy)

# Kilka wierszy, kilka kolumn
fragment = df.loc['P002':'P004', 'Wiek':'Miasto']
print(f"\nFragment (P002-P004, Wiek-Miasto):")
print(fragment)

# Lista konkretnych wierszy
wybrani = df.loc[['P001', 'P003', 'P005']]
print(f"\nWybrani pracownicy:")
print(wybrani)

# Lista wierszy i kolumn
szczegoly = df.loc[['P001', 'P003'], ['Imie', 'Pensja']]
print(f"\nSzczegóły wybranych:")
print(szczegoly)
```

### 3️⃣ Selekcja warunkowa (Boolean indexing)

```python
# Warunki logiczne
print("Wszyscy pracownicy:")
print(df)

# Pracownicy starsi niż 30 lat
starsi = df.loc[df['Wiek'] > 30]
print(f"\nPracownicy > 30 lat:")
print(starsi)

# Złożone warunki
bogate_i_mlodziutkie = df.loc[(df['Pensja'] > 6000) & (df['Wiek'] < 35)]
print(f"\nBogate i młodziutkie (pensja > 6000 i wiek < 35):")
print(bogate_i_mlodziutkie)

# Z konkretnych kolumn
tylko_imiona_starszych = df.loc[df['Wiek'] > 30, 'Imie']
print(f"\nImiona starszych od 30:")
print(tylko_imiona_starszych)
```

## 🎯 Praktyczne przypadki użycia

### 📊 Analiza sprzedaży

```python
# Dane sprzedażowe
sprzedaz = pd.DataFrame({
    'Produkt': ['Laptop', 'Telefon', 'Tablet', 'Słuchawki', 'Mysz'],
    'Cena': [3000, 800, 1200, 150, 50],
    'Sprzedane': [25, 150, 80, 200, 300],
    'Kategoria': ['Elektronika', 'Elektronika', 'Elektronika', 'Akcesoria', 'Akcesoria'],
    'Ocena': [4.5, 4.2, 4.0, 4.8, 3.9]
}, index=['PRD001', 'PRD002', 'PRD003', 'PRD004', 'PRD005'])

print("Dane sprzedażowe:")
print(sprzedaz)

# Produkty elektroniczne
elektronika = sprzedaz.loc[sprzedaz['Kategoria'] == 'Elektronika']
print(f"\nProdukty elektroniczne:")
print(elektronika)

# Drogie produkty (>1000 PLN) - tylko nazwa i cena
drogie = sprzedaz.loc[sprzedaz['Cena'] > 1000, ['Produkt', 'Cena']]
print(f"\nDrogie produkty:")
print(drogie)

# Popularne i dobrze oceniane (sprzedane >100 i ocena >4.0)
popularne = sprzedaz.loc[(sprzedaz['Sprzedane'] > 100) & (sprzedaz['Ocena'] > 4.0)]
print(f"\nPopularne i dobrze oceniane:")
print(popularne)
```

### 🏥 Dane medyczne

```python
# Dane pacjentów
pacjenci = pd.DataFrame({
    'Imie': ['Anna K.', 'Jan N.', 'Maria S.', 'Piotr W.', 'Ewa T.'],
    'Wiek': [45, 67, 34, 52, 28],
    'Cisnienie': [120, 140, 110, 135, 105],
    'Cukier': [90, 110, 85, 95, 80],
    'BMI': [22.5, 27.8, 19.2, 25.1, 21.0],
    'Diagnoza': ['Zdrowy', 'Nadciśnienie', 'Zdrowy', 'Nadciśnienie', 'Zdrowy']
}, index=[f'PAC{i:03d}' for i in range(1, 6)])

print("Dane pacjentów:")
print(pacjenci)

# Pacjenci z nadciśnieniem
nadcisnienie = pacjenci.loc[pacjenci['Diagnoza'] == 'Nadciśnienie']
print(f"\nPacjenci z nadciśnieniem:")
print(nadcisnienie[['Imie', 'Wiek', 'Cisnienie']])

# Starsi pacjenci (>50 lat) z wysokim BMI (>25)
ryzykowni = pacjenci.loc[(pacjenci['Wiek'] > 50) & (pacjenci['BMI'] > 25)]
print(f"\nPacjenci ryzykowni (>50 lat, BMI>25):")
print(ryzykowni[['Imie', 'Wiek', 'BMI', 'Diagnoza']])

# Młodzi i zdrowi - tylko podstawowe dane
mlodzi_zdrowi = pacjenci.loc[
    (pacjenci['Wiek'] < 40) & (pacjenci['Diagnoza'] == 'Zdrowy'),
    ['Imie', 'Wiek']
]
print(f"\nMłodzi i zdrowi:")
print(mlodzi_zdrowi)
```

### 📈 Analiza finansowa

```python
# Dane akcji
akcje = pd.DataFrame({
    'Firma': ['Apple', 'Microsoft', 'Google', 'Amazon', 'Tesla'],
    'Cena': [150.5, 280.2, 2800.0, 3200.5, 750.0],
    'Zmiana%': [2.5, -1.2, 3.1, -0.8, 5.2],
    'Wolumen': [45000000, 32000000, 15000000, 28000000, 65000000],
    'Sektor': ['Tech', 'Tech', 'Tech', 'E-commerce', 'Auto']
}, index=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'])

print("Dane akcji:")
print(akcje)

# Akcje technologiczne
tech_akcje = akcje.loc[akcje['Sektor'] == 'Tech']
print(f"\nAkcje technologiczne:")
print(tech_akcje[['Firma', 'Cena', 'Zmiana%']])

# Akcje rosnące (zmiana% > 0) z dużym wolumenem (>30M)
rosnace = akcje.loc[
    (akcje['Zmiana%'] > 0) & (akcje['Wolumen'] > 30000000),
    ['Firma', 'Zmiana%', 'Wolumen']
]
print(f"\nRosnące z dużym wolumenem:")
print(rosnace)

# Najdroższa akcja
najdrozsza_idx = akcje['Cena'].idxmax()
najdrozsza = akcje.loc[najdrozsza_idx, ['Firma', 'Cena']]
print(f"\nNajdroższa akcja: {najdrozsza['Firma']} - ${najdrozsza['Cena']}")
```

## 🔍 Zaawansowane użycie

### 1️⃣ Callable (funkcje) jako warunki

```python
# DataFrame ze studentami
studenci = pd.DataFrame({
    'Imie': ['Anna', 'Jan', 'Maria', 'Piotr'],
    'Matematyka': [85, 92, 78, 88],
    'Fizyka': [80, 88, 85, 82],
    'Chemia': [90, 85, 88, 91]
}, index=['S001', 'S002', 'S003', 'S004'])

print("Studenci:")
print(studenci)

# Funkcja warunkowa - średnia > 85
def dobry_student(row):
    przedmioty = ['Matematyka', 'Fizyka', 'Chemia']
    srednia = row[przedmioty].mean()
    return srednia > 85

# Zastosowanie funkcji
dobrzy = studenci.loc[studenci.apply(dobry_student, axis=1)]
print(f"\nDobrzy studenci (średnia > 85):")
print(dobrzy)
```

### 2️⃣ MultiIndex

```python
# DataFrame z MultiIndex
arrays = [
    ['Warszawa', 'Warszawa', 'Kraków', 'Kraków'],
    ['Q1', 'Q2', 'Q1', 'Q2']
]
index = pd.MultiIndex.from_arrays(arrays, names=['Miasto', 'Kwartał'])

sprzedaz_multi = pd.DataFrame({
    'Sprzedaz': [1000, 1200, 800, 900],
    'Koszty': [700, 800, 500, 600]
}, index=index)

print("Sprzedaż MultiIndex:")
print(sprzedaz_multi)

# Selekcja z MultiIndex
warszawa = sprzedaz_multi.loc['Warszawa']
print(f"\nDane dla Warszawy:")
print(warszawa)

# Konkretny wiersz
warszawa_q1 = sprzedaz_multi.loc[('Warszawa', 'Q1')]
print(f"\nWarszawa Q1:")
print(warszawa_q1)

# Slice w MultiIndex
q1_wszedzie = sprzedaz_multi.loc[(slice(None), 'Q1'), :]
print(f"\nQ1 we wszystkich miastach:")
print(q1_wszedzie)
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ Różnica między loc[] a iloc[]

```python
df_test = pd.DataFrame({'A': [1, 2, 3]}, index=[10, 20, 30])
print("Test DataFrame:")
print(df_test)

# loc używa etykiet
print(f"loc[20]: {df_test.loc[20]['A']}")  # etykieta indeksu

# iloc używa pozycji
print(f"iloc[1]: {df_test.iloc[1]['A']}")  # pozycja (drugi element)

# BŁĄD - mieszanie
try:
    # df_test.loc[1]  # Nie ma etykiety '1'!
    pass
except KeyError:
    print("KeyError - brak etykiety '1'")
```

### 2️⃣ Zapomnienie o Boolean indexing

```python
df_test = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [10, 20, 30, 40]
})

# ŹLE - próba użycia wartości bezpośrednio
# bad = df_test.loc[df_test['A'] == 2, 'B']  # To zwraca Series

# DOBRZE - pamiętaj że to Boolean Series
mask = df_test['A'] == 2
good = df_test.loc[mask, 'B']
print(f"Wartość B gdzie A==2: {good.iloc[0]}")
```

### 3️⃣ Problemy z kopiami vs widokami

```python
df_original = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Selekcja może zwrócić widok lub kopię
subset = df_original.loc[0:1, 'A':'B']

# Bezpieczna modyfikacja - zawsze używaj copy()
safe_subset = df_original.loc[0:1, 'A':'B'].copy()
safe_subset.loc[0, 'A'] = 999

print("Oryginalny (powinien być bez zmian):")
print(df_original)
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Używaj nawiasów dla złożonych warunków
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
good_condition = (df['A'] > 1) & (df['B'] < 6)
result = df.loc[good_condition]

# 2. Określaj konkretne kolumny gdy możliwe
specific = df.loc[df['A'] > 1, ['A']]  # zamiast wszystkich kolumn

# 3. Używaj query() dla czytelnych warunków
query_result = df.query('A > 1 and B < 6')  # alternatywa dla loc

# 4. Sprawdzaj czy indeks istnieje
if 'some_index' in df.index:
    value = df.loc['some_index']
```

### ❌ Unikaj

```python
# Nie mieszaj loc i iloc
# df.loc[0]  # jeśli indeks to nie 0

# Nie modyfikuj bez copy() jeśli nie jesteś pewien
# subset = df.loc[condition]
# subset['new_col'] = value  # może zmienić oryginalny df!

# Nie używaj zagnieżdżonych loc
# df.loc[condition1].loc[condition2]  # wolniej niż combined condition
```

## 🔗 Powiązane funkcje i metody

- `df.iloc[]` - selekcja oparta na pozycjach (integer location)
- `df.at[]` - szybka selekcja jednej wartości (etykiety)
- `df.iat[]` - szybka selekcja jednej wartości (pozycje)
- `df.query()` - selekcja używając stringów SQL-like
- `df[condition]` - Boolean indexing (tylko wiersze)

## 📚 Porównanie z innymi metodami

```python
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [10, 20, 30, 40]
}, index=['a', 'b', 'c', 'd'])

# Różne sposoby selekcji
print("Różne metody:")
print(f"loc (etykiety): {df.loc['b', 'A']}")
print(f"iloc (pozycje): {df.iloc[1, 0]}")
print(f"at (szybkie): {df.at['b', 'A']}")
print(f"iat (szybkie): {df.iat[1, 0]}")

# Query dla warunków
query_style = df.query('A > 2')
loc_style = df.loc[df['A'] > 2]
print("Query i loc dają ten sam wynik:")
print(query_style.equals(loc_style))
```

## 📝 Podsumowanie

`DataFrame.loc[]` to podstawowe narzędzie selekcji w Pandas:

- 🎯 Używa **etykiet** (nazw indeksów i kolumn)
- 📐 Format: `df.loc[row_indexer, column_indexer]`
- 🔍 Obsługuje warunki Boolean (selekcja warunkowa)
- 📊 Może zwracać Series (1 wymiar) lub DataFrame (2 wymiary)
- ⚡ Łącz z warunkami logicznymi: `&`, `|`, `~`
- 🎨 Pamiętaj o nawiasach w złożonych warunkach!

To jak dokładny adres - podajesz gdzie chcesz dotrzeć i dostajesz dokładnie to! 📍✨