## 🔢 NumPy - Funkcje matematyczne

_Zaawansowane funkcje matematyczne i statystyczne_

---

### 📊 Funkcje statystyczne

#### Podstawowe statystyki

```python
import numpy as np

data = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])

# Miary tendencji centralnej
print(f"Średnia: {np.mean(data)}")           # 11.0
print(f"Mediana: {np.median(data)}")         # 11.0
print(f"Percentyl 25: {np.percentile(data, 25)}")  # 5.5
print(f"Percentyl 75: {np.percentile(data, 75)}")  # 16.5

# Miary rozproszenia
print(f"Wariancja: {np.var(data)}")          # 33.0
print(f"Odchylenie std: {np.std(data)}")     # 5.74
print(f"Rozstęp: {np.ptp(data)}")            # 18 (max - min)

# Wartości ekstremalne
print(f"Minimum: {np.min(data)}")            # 2
print(f"Maksimum: {np.max(data)}")           # 20
print(f"Indeks min: {np.argmin(data)}")      # 0
print(f"Indeks max: {np.argmax(data)}")      # 9
```

#### Statystyki wielowymiarowe

```python
# Dane 2D
matrix = np.array([[1, 2, 3], 
                   [4, 5, 6], 
                   [7, 8, 9]])

# Statystyki dla całej tablicy
print(f"Średnia całościowa: {np.mean(matrix)}")  # 5.0

# Statystyki wzdłuż osi
print(f"Średnia kolumn: {np.mean(matrix, axis=0)}")  # [4, 5, 6]
print(f"Średnia wierszy: {np.mean(matrix, axis=1)}") # [2, 5, 8]

# Suma kumulatywna
cumsum = np.cumsum(data)
print(f"Suma kumulatywna: {cumsum}")
# [2, 6, 12, 20, 30, 42, 56, 72, 90, 110]
```

---

### 🧮 Algebra liniowa

```python
# Macierze
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Mnożenie macierzy
matrix_mult = np.dot(A, B)  # lub A @ B
print("A × B:")
print(matrix_mult)
# [[19, 22],
#  [43, 50]]

# Transpozycja
print("Transpozycja A:")
print(A.T)

# Wyznacznik
det_A = np.linalg.det(A)
print(f"det(A) = {det_A}")  # -2.0

# Odwrotność macierzy
if det_A != 0:
    inv_A = np.linalg.inv(A)
    print("A^(-1):")
    print(inv_A)

# Wartości własne i wektory własne
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"Wartości własne: {eigenvalues}")
print(f"Wektory własne:\n{eigenvectors}")

# Rozład SVD
U, s, Vt = np.linalg.svd(A)
print(f"SVD - wartości osobliwe: {s}")
```

---

### 📈 Funkcje specjalne

```python
# Funkcje trygonometryczne
angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])

print("Kąty w radianach:", angles)
print("Sin:", np.sin(angles))
print("Cos:", np.cos(angles))
print("Tan:", np.tan(angles))

# Funkcje hiperboliczne
x = np.array([0, 1, 2])
print("Sinh:", np.sinh(x))
print("Cosh:", np.cosh(x))
print("Tanh:", np.tanh(x))

# Funkcje wykładnicze i logarytmiczne
x = np.array([1, 2, 3, 4])
print("e^x:", np.exp(x))
print("2^x:", np.power(2, x))
print("log(x):", np.log(x))      # Logarytm naturalny
print("log10(x):", np.log10(x))  # Logarytm dziesiętny
print("log2(x):", np.log2(x))    # Logarytm dwójkowy
```

---

### 📊 Interpolacja i dopasowywanie

```python
# Interpolacja liniowa
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 1, 4, 9, 16])  # y = x^2

# Wartości do interpolacji
x_interp = np.array([0.5, 1.5, 2.5])
y_interp = np.interp(x_interp, x, y)
print(f"Interpolowane wartości: {y_interp}")

# Dopasowanie wielomianu
coeffs = np.polyfit(x, y, 2)  # Stopień 2 (parabola)
print(f"Współczynniki wielomianu: {coeffs}")

# Tworzenie wielomianu z współczynników
poly = np.poly1d(coeffs)
print(f"Wartość wielomianu dla x=2.5: {poly(2.5)}")

# Pochodna wielomianu
poly_deriv = np.polyder(poly)
print(f"Pochodna wielomianu: {poly_deriv}")
```

---

### 🎲 Generatory liczb losowych

```python
# Ustawienie seed dla powtarzalności
np.random.seed(42)

# Rozkład jednostajny
uniform = np.random.uniform(0, 10, 5)  # 5 liczb z [0, 10)
print(f"Rozkład jednostajny: {uniform}")

# Rozkład normalny (Gaussa)
normal = np.random.normal(0, 1, 5)     # μ=0, σ=1
print(f"Rozkład normalny: {normal}")

# Rozkład wykładniczy
exponential = np.random.exponential(2, 5)  # λ=2
print(f"Rozkład wykładniczy: {exponential}")

# Losowe wybieranie
choices = np.random.choice([1, 2, 3, 4, 5], size=3, replace=False)
print(f"Losowe wybory: {choices}")

# Losowe permutacje
arr = np.array([1, 2, 3, 4, 5])
np.random.shuffle(arr)
print(f"Przemieszana tablica: {arr}")
```

---

### 🔍 Znajdowanie i sortowanie

```python
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

# Sortowanie
sorted_arr = np.sort(arr)
print(f"Posortowana: {sorted_arr}")

# Indeksy sortowania
sort_indices = np.argsort(arr)
print(f"Indeksy sortowania: {sort_indices}")

# Wyszukiwanie binarne (w posortowanej tablicy)
sorted_arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
index = np.searchsorted(sorted_arr, 5)
print(f"Indeks dla wartości 5: {index}")

# Elementy unikalne
unique_vals = np.unique(arr)
print(f"Unikalne wartości: {unique_vals}")

# Zliczanie unikalnych
values, counts = np.unique(arr, return_counts=True)
for val, count in zip(values, counts):
    print(f"Wartość {val}: {count} razy")
```

---

### 💻 Praktyczne zastosowania

```python
# 1. Obliczanie korelacji Pearsona
def correlation(x, y):
    mean_x, mean_y = np.mean(x), np.mean(y)
    num = np.sum((x - mean_x) * (y - mean_y))
    den = np.sqrt(np.sum((x - mean_x)**2) * np.sum((y - mean_y)**2))
    return num / den

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])
corr = correlation(x, y)
print(f"Korelacja: {corr}")

# 2. Normalizacja min-max
def minmax_normalize(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

data = np.array([10, 20, 30, 40, 50])
normalized = minmax_normalize(data)
print(f"Znormalizowane: {normalized}")

# 3. Z-score normalizacja
def zscore_normalize(arr):
    return (arr - np.mean(arr)) / np.std(arr)

zscore = zscore_normalize(data)
print(f"Z-score: {zscore}")

# 4. Moving average
def moving_average(arr, window):
    return np.convolve(arr, np.ones(window)/window, mode='valid')

time_series = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
ma3 = moving_average(time_series, 3)
print(f"Moving average (okno=3): {ma3}")
```

---

### 🎯 Następny krok

Poznasz **indexowanie i slicing w NumPy**:

- Indeksowanie jednowymiarowe i wielowymiarowe
- Fancy indexing
- Boolean indexing
- Slicing zaawansowany
- Kopiowanie vs widoki