## 🐼 Pandas - Wprowadzenie do DataFrame

_Biblioteka do manipulacji i analizy danych strukturalnych_

---

### 📝 Wprowadzenie do Pandas

**Pandas** to najważniejsza biblioteka do pracy z danymi strukturalnymi w Python:

1. **DataFrame** - główna struktura danych (jak tabela w Excel)
2. **Series** - jednowymiarowa struktura danych (kolumna DataFrame)
3. **Potężne narzędzia** do czyszczenia, transformacji i analizy danych
4. **Integracja** z NumPy, Matplotlib i innymi bibliotekami

```python
import pandas as pd
import numpy as np

# Sprawdzenie wersji
print(pd.__version__)
```

---

### 🏗️ Tworzenie DataFrame

#### Z różnych źródeł danych

```python
# 1. Ze słownika
data_dict = {
    'Imię': ['Anna', 'Jan', 'Katarzyna', 'Piotr'],
    'Wiek': [25, 30, 35, 28],
    'Miasto': ['Warszawa', 'Kraków', 'Gdańsk', 'Wrocław'],
    'Pensja': [5000, 6000, 5500, 4800]
}
df = pd.DataFrame(data_dict)
print(df)

# 2. Z listy list
data_list = [
    ['Anna', 25, 'Warszawa', 5000],
    ['Jan', 30, 'Kraków', 6000],
    ['Katarzyna', 35, 'Gdańsk', 5500]
]
df = pd.DataFrame(data_list, columns=['Imię', 'Wiek', 'Miasto', 'Pensja'])

# 3. Z tablicy NumPy
arr = np.random.randn(4, 3)
df = pd.DataFrame(arr, columns=['A', 'B', 'C'])

# 4. Z pliku CSV
df = pd.read_csv('plik.csv')

# 5. Pusty DataFrame z określonymi kolumnami
df_empty = pd.DataFrame(columns=['Imię', 'Wiek', 'Miasto'])
```

---

### 🔍 Podstawowe informacje o DataFrame

```python
df = pd.DataFrame({
    'Imię': ['Anna', 'Jan', 'Katarzyna', 'Piotr'],
    'Wiek': [25, 30, 35, 28],
    'Miasto': ['Warszawa', 'Kraków', 'Gdańsk', 'Wrocław'],
    'Pensja': [5000, 6000, 5500, 4800]
})

# Podstawowe informacje
print(f"Kształt: {df.shape}")              # (4, 4)
print(f"Rozmiar: {df.size}")               # 16
print(f"Kolumny: {df.columns.tolist()}")   # Lista kolumn
print(f"Indeks: {df.index.tolist()}")      # Lista indeksów
print(f"Typy danych:\n{df.dtypes}")

# Podgląd danych
print(df.head())        # Pierwsze 5 wierszy (domyślnie)
print(df.head(2))       # Pierwsze 2 wiersze
print(df.tail())        # Ostatnie 5 wierszy
print(df.sample(3))     # 3 losowe wiersze

# Informacje szczegółowe
df.info()               # Typy, pamięć, brakujące wartości
print(df.describe())    # Statystyki opisowe dla kolumn numerycznych
```

---

### 📊 Dostęp do danych

#### Wybieranie kolumn

```python
# Pojedyncza kolumna (zwraca Series)
wiek = df['Wiek']
print(type(wiek))       # pandas.core.series.Series

# Wiele kolumn (zwraca DataFrame)
subset = df[['Imię', 'Pensja']]
print(type(subset))     # pandas.core.frame.DataFrame

# Wszystkie kolumny numeryczne
numeric_cols = df.select_dtypes(include=[np.number])
print(numeric_cols)

# Dostęp przez atrybut (tylko gdy nazwa kolumny jest poprawna dla Python)
pensje = df.Pensja      # Równoważne df['Pensja']
```

#### Wybieranie wierszy

```python
# Przez indeks pozycyjny (iloc)
pierwszy_wiersz = df.iloc[0]        # Pierwszy wiersz
pierwsze_dwa = df.iloc[0:2]         # Pierwsze dwa wiersze
ostatni = df.iloc[-1]               # Ostatni wiersz

# Przez etykietę indeksu (loc)
# (gdy indeks ma nazwy zamiast liczb)
df_with_names = df.set_index('Imię')
anna_data = df_with_names.loc['Anna']

# Kombinacja wierszy i kolumn
# iloc[wiersze, kolumny]
fragment = df.iloc[0:2, 1:3]       # Wiersze 0-1, kolumny 1-2
konkretny = df.iloc[1, 2]          # Wiersz 1, kolumna 2

# loc[wiersze, kolumny]
df_indexed = df.set_index('Imię')
anna_wiek = df_indexed.loc['Anna', 'Wiek']
```

---

### 🔧 Modyfikacja danych

#### Dodawanie kolumn

