# 🔗 NumPy - numpy.concatenate() - Łączenie tablic

## 📚 Co to jest numpy.concatenate()?

`numpy.concatenate()` to funkcja, która łączy (skleja) tablice wzdłuż określonej osi. To jak łączenie wagonów pociągu - można je połączyć jeden za drugim lub obok siebie! 🚂🚃🚃

## 🔧 Podstawowa składnia

```python
import numpy as np

# Podstawowa składnia
numpy.concatenate((array1, array2, ...), axis=0, out=None, dtype=None)
```

## 💻 Praktyczne przykłady

### 1️⃣ Łączenie tablic 1D

```python
import numpy as np

# Dwie tablice 1D
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr3 = np.array([7, 8, 9])

# Łączenie
polaczone = np.concatenate((arr1, arr2, arr3))
print(f"Pierwsza: {arr1}")
print(f"Druga: {arr2}")
print(f"Trzecia: {arr3}")
print(f"Połączone: {polaczone}")
# Wynik: [1 2 3 4 5 6 7 8 9]
```

### 2️⃣ Łączenie tablic 2D - wierszami (axis=0)

```python
# Tablice 2D
macierz1 = np.array([[1, 2], [3, 4]])
macierz2 = np.array([[5, 6], [7, 8]])

print("Macierz 1:")
print(macierz1)
print("\nMacierz 2:")
print(macierz2)

# Łączenie wierszami (dodawanie wierszy)
polaczone_wiersze = np.concatenate((macierz1, macierz2), axis=0)
print(f"\nPołączone wierszami (axis=0):")
print(polaczone_wiersze)
print(f"Shape: {polaczone_wiersze.shape}")

# Wynik:
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]
```

### 3️⃣ Łączenie tablic 2D - kolumnami (axis=1)

```python
# Te same macierze co wyżej
macierz1 = np.array([[1, 2], [3, 4]])
macierz2 = np.array([[5, 6], [7, 8]])

# Łączenie kolumnami (dodawanie kolumn)
polaczone_kolumny = np.concatenate((macierz1, macierz2), axis=1)
print("Połączone kolumnami (axis=1):")
print(polaczone_kolumny)
print(f"Shape: {polaczone_kolumny.shape}")

# Wynik:
# [[1 2 5 6]
#  [3 4 7 8]]
```

## 🎯 Praktyczne przypadki użycia

### 📊 Łączenie danych z różnych źródeł

```python
# Dane sprzedaży z różnych sklepów
sklep_A = np.array([[100, 120, 90],   # Styczeń, Luty, Marzec
                    [110, 130, 95]])   # Kwiecień, Maj, Czerwiec

sklep_B = np.array([[80, 90, 85], 
                    [95, 100, 105]])

sklep_C = np.array([[120, 140, 130],
                    [135, 150, 145]])

print("Sklep A:")
print(sklep_A)
print("Sklep B:")
print(sklep_B)
print("Sklep C:")
print(sklep_C)

# Łączenie danych wszystkich sklepów
wszystkie_sklepy = np.concatenate((sklep_A, sklep_B, sklep_C), axis=0)
print(f"\nWszystkie sklepy razem:")
print(wszystkie_sklepy)
print(f"Shape: {wszystkie_sklepy.shape}")  # (6, 3)
```

### 🎯 Łączenie features w ML

```python
# Różne typy cech
cechy_demograficzne = np.array([[25, 1, 50000],    # wiek, płeć, dochód
                                [30, 0, 60000],
                                [35, 1, 75000]])

cechy_behawioralne = np.array([[5, 2],     # liczba zakupów, zwrotów
                               [8, 1],
                               [12, 0]])

cechy_geograficzne = np.array([[1],  # kod regionu
                               [2],
                               [1]])

print(f"Demograficzne: {cechy_demograficzne.shape}")
print(f"Behawioralne: {cechy_behawioralne.shape}")
print(f"Geograficzne: {cechy_geograficzne.shape}")

# Połączenie wszystkich cech
wszystkie_cechy = np.concatenate((cechy_demograficzne, 
                                  cechy_behawioralne, 
                                  cechy_geograficzne), axis=1)

print(f"\nWszystkie cechy: {wszystkie_cechy.shape}")
print("Kompletny dataset:")
print(wszystkie_cechy)
```

### 📈 Łączenie szeregów czasowych

```python
# Dane z różnych okresów
q1 = np.array([100, 105, 110])  # Q1
q2 = np.array([115, 120, 125])  # Q2
q3 = np.array([130, 125, 135])  # Q3
q4 = np.array([140, 145, 150])  # Q4

# Cały rok
caly_rok = np.concatenate((q1, q2, q3, q4))
print(f"Q1: {q1}")
print(f"Q2: {q2}")
print(f"Q3: {q3}")
print(f"Q4: {q4}")
print(f"Cały rok: {caly_rok}")
print(f"Długość: {len(caly_rok)} miesięcy")
```

## 🔍 Zaawansowane użycie

### 1️⃣ Łączenie tablic 3D

```python
# Tablice 3D (np. batch obrazów RGB)
batch1 = np.random.randint(0, 255, (2, 32, 32, 3))  # 2 obrazy 32x32 RGB
batch2 = np.random.randint(0, 255, (3, 32, 32, 3))  # 3 obrazy 32x32 RGB

print(f"Batch 1: {batch1.shape}")
print(f"Batch 2: {batch2.shape}")

# Łączenie batchów
duzy_batch = np.concatenate((batch1, batch2), axis=0)
print(f"Duży batch: {duzy_batch.shape}")  # (5, 32, 32, 3)
```

