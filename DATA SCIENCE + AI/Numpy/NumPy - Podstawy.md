## 🔢 NumPy - Podstawy

_Biblioteka do obliczeń naukowych w Python_

---

### 📝 Wprowadzenie do NumPy

**NumPy (Numerical Python)** to podstawowa biblioteka do obliczeń naukowych w Python, która zapewnia:

1. **N-wymiarowe tablice (ndarray)**
   - Wydajne przechowywanie danych
   - Znacznie szybsze niż listy Python
   - Jednorodne typy danych

2. **Operacje matematyczne**
   - Funkcje matematyczne na całych tablicach
   - Operacje element-wise
   - Funkcje agregujące

3. **Integracja z innymi bibliotekami**
   - Pandas, Matplotlib, Scikit-learn
   - Podstawa większości bibliotek Data Science

---

### 🚀 Instalacja i import

```python
# Instalacja
pip install numpy

# Import standardowy
import numpy as np
```

---

### 📊 Tworzenie tablic

#### Podstawowe metody

```python
# Z listy Python
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# Tablice wypełnione zerami
zeros = np.zeros(5)              # [0, 0, 0, 0, 0]
zeros_2d = np.zeros((3, 4))      # 3x4 tablica zer

# Tablice wypełnione jedynkami
ones = np.ones(5)                # [1, 1, 1, 1, 1]
ones_2d = np.ones((2, 3))        # 2x3 tablica jedynek

# Tablice z określoną wartością
full = np.full(5, 7)             # [7, 7, 7, 7, 7]
```

#### Sekwencje liczb

```python
# Sekwencja liniowa
range_arr = np.arange(0, 10, 2)      # [0, 2, 4, 6, 8]
linspace_arr = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1.0]

# Tablica losowa
random_arr = np.random.random(5)     # Losowe wartości 0-1
random_int = np.random.randint(1, 10, 5)  # Losowe int 1-9
```

---

### 🔍 Właściwości tablic

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)    # (2, 3) - wymiary
print(arr.ndim)     # 2 - liczba wymiarów
print(arr.size)     # 6 - liczba elementów
print(arr.dtype)    # int64 - typ danych
print(arr.itemsize) # 8 - rozmiar elementu w bajtach
```

---

### 🎯 Typy danych

```python
# Określanie typu przy tworzeniu
int_arr = np.array([1, 2, 3], dtype=np.int32)
float_arr = np.array([1, 2, 3], dtype=np.float64)
bool_arr = np.array([True, False, True], dtype=np.bool_)

# Konwersja typu
arr = np.array([1.5, 2.7, 3.1])
int_converted = arr.astype(np.int32)  # [1, 2, 3]
```

---

### ⚡ Wydajność vs listy Python

```python
import time

# Lista Python
python_list = list(range(1000000))
start = time.time()
python_squared = [x**2 for x in python_list]
python_time = time.time() - start

# NumPy array
numpy_arr = np.arange(1000000)
start = time.time()
numpy_squared = numpy_arr**2
numpy_time = time.time() - start

print(f"Python list: {python_time:.4f}s")
print(f"NumPy array: {numpy_time:.4f}s")
# NumPy jest zazwyczaj 10-100x szybszy!
```

---

### 💡 Kluczowe zalety

1. **Wydajność** - operacje wykonywane w C
2. **Wygoda** - prosta składnia dla operacji na tablicach
3. **Pamięć** - efektywne przechowywanie danych
4. **Integracja** - współpraca z innymi bibliotekami
5. **Broadcasting** - automatyczne dopasowywanie wymiarów

---

### 🎯 Następny krok

Poznasz **operacje na tablicach NumPy**:

- Indexowanie i slicing
- Operacje matematyczne
- Funkcje agregujące
- Broadcasting
- Manipulacja kształtu tablic