```python
# Nowa kolumna z wartością stałą
df['Krajowość'] = 'Polska'

# Nowa kolumna na podstawie obliczeń
df['Pensja_netto'] = df['Pensja'] * 0.77

# Nowa kolumna z warunkami
df['Kategoria_wiekowa'] = np.where(df['Wiek'] < 30, 'Młody', 'Starszy')

# Złożone warunki
conditions = [
    df['Pensja'] < 5000,
    df['Pensja'] < 6000,
    df['Pensja'] >= 6000
]
choices = ['Niska', 'Średnia', 'Wysoka']
df['Kategoria_pensji'] = np.select(conditions, choices)
```

#### Modyfikacja wartości

```python
# Zmiana pojedynczej wartości
df.loc[0, 'Wiek'] = 26
df.iloc[1, 1] = 31

# Zmiana z warunkiem
df.loc[df['Miasto'] == 'Kraków', 'Pensja'] = 6200

# Zastąpienie wartości
df['Miasto'] = df['Miasto'].replace('Gdańsk', 'Gdynia')

# Zastąpienie wielu wartości
replace_dict = {'Warszawa': 'Warsaw', 'Kraków': 'Cracow'}
df['Miasto_EN'] = df['Miasto'].replace(replace_dict)
```

#### Dodawanie i usuwanie wierszy

```python
# Dodanie nowego wiersza
nowy_wiersz = pd.DataFrame({
    'Imię': ['Magdalena'],
    'Wiek': [27],
    'Miasto': ['Poznań'],
    'Pensja': [5200]
})
df = pd.concat([df, nowy_wiersz], ignore_index=True)

# Usuwanie wierszy
df = df.drop(0)                     # Usuń wiersz o indeksie 0
df = df.drop([1, 2])               # Usuń wiersze o indeksach 1,2
df = df[df['Wiek'] > 25]           # Zachowaj tylko wiersze gdzie Wiek > 25

# Reset indeksu po usunięciu
df = df.reset_index(drop=True)

# Usuwanie kolumn
df = df.drop('Krajowość', axis=1)   # Usuń kolumnę
df = df.drop(['Pensja_netto', 'Kategoria_wiekowa'], axis=1)  # Usuń wiele kolumn
```

---

### 🎯 Filtrowanie danych

```python
# Podstawowe filtrowanie
mlodzi = df[df['Wiek'] < 30]
wysokie_pensje = df[df['Pensja'] > 5000]

# Wiele warunków
filtered = df[(df['Wiek'] > 25) & (df['Pensja'] < 6000)]

# Warunki OR
war_krak = df[(df['Miasto'] == 'Warszawa') | (df['Miasto'] == 'Kraków')]

# Filtrowanie przez listę wartości
wybrane_miasta = df[df['Miasto'].isin(['Warszawa', 'Gdańsk'])]

# Filtrowanie przez tekst
zawiera_a = df[df['Imię'].str.contains('a')]
zaczyna_od = df[df['Imię'].str.startswith('A')]

# Negacja warunków
nie_warszawa = df[~(df['Miasto'] == 'Warszawa')]  # ~ oznacza NOT
```

---

### 🗂️ Sortowanie

```python
# Sortowanie według jednej kolumny
sorted_by_age = df.sort_values('Wiek')                    # Rosnąco
sorted_by_salary_desc = df.sort_values('Pensja', ascending=False)  # Malejąco

# Sortowanie według wielu kolumn
multi_sort = df.sort_values(['Miasto', 'Wiek'], ascending=[True, False])

# Sortowanie według indeksu
sorted_by_index = df.sort_index()

# In-place sorting (modyfikuje oryginalny DataFrame)
df.sort_values('Wiek', inplace=True)
```

---

### 📋 Praktyczne przykłady

```python
# 1. Analiza podstawowa
print(f"Średni wiek: {df['Wiek'].mean():.1f}")
print(f"Najwyższa pensja: {df['Pensja'].max()}")
print(f"Liczba unikalnych miast: {df['Miasto'].nunique()}")

# 2. Grupowanie i agregacja (szczegóły w kolejnych notatkach)
mean_salary_by_city = df.groupby('Miasto')['Pensja'].mean()
print(mean_salary_by_city)

# 3. Tworzenie raportów
report = df.groupby('Miasto').agg({
    'Wiek': 'mean',
    'Pensja': ['min', 'max', 'mean']
})
print(report)

# 4. Top N wartości
top_earners = df.nlargest(2, 'Pensja')  # 2 najwyższe pensje
youngest = df.nsmallest(2, 'Wiek')      # 2 najmłodsze osoby
```

---

### 💡 Najlepsze praktyki

1. **Zawsze sprawdź dane** - `df.info()`, `df.describe()`, `df.head()`
2. **Kopiuj DataFrame** przy modyfikacjach - `df.copy()`
3. **Używaj czytelnych nazw kolumn** - bez spacji, polskich znaków w kodzie
4. **Regularnie sprawdzaj typy danych** - `df.dtypes`
5. **Dokumentuj transformacje** - komentarze w kodzie

---

### 🎯 Następny krok

Poznasz **operacje na danych w Pandas**:

- Funkcje agregujące i statystyczne
- Operacje na tekstach
- Praca z datami
- Transformacje danych
- Pivot tables i cross-tabulation