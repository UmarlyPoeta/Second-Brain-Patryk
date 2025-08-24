# 🔢 Pandas - DataFrame.iloc[] - Selekcja oparta na pozycjach

## 📚 Co to jest DataFrame.iloc[]?

`DataFrame.iloc[]` to narzędzie w Pandas do selekcji danych opartej na **pozycjach numerycznych** (jak indeksy w liście Python). To jak współrzędne na mapie - podajesz konkretne liczby i dostajesz dane z tej pozycji! 📍

## 🔧 Podstawowa składnia

```python
import pandas as pd

# Podstawowa składnia
df.iloc[row_indexer, column_indexer]
df.iloc[row_indexer]  # tylko wiersze, wszystkie kolumny
```

## 💻 Praktyczne przykłady

### 1️⃣ Podstawowa selekcja po pozycji

```python
import pandas as pd

# Przykładowy DataFrame
dane = {
    'Imie': ['Anna', 'Jan', 'Maria', 'Piotr', 'Ewa'],
    'Wiek': [25, 30, 35, 28, 32],
    'Miasto': ['Warszawa', 'Kraków', 'Gdańsk', 'Poznań', 'Wrocław'],
    'Pensja': [5000, 6000, 7000, 5500, 6500]
}

df = pd.DataFrame(dane)
print("DataFrame:")
print(df)
print(f"Shape: {df.shape}")

# Pierwszy wiersz (indeks 0)
pierwszy_wiersz = df.iloc[0]
print(f"\nPierwszy wiersz (0):")
print(pierwszy_wiersz)

# Trzeci wiersz, druga kolumna (Maria, Wiek)
wartość = df.iloc[2, 1]  # pozycja [2,1]
print(f"\nWartość na pozycji [2,1]: {wartość}")

# Ostatni wiersz
ostatni = df.iloc[-1]
print(f"\nOstatni wiersz (-1):")
print(ostatni)
```

### 2️⃣ Selekcja zakresów i list

```python
# Pierwsze 3 wiersze
pierwsze_trzy = df.iloc[0:3]
print("Pierwsze 3 wiersze (0:3):")
print(pierwsze_trzy)

# Ostatnie 2 wiersze
ostatnie_dwa = df.iloc[-2:]
print(f"\nOstatnie 2 wiersze (-2:):")
print(ostatnie_dwa)

# Konkretne wiersze i kolumny przez listy
wybrane = df.iloc[[0, 2, 4], [0, 3]]  # wiersze 0,2,4 i kolumny 0,3
print(f"\nWybrane wiersze i kolumny:")
print(wybrane)

# Co drugi wiersz
co_drugi = df.iloc[::2]
print(f"\nCo drugi wiersz (::2):")
print(co_drugi)

# Pierwszy i ostatni wiersz, środkowe kolumny
fragment = df.iloc[[0, -1], 1:3]
print(f"\nFragment [0,-1], 1:3:")
print(fragment)
```

### 3️⃣ Wszystkie wiersze lub kolumny

```python
# Wszystkie wiersze, tylko pierwsza kolumna
pierwsza_kolumna = df.iloc[:, 0]
print("Pierwsza kolumna (wszystkie wiersze):")
print(pierwsza_kolumna)

# Pierwszy wiersz, wszystkie kolumny
pierwszy_wszystkie = df.iloc[0, :]
print(f"\nPierwszy wiersz (wszystkie kolumny):")
print(pierwszy_wszystkie)

# Środkowe kolumny, wszystkie wiersze
srodkowe = df.iloc[:, 1:3]
print(f"\nŚrodkowe kolumny (1:3):")
print(srodkowe)
```

## 🎯 Praktyczne przypadki użycia

### 📊 Podglądanie danych

```python
# Duży dataset
np.random.seed(42)
duze_dane = pd.DataFrame({
    'A': np.random.randn(1000),
    'B': np.random.randn(1000),
    'C': np.random.randn(1000),
    'D': np.random.randn(1000),
    'E': np.random.randn(1000)
})

print(f"Duży dataset: {duze_dane.shape}")

# Szybki podgląd - pierwsze 5 wierszy, pierwsze 3 kolumny
podglad = duze_dane.iloc[:5, :3]
print("Podgląd (5x3):")
print(podglad)

# Losowe 10 wierszy dla przeglądu
import numpy as np
losowe_indeksy = np.random.choice(duze_dane.shape[0], 10, replace=False)
losowe_wiersze = duze_dane.iloc[losowe_indeksy]
print(f"\n10 losowych wierszy:")
print(losowe_wiersze.head())

# Ostatnie kolumny dla sprawdzenia
ostatnie_kolumny = duze_dane.iloc[:10, -2:]
print(f"\nOstatnie 2 kolumny (pierwszych 10 wierszy):")
print(ostatnie_kolumny)
```

### 🎯 Dzielenie danych (train/test split ręczny)

