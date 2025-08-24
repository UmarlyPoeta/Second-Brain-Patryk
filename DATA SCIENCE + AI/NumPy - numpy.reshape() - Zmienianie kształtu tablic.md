# 🔄 NumPy - numpy.reshape() - Zmienianie kształtu tablic

## 📚 Co to jest numpy.reshape()?

`numpy.reshape()` to funkcja, która zmienia kształt (shape) tablicy bez zmieniania jej danych. To jak przepakowywanie prezentów - masz te same rzeczy, ale w innym pudełku! 📦➡️📦

## 🔧 Podstawowa składnia

```python
import numpy as np

# Podstawowa składnia
numpy.reshape(array, newshape, order='C')
# LUB
array.reshape(newshape, order='C')
```

## 💻 Praktyczne przykłady

### 1️⃣ Podstawowe przekształcenia

```python
import numpy as np

# Tablica 1D -> 2D
tablica_1d = np.array([1, 2, 3, 4, 5, 6])
print(f"Oryginalna (1D): {tablica_1d}")
print(f"Shape: {tablica_1d.shape}")

# Przekształcenie na 2x3
tablica_2x3 = tablica_1d.reshape(2, 3)
print(f"\nReshape 2x3:")
print(tablica_2x3)
print(f"Shape: {tablica_2x3.shape}")

# Przekształcenie na 3x2
tablica_3x2 = tablica_1d.reshape(3, 2)
print(f"\nReshape 3x2:")
print(tablica_3x2)
print(f"Shape: {tablica_3x2.shape}")
```

### 2️⃣ Korzystanie z -1 (automatyczny rozmiar)

```python
# -1 oznacza "oblicz automatycznie"
dane = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

# Chcemy 4 kolumny, ile wierszy? NumPy obliczy samo
auto_wiersze = dane.reshape(-1, 4)
print("Auto wiersze (4 kolumny):")
print(auto_wiersze)
print(f"Shape: {auto_wiersze.shape}")

# Chcemy 3 wiersze, ile kolumn? NumPy obliczy samo
auto_kolumny = dane.reshape(3, -1)
print(f"\nAuto kolumny (3 wiersze):")
print(auto_kolumny)
print(f"Shape: {auto_kolumny.shape}")
```

### 3️⃣ Spłaszczanie tablic (flatten)

```python
# Macierz 2D -> 1D
macierz = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("Macierz 3x3:")
print(macierz)

# Spłaszczenie do 1D
splaszczona = macierz.reshape(-1)
print(f"\nSpłaszczona: {splaszczona}")
print(f"Shape: {splaszczona.shape}")
```

## 🎯 Praktyczne przypadki użycia

### 📊 Przygotowanie danych do ML

```python
# Dane obrazu 28x28 pikseli -> wektor 784 elementów
obraz_2d = np.random.randint(0, 255, (28, 28))
print(f"Obraz 2D shape: {obraz_2d.shape}")

# Dla sieci neuronowej potrzebujemy 1D
obraz_1d = obraz_2d.reshape(-1)
print(f"Obraz 1D shape: {obraz_1d.shape}")  # (784,)

# Albo batch obrazów (np. 100 obrazów)
batch_obrazow = np.random.randint(0, 255, (100, 28, 28))
batch_1d = batch_obrazow.reshape(100, -1)
print(f"Batch shape: {batch_1d.shape}")  # (100, 784)
```

### 📈 Reorganizacja danych czasowych

```python
# Dane sprzedaży - 12 miesięcy
sprzedaz = np.array([100, 120, 90, 110, 130, 140, 
                     160, 150, 170, 180, 200, 190])

# Przekształć na kwartały (4 kwartały x 3 miesiące)
kwartaly = sprzedaz.reshape(4, 3)
print("Sprzedaż po kwartałach:")
print(kwartaly)

# Suma sprzedaży w każdym kwartale
suma_kwartaly = np.sum(kwartaly, axis=1)
print(f"Suma kwartałów: {suma_kwartaly}")
```

### 🎲 Gry i symulacje

```python
# Tablica 1D reprezentująca planszę szachową
plansza_1d = np.arange(64)
print(f"Plansza 1D: {plansza_1d}")

# Przekształć na planszę 8x8
plansza_8x8 = plansza_1d.reshape(8, 8)
print("Plansza szachowa 8x8:")
print(plansza_8x8)
```

## 🔍 Zaawansowane użycie

### 1️⃣ Wielowymiarowe reshape

```python
# 3D dane (np. RGB obraz)
dane_3d = np.arange(24)
print(f"1D: {dane_3d.shape}")

# Przekształć na 2x3x4 (wysokość x szerokość x kanały)
dane_rgb = dane_3d.reshape(2, 3, 4)
print(f"3D shape: {dane_rgb.shape}")
print("3D array:")
print(dane_rgb)
```

