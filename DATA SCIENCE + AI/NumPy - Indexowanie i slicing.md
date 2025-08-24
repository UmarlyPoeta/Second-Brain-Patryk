## 🔢 NumPy - Indexowanie i slicing

_Zaawansowane techniki dostępu do danych w tablicach_

---

### 📝 Podstawowe indexowanie

#### Tablice jednowymiarowe

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Dostęp do pojedynczych elementów
print(arr[0])    # 10 - pierwszy element
print(arr[-1])   # 50 - ostatni element
print(arr[2])    # 30 - trzeci element

# Modyfikacja elementów
arr[1] = 25
print(arr)       # [10, 25, 30, 40, 50]

# Slicing - [start:stop:step]
print(arr[1:4])    # [25, 30, 40] - elementy 1-3
print(arr[:3])     # [10, 25, 30] - pierwsze 3
print(arr[2:])     # [30, 40, 50] - od 3. do końca
print(arr[::2])    # [10, 30, 50] - co drugi element
print(arr[::-1])   # [50, 40, 30, 25, 10] - odwrócona
```

#### Tablice wielowymiarowe

```python
# Tablica 2D
matrix = np.array([[1, 2, 3], 
                   [4, 5, 6], 
                   [7, 8, 9]])

# Dostęp [wiersz, kolumna]
print(matrix[0, 0])     # 1 - pierwszy element
print(matrix[1, 2])     # 6 - wiersz 1, kolumna 2
print(matrix[-1, -1])   # 9 - ostatni element

# Dostęp do całych wierszy/kolumn
print(matrix[0, :])     # [1, 2, 3] - pierwszy wiersz
print(matrix[:, 0])     # [1, 4, 7] - pierwsza kolumna
print(matrix[1])        # [4, 5, 6] - można pominąć :

# Slicing 2D
print(matrix[0:2, 1:3]) # Wiersze 0-1, kolumny 1-2
# [[2, 3],
#  [5, 6]]
```

---

### 🎯 Fancy Indexing

**Fancy indexing** pozwala na dostęp do elementów za pomocą tablic indeksów:

```python
arr = np.array([10, 20, 30, 40, 50, 60])

# Lista indeksów
indices = [0, 2, 4]
print(arr[indices])     # [10, 30, 50]

# Tablica indeksów
indices_arr = np.array([1, 3, 5])
print(arr[indices_arr]) # [20, 40, 60]

# Fancy indexing 2D
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])

# Wybór konkretnych elementów
rows = np.array([0, 1, 2])
cols = np.array([1, 2, 3])
print(matrix[rows, cols])  # [2, 7, 12] - elementy (0,1), (1,2), (2,3)

# Wybór wierszy w określonej kolejności
row_indices = [2, 0, 1]
print(matrix[row_indices])
# [[9, 10, 11, 12],
#  [1, 2, 3, 4],
#  [5, 6, 7, 8]]
```

---

### 🔍 Boolean Indexing

**Boolean indexing** używa tablic logicznych do filtrowania danych:

```python
arr = np.array([1, 5, 3, 8, 2, 7, 6, 4])

# Tworzenie maski logicznej
mask = arr > 4
print(mask)             # [False, True, False, True, False, True, True, False]

# Zastosowanie maski
filtered = arr[mask]
print(filtered)         # [5, 8, 7, 6] - tylko elementy > 4

# Bezpośrednio w jednej linii
print(arr[arr > 4])     # [5, 8, 7, 6]

# Złożone warunki
print(arr[(arr > 3) & (arr < 7)])  # [5, 6, 4] - między 3 a 7
print(arr[(arr < 3) | (arr > 7)])  # [1, 2, 8] - mniejsze od 3 lub większe od 7

# Boolean indexing w 2D
matrix = np.array([[1, 2, 3], 
                   [4, 5, 6], 
                   [7, 8, 9]])

# Elementy większe od 5
print(matrix[matrix > 5])  # [6, 7, 8, 9]

# Modyfikacja z użyciem boolean indexing
matrix[matrix > 5] = 0
print(matrix)
# [[1, 2, 3],
#  [4, 5, 0],
#  [0, 0, 0]]
```

---

### ⚙️ Zaawansowane slicing

```python
# Tablica 3D
arr_3d = np.arange(24).reshape(2, 3, 4)
print(arr_3d.shape)     # (2, 3, 4)

# Dostęp do wymiarów
print(arr_3d[0])        # Pierwszy "blok" 3x4
print(arr_3d[0, 1])     # Drugi wiersz pierwszego bloku
print(arr_3d[0, 1, 2])  # Konkretny element

# Slicing z wieloma wymiarami
print(arr_3d[:, 1:3, ::2])  # Wszystkie bloki, wiersze 1-2, co druga kolumna