```python
# Mały dataset dla przykładu
data = pd.DataFrame({
    'feature1': range(100),
    'feature2': range(100, 200),
    'target': range(200, 300)
})

print(f"Całość: {data.shape}")

# Podział 80/20 (train/test)
n_samples = len(data)
train_size = int(0.8 * n_samples)

# Training data (80%)
train_data = data.iloc[:train_size]
print(f"Train: {train_data.shape}")

# Test data (20%)
test_data = data.iloc[train_size:]
print(f"Test: {test_data.shape}")

# Lub można użyć random split
shuffled_indices = np.random.permutation(n_samples)
train_indices = shuffled_indices[:train_size]
test_indices = shuffled_indices[train_size:]

train_random = data.iloc[train_indices]
test_random = data.iloc[test_indices]

print(f"Random train: {train_random.shape}")
print(f"Random test: {test_random.shape}")
```

### 📈 Analiza szeregów czasowych

```python
# Dane czasowe
daty = pd.date_range('2023-01-01', periods=365, freq='D')
szereg_czasowy = pd.DataFrame({
    'data': daty,
    'sprzedaz': np.random.randint(100, 1000, 365),
    'koszty': np.random.randint(50, 500, 365)
})

print("Szereg czasowy:")
print(szereg_czasowy.head())

# Pierwszy miesiąc (pierwsze ~30 dni)
pierwszy_miesiac = szereg_czasowy.iloc[:30]
print(f"\nPierwszy miesiąc (30 dni):")
print(f"Średnia sprzedaż: {pierwszy_miesiac.iloc[:, 1].mean():.0f}")

# Ostatni kwartał (ostatnie ~90 dni)
ostatni_kwartal = szereg_czasowy.iloc[-90:]
print(f"\nOstatni kwartał:")
print(f"Średnia sprzedaż: {ostatni_kwartal.iloc[:, 1].mean():.0f}")

# Co 7. dzień (tygodniowy pattern)
tygodniowo = szereg_czasowy.iloc[::7]
print(f"\nDane co 7 dni: {tygodniowo.shape[0]} punktów")
```

### 🔍 Filtrowanie i selekcja pozycyjna

```python
# Dataset ze studentami
studenci = pd.DataFrame({
    'student_id': [f'S{i:03d}' for i in range(1, 21)],
    'matematyka': np.random.randint(60, 100, 20),
    'fizyka': np.random.randint(50, 95, 20),
    'chemia': np.random.randint(55, 98, 20)
})

print("Studenci (pierwsze 5):")
print(studenci.head())

# Top 5 studentów (załóżmy że są posortowani)
studenci_sorted = studenci.sort_values('matematyka', ascending=False)
top_5 = studenci_sorted.iloc[:5]
print(f"\nTop 5 w matematyce:")
print(top_5[['student_id', 'matematyka']])

# Co drugi student z top 10
co_drugi_top = studenci_sorted.iloc[::2][:5]
print(f"\nCo drugi z top studentów:")
print(co_drugi_top[['student_id', 'matematyka']])

# Środkowi studenci (pozycje 8-12)
srodkowi = studenci_sorted.iloc[8:13]
print(f"\nŚrodkowi studenci (pozycje 8-12):")
print(srodkowi[['student_id', 'matematyka']])
```

## 🔍 Zaawansowane użycie

### 1️⃣ Łączenie z innymi metodami

```python
# DataFrame z danymi sprzedażowymi
sprzedaz = pd.DataFrame({
    'produkt': [f'P{i}' for i in range(1, 11)],
    'q1': np.random.randint(100, 500, 10),
    'q2': np.random.randint(120, 600, 10),
    'q3': np.random.randint(80, 450, 10),
    'q4': np.random.randint(150, 700, 10)
})

print("Sprzedaż produktów:")
print(sprzedaz)

# Sortuj po Q1, weź top 3
top_q1 = sprzedaz.nlargest(3, 'q1')
print(f"\nTop 3 produkty w Q1:")
print(top_q1.iloc[:, [0, 1]])  # tylko nazwa i Q1

# Najgorszych 3 w Q4, tylko kwartały
bottom_q4_quarters = sprzedaz.nsmallest(3, 'q4').iloc[:, 1:]
print(f"\nNajgorsze 3 w Q4 (tylko kwartały):")
print(bottom_q4_quarters)
```

### 2️⃣ Dynamiczne indeksowanie

```python
# DataFrame z różną liczbą kolumn
def analyze_last_columns(df, n_cols=2):
    """Analizuje ostatnie n kolumn"""
    last_cols = df.iloc[:, -n_cols:]
    return {
        'shape': last_cols.shape,
        'mean': last_cols.mean(),
        'sum': last_cols.sum()
    }

# Test z różnymi DataFrame
df_small = pd.DataFrame(np.random.rand(5, 3), columns=['A', 'B', 'C'])
df_large = pd.DataFrame(np.random.rand(10, 8), columns=[f'Col{i}' for i in range(8)])

print("Analiza ostatnich 2 kolumn:")
print(f"Small DF: {analyze_last_columns(df_small)['shape']}")
print(f"Large DF: {analyze_last_columns(df_large)['shape']}")
```

### 3️⃣ Sliding window (okno przesuwne)

