# 🔢 NumPy - numpy.array() - Tworzenie tablic

## 📚 Co to jest numpy.array()?

`numpy.array()` to podstawowa funkcja w NumPy, która tworzy tablice (arrays) z różnych typów danych. To jak magiczna skrzynka, która zamienia zwykłe listy Pythona w superszybkie tablice NumPy! 🎯

## 🔧 Podstawowa składnia

```python
import numpy as np

# Podstawowa składnia
numpy.array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0)
```

## 💻 Praktyczne przykłady

### 1️⃣ Tworzenie tablicy z listy

```python
import numpy as np

# Z listy liczb
lista = [1, 2, 3, 4, 5]
tablica = np.array(lista)
print(f"Lista: {lista}")
print(f"Tablica NumPy: {tablica}")
print(f"Typ: {type(tablica)}")

# Wynik:
# Lista: [1, 2, 3, 4, 5]
# Tablica NumPy: [1 2 3 4 5]
# Typ: <class 'numpy.ndarray'>
```

### 2️⃣ Tablice dwuwymiarowe (2D)

```python
# Z listy list - tworzy macierz
macierz = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("Macierz 3x3:")
print(macierz)
print(f"Kształt: {macierz.shape}")

# Wynik:
# Macierz 3x3:
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]
# Kształt: (3, 3)
```

### 3️⃣ Różne typy danych

```python
# Liczby całkowite
int_array = np.array([1, 2, 3], dtype=int)
print(f"Całkowite: {int_array}, typ: {int_array.dtype}")

# Liczby zmiennoprzecinkowe
float_array = np.array([1, 2, 3], dtype=float)
print(f"Zmiennoprzecinkowe: {float_array}, typ: {float_array.dtype}")

# Stringi
str_array = np.array(['a', 'b', 'c'])
print(f"Stringi: {str_array}, typ: {str_array.dtype}")

# Boolean
bool_array = np.array([True, False, True])
print(f"Boolean: {bool_array}, typ: {bool_array.dtype}")
```

## 🎯 Najważniejsze parametry

### `dtype` - Typ danych
```python
# Automatyczne wykrywanie typu
auto = np.array([1, 2, 3])        # int64
explicit = np.array([1, 2, 3], dtype='float32')  # float32

print(f"Auto dtype: {auto.dtype}")
print(f"Explicit dtype: {explicit.dtype}")
```

### `ndmin` - Minimalna liczba wymiarów
```python
# Wymuszenie 2D na tablicy 1D
tablica_1d = np.array([1, 2, 3])
tablica_2d = np.array([1, 2, 3], ndmin=2)

print(f"1D shape: {tablica_1d.shape}")  # (3,)
print(f"2D shape: {tablica_2d.shape}")  # (1, 3)
```

## ⚡ Dlaczego numpy.array() to super?

### 🚀 Szybkość
```python
import time

# Python lista
python_lista = list(range(1000000))
start = time.time()
suma_python = sum(python_lista)
czas_python = time.time() - start

# NumPy array
numpy_tablica = np.array(python_lista)
start = time.time()
suma_numpy = np.sum(numpy_tablica)
czas_numpy = time.time() - start

print(f"Python: {czas_python:.4f}s")
print(f"NumPy: {czas_numpy:.4f}s")
print(f"NumPy jest ~{czas_python/czas_numpy:.1f}x szybszy!")
```

### 💾 Pamięć
```python
import sys

lista = [1, 2, 3, 4, 5] * 1000
tablica = np.array(lista)

print(f"Lista Python: {sys.getsizeof(lista)} bajtów")
print(f"NumPy array: {tablica.nbytes} bajtów")
```

## 🔍 Częste przypadki użycia

### 📊 Dane z CSV
```python
# Symulacja danych z pliku
dane_csv = [
    [1.2, 2.3, 3.4],
    [4.5, 5.6, 6.7],
    [7.8, 8.9, 9.0]
]

dane_numpy = np.array(dane_csv)
print("Dane jako NumPy array:")
print(dane_numpy)

# Operacje na danych
srednia_kolumn = np.mean(dane_numpy, axis=0)
print(f"Średnia kolumn: {srednia_kolumn}")
```

### 🎲 Generowanie danych testowych
```python
# Z range
zakres = np.array(range(10))
print(f"Zakres: {zakres}")

# Z linspace (alternatywa)
liniowy = np.array(np.linspace(0, 10, 5))
print(f"Liniowy: {liniowy}")
```

## ⚠️ Częste pułapki

### 1️⃣ Mieszanie typów
```python
# NumPy automatycznie konwertuje do wspólnego typu
mieszane = np.array([1, 2.5, 3])
print(f"Wszystko będzie float: {mieszane}")  # [1.  2.5 3. ]
```

### 2️⃣ Nierówne długości
```python
# To nie zadziała jak oczekujesz!
try:
    nierowne = np.array([[1, 2], [3, 4, 5]])
    print(nierowne)  # Zostanie object array!
except:
    print("Problemy z nierównymi długościami!")
```

### 3️⃣ Pamięć vs kopia
```python
lista = [1, 2, 3]
tablica1 = np.array(lista)      # Kopia
tablica2 = np.array(tablica1)   # Domyślnie kopia

# Zmiana w oryginalnej liście nie wpływa na tablicę
lista[0] = 999
print(f"Lista: {lista}")
print(f"Tablica: {tablica1}")  # Bez zmian
```

## 🎯 Best Practices

### ✅ Dobre praktyki
```python
# 1. Zawsze określ dtype jeśli wiesz jaki potrzebujesz
dane = np.array([1, 2, 3], dtype=np.float32)

# 2. Używaj list comprehensions dla złożonych transformacji
kwadraty = np.array([x**2 for x in range(10)])

# 3. Sprawdzaj kształt po utworzeniu
print(f"Kształt: {dane.shape}")
```

### ❌ Unikaj
```python
# Nie twórz w pętli (wolne!)
slow_way = []
for i in range(1000):
    slow_way.append(np.array([i]))

# Lepiej:
fast_way = np.array(range(1000))
```

## 🔗 Powiązane funkcje

- `np.asarray()` - nie kopiuje jeśli już jest array
- `np.zeros()` - tablica zer
- `np.ones()` - tablica jedynek
- `np.empty()` - niezainicjalizowana tablica
- `np.arange()` - tablica z zakresu

## 📝 Podsumowanie

`numpy.array()` to podstawa NumPy - każda analiza danych zaczyna się od przekształcenia danych w tablice NumPy. Pamiętaj:

- 🎯 Zawsze określaj `dtype` jeśli to możliwe
- 🚀 NumPy arrays są znacznie szybsze od list Python
- 💾 Zajmują mniej pamięci
- 🔧 Umożliwiają vectoryzowane operacje
- ⚠️ Wszystkie elementy muszą być tego samego typu

To twoja brama do świata szybkich obliczeń numerycznych! 🌟