### 2️⃣ Różne typy danych

```python
# NumPy automatycznie znajdzie wspólny typ
int_array = np.array([1, 2, 3])
float_array = np.array([4.5, 5.5, 6.5])

# Wszystko zostanie skonwertowane do float
mixed = np.concatenate((int_array, float_array))
print(f"Mieszane typy: {mixed}")
print(f"Typ wyniku: {mixed.dtype}")  # float64
```

### 3️⃣ Wykorzystanie parametru out

```python
# Przygotowanie miejsca na wynik
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# Predefiniowana tablica wynikowa
wynik = np.empty(6, dtype=int)

# Łączenie z zapisem do przygotowanej tablicy
np.concatenate((arr1, arr2), out=wynik)
print(f"Wynik: {wynik}")
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ Niepasujące wymiary

```python
# BŁĄD - różne wymiary
arr1 = np.array([[1, 2, 3]])      # (1, 3)
arr2 = np.array([[4, 5]])         # (1, 2)

try:
    blad = np.concatenate((arr1, arr2), axis=1)
except ValueError as e:
    print(f"Błąd: {e}")
    print("Nie można łączyć tablic o różnych wymiarach!")
```

### 2️⃣ Złe użycie axis

```python
arr1 = np.array([[1, 2], [3, 4]])    # (2, 2)
arr2 = np.array([[5, 6]])            # (1, 2)

# UWAGA: axis=0 wymaga zgodności w pozostałych wymiarach
try:
    # To zadziała - łączymy wiersze
    ok = np.concatenate((arr1, arr2), axis=0)
    print("OK - zgodne wymiary dla axis=0:")
    print(ok)
except ValueError as e:
    print(f"Błąd: {e}")

# To nie zadziała - różna liczba kolumn dla axis=1
arr3 = np.array([[7], [8]])  # (2, 1)
try:
    blad = np.concatenate((arr1, arr3), axis=1)
    print("To nie powinno się wydrukować!")
except ValueError as e:
    print(f"Błąd axis=1: {e}")
```

### 3️⃣ Zapomnienie o tuple

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# BŁĄD - brak nawiasów w tuple
try:
    # np.concatenate(arr1, arr2)  # ŹLE!
    pass
except:
    print("Pamiętaj o tuple: (arr1, arr2)")

# PRAWIDŁOWO
prawidlowo = np.concatenate((arr1, arr2))
print(f"Prawidłowo: {prawidlowo}")
```

## 🔗 Alternatywne funkcje

### `np.vstack()` - łączenie pionowe (vertical)
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# vstack automatycznie łączy wierszami
vstacked = np.vstack((a, b))
print("vstack:")
print(vstacked)

# Równoważne z:
equivalent = np.concatenate((a[np.newaxis, :], b[np.newaxis, :]), axis=0)
```

### `np.hstack()` - łączenie poziome (horizontal)
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# hstack automatycznie łączy kolumnami
hstacked = np.hstack((a, b))
print(f"hstack: {hstacked}")

# Równoważne z:
equivalent = np.concatenate((a, b), axis=0)  # dla 1D
```

### `np.dstack()` - łączenie głębokościowe (depth)
```python
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# dstack łączy wzdłuż 3. osi
dstacked = np.dstack((a, b))
print(f"dstack shape: {dstacked.shape}")  # (2, 2, 2)
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Sprawdzaj wymiary przed łączeniem
def safe_concatenate(arrays, axis=0):
    """Bezpieczne łączenie z sprawdzaniem wymiarów"""
    if not arrays:
        return np.array([])
    
    # Sprawdź czy wymiary się zgadzają
    first_shape = arrays[0].shape
    for i, arr in enumerate(arrays[1:], 1):
        if len(arr.shape) != len(first_shape):
            raise ValueError(f"Tablica {i} ma inną liczbę wymiarów")
            
        for j, (dim1, dim2) in enumerate(zip(first_shape, arr.shape)):
            if j != axis and dim1 != dim2:
                raise ValueError(f"Niezgodność w wymiarze {j}")
    
    return np.concatenate(arrays, axis=axis)

# 2. Używaj odpowiednich skrótów
# Zamiast np.concatenate(..., axis=0) użyj np.vstack()
# Zamiast np.concatenate(..., axis=1) użyj np.hstack()
```

### ❌ Unikaj

```python
# Nie łącz w pętli (wolne!)
arrays = [np.random.rand(10) for _ in range(100)]

# ŹLE - łączenie w pętli
# result = arrays[0]
# for arr in arrays[1:]:
#     result = np.concatenate((result, arr))

# DOBRZE - jednorazowe łączenie
result = np.concatenate(arrays)
```

## 📝 Podsumowanie

`numpy.concatenate()` to podstawowe narzędzie do łączenia tablic:

- 🔗 Łączy tablice wzdłuż określonej osi
- 📐 Wymiary muszą się zgadzać (oprócz osi łączenia)
- ⚡ Wykorzystuj `vstack()`, `hstack()`, `dstack()` dla prostych przypadków
- 🎯 Zawsze sprawdzaj wymiary przed łączeniem
- 💾 Jeden `concatenate()` jest lepszy niż łączenie w pętli

To jak składanie puzzli - części muszą do siebie pasować! 🧩🔗🧩