### 2️⃣ Kolejność układania (order parameter)

```python
dane = np.array([[1, 2, 3], [4, 5, 6]])
print("Oryginalna macierz:")
print(dane)

# C-style (row-major) - domyślny
c_style = dane.reshape(-1, order='C')
print(f"C-style: {c_style}")

# Fortran-style (column-major)
f_style = dane.reshape(-1, order='F')
print(f"F-style: {f_style}")
```

### 3️⃣ Reshape z kopiowaniem vs view

```python
# Oryginalna tablica
original = np.array([1, 2, 3, 4])
print(f"Original: {original}")

# Reshape (zwykle tworzy view, nie kopię)
reshaped = original.reshape(2, 2)
print("Reshaped:")
print(reshaped)

# Zmiana w reshapowanej tablicy wpływa na oryginalną
reshaped[0, 0] = 999
print(f"Po zmianie w reshaped - original: {original}")
print("Reshaped:")
print(reshaped)
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ Niepoprawny rozmiar

```python
tablica = np.array([1, 2, 3, 4, 5])  # 5 elementów

try:
    # Próba reshape na 2x3 = 6 elementów (błąd!)
    zla_reshape = tablica.reshape(2, 3)
except ValueError as e:
    print(f"Błąd: {e}")
    print("5 elementów nie da się ułożyć w 2x3!")
```

### 2️⃣ Zapomnienie o -1

```python
# Zamiast ręcznego liczenia
dane = np.arange(100)

# Źle - trzeba liczyć
# dane.reshape(10, 10)  # Co jeśli się pomylisz?

# Dobrze - automatyczne
dane_auto = dane.reshape(-1, 10)  # NumPy obliczy wiersze
print(f"Auto shape: {dane_auto.shape}")
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Używaj -1 dla automatycznego wymiaru
dane = np.arange(24)
good_reshape = dane.reshape(-1, 6)  # Auto-oblicz wiersze

# 2. Sprawdzaj shape przed i po
print(f"Przed: {dane.shape}")
print(f"Po: {good_reshape.shape}")

# 3. Kombinuj z innymi operacjami
transposed = dane.reshape(4, 6).T  # Reshape + transpose
```

### ❌ Unikaj

```python
# Nie rób niepotrzebnych reshape
dane = np.array([[1, 2], [3, 4]])
# Źle:
# flat = dane.reshape(-1)
# back = flat.reshape(2, 2)

# Lepiej - użyj .ravel() i zachowaj oryginalny shape
flat = dane.ravel()  # Szybsze niż reshape(-1)
```

## 🔗 Powiązane funkcje

- `np.ravel()` - spłaszczenie (często szybsze niż reshape(-1))
- `np.flatten()` - spłaszczenie (zawsze kopia)
- `np.transpose()` / `.T` - transpozycja
- `np.squeeze()` - usuń wymiary o rozmiarze 1
- `np.expand_dims()` - dodaj nowy wymiar

## 📚 Przykłady z prawdziwego świata

### 🖼️ Przetwarzanie obrazów
```python
# Batch obrazów 32x32 RGB
batch_images = np.random.rand(10, 32, 32, 3)  # 10 obrazów
print(f"Batch shape: {batch_images.shape}")

# Dla niektórych algorytmów potrzeba spłaszczyć
flat_images = batch_images.reshape(10, -1)  # 10 x (32*32*3)
print(f"Flat shape: {flat_images.shape}")
```

### 📊 Analiza danych
```python
# Dane sprzedaży - 2 lata, 12 miesięcy
sprzedaz = np.random.randint(1000, 5000, 24)

# Przekształć na lata
lata = sprzedaz.reshape(2, 12)
print("Sprzedaż po latach:")
print(lata)

# Średnia miesięczna w każdym roku
srednia_rok = np.mean(lata, axis=1)
print(f"Średnia rocznie: {srednia_rok}")
```

## 📝 Podsumowanie

`numpy.reshape()` to potężne narzędzie do reorganizacji danych. Kluczowe punkty:

- 🔢 Liczba elementów musi być taka sama przed i po reshape
- 🎯 Użyj `-1` dla automatycznego obliczenia wymiaru
- ⚡ Zwykle tworzy view, nie kopię (szybkie!)
- 🎮 Przydatne w ML, analizie obrazów, reorganizacji danych
- ⚠️ Sprawdzaj zawsze wymiary przed reshape

To jak przekształcanie Lego - te same klocki, ale nowa konstrukcja! 🧱🔄🧱