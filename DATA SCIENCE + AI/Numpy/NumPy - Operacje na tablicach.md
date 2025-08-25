## 🔢 NumPy - Operacje na tablicach

_Zaawansowane operacje i manipulacje tablicami NumPy_

---

### 📝 Operacje matematyczne

#### Operacje element-wise

```python
import numpy as np

arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([5, 6, 7, 8])

# Podstawowe operacje arytmetyczne
print(arr1 + arr2)     # [6, 8, 10, 12]
print(arr1 - arr2)     # [-4, -4, -4, -4]
print(arr1 * arr2)     # [5, 12, 21, 32]
print(arr1 / arr2)     # [0.2, 0.33, 0.43, 0.5]
print(arr1 ** 2)       # [1, 4, 9, 16]
```

#### Funkcje matematyczne

```python
arr = np.array([1, 4, 9, 16])

# Funkcje uniwersalne (ufuncs)
print(np.sqrt(arr))        # [1, 2, 3, 4]
print(np.exp(arr))         # Funkcja wykładnicza
print(np.log(arr))         # Logarytm naturalny
print(np.sin(arr))         # Funkcje trygonometryczne
print(np.abs(arr))         # Wartość bezwzględna

# Zaokrąglanie
float_arr = np.array([1.2, 2.7, 3.1, 4.9])
print(np.round(float_arr))    # [1, 3, 3, 5]
print(np.floor(float_arr))    # [1, 2, 3, 4]
print(np.ceil(float_arr))     # [2, 3, 4, 5]
```

---

### 📊 Funkcje agregujące

```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Agregacja całej tablicy
print(np.sum(arr))     # 45
print(np.mean(arr))    # 5.0
print(np.std(arr))     # 2.58 - odchylenie standardowe
print(np.var(arr))     # 6.67 - wariancja
print(np.min(arr))     # 1
print(np.max(arr))     # 9

# Agregacja wzdłuż osi
print(np.sum(arr, axis=0))   # [12, 15, 18] - suma kolumn
print(np.sum(arr, axis=1))   # [6, 15, 24] - suma wierszy
print(np.mean(arr, axis=0))  # [4, 5, 6] - średnia kolumn
```

---

### 🎯 Broadcasting

**Broadcasting** pozwala na operacje między tablicami o różnych kształtach:

```python
# Tablica 2D + skalar
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
result = arr_2d + 10  # Dodaje 10 do każdego elementu
print(result)  # [[11, 12, 13], [14, 15, 16]]

# Tablica 2D + tablica 1D
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
arr_1d = np.array([10, 20, 30])
result = arr_2d + arr_1d  # Dodaje [10,20,30] do każdego wiersza
print(result)  # [[11, 22, 33], [14, 25, 36]]

# Różne wymiary
arr1 = np.array([[1], [2], [3]])     # (3,1)
arr2 = np.array([10, 20, 30])        # (3,)
result = arr1 + arr2                  # Broadcasting do (3,3)
print(result)
# [[11, 21, 31],
#  [12, 22, 32],
#  [13, 23, 33]]
```

---

### 🔍 Operacje logiczne

```python
arr = np.array([1, 2, 3, 4, 5])

# Porównania element-wise
print(arr > 3)        # [False, False, False, True, True]
print(arr == 3)       # [False, False, True, False, False]
print(arr % 2 == 0)   # [False, True, False, True, False]

# Operacje logiczne na tablicach bool
bool_arr1 = np.array([True, False, True, False])
bool_arr2 = np.array([True, True, False, False])

print(np.logical_and(bool_arr1, bool_arr2))  # [True, False, False, False]
print(np.logical_or(bool_arr1, bool_arr2))   # [True, True, True, False]
print(np.logical_not(bool_arr1))             # [False, True, False, True]

# Funkcje agregujące dla warunków
print(np.any(arr > 3))    # True - czy jakikolwiek element > 3
print(np.all(arr > 0))    # True - czy wszystkie elementy > 0
```

---

### ⚙️ Manipulacja kształtu

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# Zmiana kształtu
reshaped = arr.reshape(3, 2)  # Z (2,3) na (3,2)
print(reshaped)
# [[1, 2],
#  [3, 4],
#  [5, 6]]

# Spłaszczenie
flattened = arr.flatten()     # [1, 2, 3, 4, 5, 6]
raveled = arr.ravel()         # [1, 2, 3, 4, 5, 6] - widok, nie kopia

# Dodawanie wymiarów
expanded = np.expand_dims(arr, axis=0)  # Dodaje wymiar na początku
print(expanded.shape)  # (1, 2, 3)

# Usuwanie wymiarów o rozmiarze 1
squeezed = np.squeeze(expanded)  # Usuwa wymiary = 1
print(squeezed.shape)  # (2, 3)
```

---

### 🔄 Operacje na osiach

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

# Transpozycja
transposed = arr.T  # lub arr.transpose()
print(transposed)
# [[1, 4],
#  [2, 5],
#  [3, 6]]

# Łączenie tablic
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

# Łączenie wzdłuż osi 0 (wiersze)
vertical = np.concatenate([arr1, arr2], axis=0)
# lub: np.vstack([arr1, arr2])

# Łączenie wzdłuż osi 1 (kolumny)
horizontal = np.concatenate([arr1, arr2], axis=1)
# lub: np.hstack([arr1, arr2])
```

---

### 💻 Praktyczne przykłady

```python
# Obliczanie odległości euklidesowej
point1 = np.array([1, 2])
point2 = np.array([4, 6])
distance = np.sqrt(np.sum((point1 - point2)**2))
print(f"Odległość: {distance}")

# Normalizacja danych
data = np.array([1, 2, 3, 4, 5])
normalized = (data - np.mean(data)) / np.std(data)
print(f"Znormalizowane: {normalized}")

# Znajdowanie indeksów spełniających warunek
arr = np.array([1, 5, 3, 8, 2, 7])
indices = np.where(arr > 4)
print(f"Indeksy elementów > 4: {indices[0]}")  # [1, 3, 5]
print(f"Wartości > 4: {arr[indices]}")         # [5, 8, 7]
```

---

### 🎯 Następny krok

Poznasz **funkcje matematyczne NumPy**:

- Funkcje statystyczne
- Algebra liniowa
- Transformaty Fouriera
- Funkcje specjalne
- Operacje na wielomianach