# Użycie elipsis (...)
print(arr_3d[0, ...])   # Równoważne arr_3d[0, :, :]
print(arr_3d[..., -1])  # Ostatnia kolumna ze wszystkich wymiarów

# Newaxis do dodawania wymiarów
arr = np.array([1, 2, 3])
print(arr.shape)                    # (3,)
print(arr[np.newaxis, :].shape)     # (1, 3)
print(arr[:, np.newaxis].shape)     # (3, 1)
```

---

### 🔄 Kopiowanie vs Widoki

```python
original = np.array([1, 2, 3, 4, 5])

# View (widok) - dzieli pamięć z oryginałem
view = original[1:4]
view[0] = 999
print(original)         # [1, 999, 3, 4, 5] - zmieniony!

# Copy (kopia) - nowa pamięć
original = np.array([1, 2, 3, 4, 5])
copy = original[1:4].copy()
copy[0] = 999
print(original)         # [1, 2, 3, 4, 5] - bez zmian

# Sprawdzanie czy to view czy copy
print(np.shares_memory(original, view))   # True
print(np.shares_memory(original, copy))   # False

# Fancy indexing zawsze tworzy kopię
fancy = original[[1, 2, 3]]
fancy[0] = 888
print(original)         # [1, 2, 3, 4, 5] - bez zmian
```

---

### 🎛️ Manipulacja indeksów

```python
# np.where() - znajdowanie indeksów spełniających warunek
arr = np.array([1, 5, 3, 8, 2, 7])
indices = np.where(arr > 4)
print(indices[0])       # [1, 3, 5] - indeksy elementów > 4

# Zastępowanie wartości z warunkiem
result = np.where(arr > 4, arr, 0)  # Jeśli > 4 to pozostaw, inaczej 0
print(result)           # [0, 5, 0, 8, 0, 7]

# np.select() - wielokrotne warunki
conditions = [arr < 3, arr < 6, arr >= 6]
choices = ['mały', 'średni', 'duży']
labels = np.select(conditions, choices)
print(labels)           # ['mały', 'średni', 'mały', 'duży', 'mały', 'duży']

# np.choose() - wybór z tablic
choice_arr = np.array([0, 1, 0, 2, 1])
source_arrs = [arr, arr*2, arr*3]
chosen = np.choose(choice_arr, source_arrs)
print(chosen)           # [1, 10, 3, 24, 4]
```

---

### 💻 Praktyczne przykłady

```python
# 1. Filtrowanie danych wielowymiarowych
sales_data = np.array([[100, 200, 150],   # Sprzedaż Q1, Q2, Q3
                       [80, 220, 180],
                       [120, 180, 160],
                       [90, 240, 140]])

# Firmy z Q2 > 200
high_q2 = sales_data[sales_data[:, 1] > 200]
print("Firmy z wysoką sprzedażą Q2:")
print(high_q2)

# 2. Czyszczenie danych - usuwanie outlierów
data = np.array([1, 2, 3, 100, 4, 5, 6, -50, 7])
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

clean_data = data[(data >= lower_bound) & (data <= upper_bound)]
print(f"Dane bez outlierów: {clean_data}")

# 3. Segmentacja klientów
customer_ages = np.array([25, 35, 45, 55, 65, 75, 22, 38, 52])
age_groups = np.where(customer_ages < 30, 'Młodzi',
                     np.where(customer_ages < 50, 'Średni wiek', 'Starsi'))
print("Grupy wiekowe:", age_groups)

# 4. Wyszukiwanie najbliższych wartości
target = 42
arr = np.array([10, 25, 30, 40, 45, 50, 60])
closest_idx = np.argmin(np.abs(arr - target))
print(f"Najbliższa wartość do {target}: {arr[closest_idx]}")
```

---

### ⚡ Wskazówki optymalizacyjne

```python
# 1. Używaj boolean indexing zamiast pętli
# WOLNE:
result = []
for i, val in enumerate(arr):
    if val > threshold:
        result.append(val)

# SZYBKIE:
result = arr[arr > threshold]

# 2. Unikaj kopiowania gdy to możliwe
# Użyj view'ów dla operacji read-only

# 3. Kombinuj warunki efektywnie
# Zamiast: mask1 = arr > 10; mask2 = arr < 50; combined = mask1 & mask2
# Użyj: combined = (arr > 10) & (arr < 50)
```

---

### 🎯 Następny krok

Poznasz **Pandas - DataFrame**:

- Tworzenie i manipulacja DataFrame
- Indexowanie w Pandas
- Operacje na kolumnach i wierszach
- Filtrowanie i grupowanie danych
- Import/export różnych formatów