```python
# Dane czasowe dla okna przesuwnego
ts_data = pd.DataFrame({
    'value': np.random.randn(20).cumsum(),
    'date': pd.date_range('2023-01-01', periods=20)
})

print("Dane czasowe:")
print(ts_data.head())

# Okno przesuwne 5-elementowe
window_size = 5
windows = []

for i in range(len(ts_data) - window_size + 1):
    window = ts_data.iloc[i:i+window_size, 0]  # tylko kolumna 'value'
    windows.append({
        'start_idx': i,
        'end_idx': i+window_size-1,
        'mean': window.mean(),
        'std': window.std()
    })

windows_df = pd.DataFrame(windows)
print(f"\nOkna przesuwne (rozmiar {window_size}):")
print(windows_df.head())
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ Różnica między iloc[] a loc[]

```python
# DataFrame z niestandardowym indeksem
df_custom = pd.DataFrame({'A': [1, 2, 3]}, index=[10, 20, 30])
print("DataFrame z custom index:")
print(df_custom)

# iloc używa pozycji
print(f"iloc[0]: {df_custom.iloc[0]['A']}")  # pierwszy element (pozycja 0)

# loc używa etykiet
print(f"loc[10]: {df_custom.loc[10]['A']}")  # etykieta indeksu '10'

# BŁĄD - mieszanie
try:
    # df_custom.iloc[10]  # Nie ma pozycji 10!
    pass
except IndexError:
    print("IndexError - brak pozycji 10")
```

### 2️⃣ Przekraczanie granic

```python
small_df = pd.DataFrame({'A': [1, 2, 3]})

try:
    # out_of_bounds = small_df.iloc[5]  # Index out of bounds!
    pass
except IndexError as e:
    print(f"IndexError: {e}")

# Bezpieczne sprawdzenie
if len(small_df) > 5:
    safe_access = small_df.iloc[5]
else:
    print("Za mało wierszy dla indeksu 5")
```

### 3️⃣ Slice vs lista

```python
df_test = pd.DataFrame({'A': range(5), 'B': range(5, 10)})

# Slice - zwraca DataFrame
slice_result = df_test.iloc[1:3]
print(f"Slice type: {type(slice_result)}")

# Single index - zwraca Series
single_result = df_test.iloc[1]
print(f"Single type: {type(single_result)}")

# Lista z jednym elementem - zwraca DataFrame
list_result = df_test.iloc[[1]]
print(f"List type: {type(list_result)}")
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Sprawdzaj rozmiary przed indexowaniem
df = pd.DataFrame({'A': range(10)})

if len(df) > 5:
    safe_slice = df.iloc[:5]

# 2. Używaj negative indexing dla końca
last_rows = df.iloc[-3:]  # ostatnie 3 wiersze

# 3. Łącz z shape dla dynamicznego dostępu
n_rows, n_cols = df.shape
middle_row = df.iloc[n_rows//2]

# 4. Używaj step dla próbkowania
sample = df.iloc[::2]  # co drugi wiersz
```

### ❌ Unikaj

```python
# Nie używaj bezpośrednio dużych liczb bez sprawdzenia
# big_index = df.iloc[99999]  # może nie istnieć!

# Nie mieszaj loc i iloc
# df.iloc['some_label']  # iloc tylko pozycje!

# Unikaj wielokrotnego iloc w pętli (wolne)
# for i in range(len(df)):
#     row = df.iloc[i]  # wolniejsze niż iterrows()
```

## 🔗 Powiązane funkcje i metody

- `df.loc[]` - selekcja oparta na etykietach
- `df.at[]` / `df.iat[]` - szybka selekcja pojedynczych wartości
- `df.head()` / `df.tail()` - pierwsze/ostatnie wiersze
- `df.sample()` - losowe wiersze
- `df.nlargest()` / `df.nsmallest()` - n największych/najmniejszych

## 📚 Porównanie metod selekcji

```python
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [10, 20, 30, 40]
}, index=['a', 'b', 'c', 'd'])

print("Porównanie metod:")
print(f"iloc[1,0] (pozycja):  {df.iloc[1, 0]}")
print(f"loc['b','A'] (etykiety): {df.loc['b', 'A']}")
print(f"iat[1,0] (szybkie):   {df.iat[1, 0]}")
print(f"at['b','A'] (szybkie): {df.at['b', 'A']}")

# Wydajność
print(f"head(2):")
print(df.head(2))
print(f"iloc[:2] (równoważne):")
print(df.iloc[:2])
```

## 📝 Podsumowanie

`DataFrame.iloc[]` to narzędzie pozycyjnej selekcji:

- 🔢 Używa **pozycji numerycznych** (jak listy Python)
- 📐 Format: `df.iloc[row_positions, column_positions]`
- 🎯 Obsługuje slice (`:`), listy (`[]`), negative indexing (`-1`)
- ⚡ Szybkie dla znanej struktury danych
- 🔍 Idealne do iteracji, sampling, dzielenia danych
- ⚠️ Sprawdzaj zawsze rozmiary DataFrame przed dostępem!

To jak GPS współrzędne - podajesz dokładną pozycję i dostajesz dane! 🗺️📍