# 🔧 NumPy - numpy.argmax() & numpy.argmin() - Znajdowanie indeksów ekstremów

## 📚 Co to są argmax() i argmin()?

`numpy.argmax()` i `numpy.argmin()` to funkcje, które znajdują **indeksy** (pozycje) największych i najmniejszych wartości w tablicy. To jak GPS dla ekstremów - nie mówi "jakie", ale "gdzie"! 📍

## 🔧 Podstawowa składnia

```python
import numpy as np

# Podstawowa składnia
numpy.argmax(array, axis=None)  # indeks maksimum
numpy.argmin(array, axis=None)  # indeks minimum
```

## 💻 Podstawowe przykłady

```python
import numpy as np

# Tablica 1D
liczby = np.array([3, 1, 7, 2, 9, 4, 8])
print(f"Liczby: {liczby}")

# Znajdź indeksy
idx_max = np.argmax(liczby)
idx_min = np.argmin(liczby)

print(f"Indeks maksimum: {idx_max} (wartość: {liczby[idx_max]})")
print(f"Indeks minimum: {idx_min} (wartość: {liczby[idx_min]})")

# Tablica 2D
macierz = np.array([[1, 8, 3], [4, 2, 9], [7, 5, 6]])
print(f"\nMacierz:")
print(macierz)

# Globalne maksimum/minimum (spłaszczona tablica)
global_max_idx = np.argmax(macierz)
global_min_idx = np.argmin(macierz)

print(f"Globalny max indeks: {global_max_idx}")
print(f"Globalny min indeks: {global_min_idx}")

# Konwersja na współrzędne 2D
max_coords = np.unravel_index(global_max_idx, macierz.shape)
min_coords = np.unravel_index(global_min_idx, macierz.shape)
print(f"Max współrzędne: {max_coords} (wartość: {macierz[max_coords]})")
print(f"Min współrzędne: {min_coords} (wartość: {macierz[min_coords]})")
```

## 🎯 Praktyczne zastosowania

### 📊 Analiza wyników studentów

```python
# Oceny studentów z różnych przedmiotów
studenci = ['Anna', 'Jan', 'Maria', 'Piotr', 'Ewa']
oceny = np.array([
    [85, 92, 78],  # Anna: Mat, Fiz, Chem
    [76, 88, 85],  # Jan
    [94, 76, 91],  # Maria  
    [67, 85, 72],  # Piotr
    [88, 79, 96]   # Ewa
])
przedmioty = ['Matematyka', 'Fizyka', 'Chemia']

print("Oceny studentów:")
for i, student in enumerate(studenci):
    print(f"{student}: {oceny[i]}")

# Najlepszy student w każdym przedmiocie
for j, przedmiot in enumerate(przedmioty):
    najlepszy_idx = np.argmax(oceny[:, j])
    najgorsza_idx = np.argmin(oceny[:, j])
    
    print(f"\n{przedmiot}:")
    print(f"  Najlepszy: {studenci[najlepszy_idx]} ({oceny[najlepszy_idx, j]})")
    print(f"  Najgorszy: {studenci[najgorsza_idx]} ({oceny[najgorsza_idx, j]})")

# Najlepszy przedmiot każdego studenta
for i, student in enumerate(studenci):
    najlepszy_przedmiot_idx = np.argmax(oceny[i, :])
    print(f"{student} najlepszy w: {przedmioty[najlepszy_przedmiot_idx]} ({oceny[i, najlepszy_przedmiot_idx]})")
```

### 💰 Analiza sprzedaży

```python
# Sprzedaż miesięczna różnych produktów
produkty = ['Laptop', 'Telefon', 'Tablet', 'Słuchawki']
miesiace = ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze']

sprzedaz = np.array([
    [120, 150, 180, 140, 200, 190],  # Laptop
    [300, 280, 350, 400, 380, 420],  # Telefon  
    [80, 90, 110, 95, 120, 100],     # Tablet
    [450, 500, 480, 520, 510, 530]   # Słuchawki
])

print("Sprzedaż produktów:")
for i, produkt in enumerate(produkty):
    print(f"{produkt}: {sprzedaz[i]}")

# Najlepszy miesiąc dla każdego produktu
print(f"\nNajlepsze miesiące:")
for i, produkt in enumerate(produkty):
    najlepszy_miesiac_idx = np.argmax(sprzedaz[i, :])
    najgorszy_miesiac_idx = np.argmin(sprzedaz[i, :])
    
    print(f"{produkt}:")
    print(f"  Najlepszy: {miesiace[najlepszy_miesiac_idx]} ({sprzedaz[i, najlepszy_miesiac_idx]} szt)")
    print(f"  Najgorszy: {miesiace[najgorszy_miesiac_idx]} ({sprzedaz[i, najgorszy_miesiac_idx]} szt)")

# Najlepszy produkt w każdym miesiącu
print(f"\nNajlepsze produkty w miesiącach:")
for j, miesiac in enumerate(miesiace):
    najlepszy_produkt_idx = np.argmax(sprzedaz[:, j])
    print(f"{miesiac}: {produkty[najlepszy_produkt_idx]} ({sprzedaz[najlepszy_produkt_idx, j]} szt)")
```

## 🔍 Zaawansowane użycie

### 1️⃣ Z osią (axis parameter)

```python
# Dane 3D - sprzedaż (produkty x miesiące x regiony)
np.random.seed(42)
sprzedaz_3d = np.random.randint(50, 500, (3, 4, 2))  # 3 produkty, 4 miesiące, 2 regiony

print(f"Sprzedaż 3D shape: {sprzedaz_3d.shape}")
print(f"Dane:\n{sprzedaz_3d}")

# Max indeksy wzdłuż różnych osi
max_axis0 = np.argmax(sprzedaz_3d, axis=0)  # najlepszy produkt
max_axis1 = np.argmax(sprzedaz_3d, axis=1)  # najlepszy miesiąc  
max_axis2 = np.argmax(sprzedaz_3d, axis=2)  # najlepszy region

print(f"\nNajlepsze produkty (axis=0):\n{max_axis0}")
print(f"Najlepsze miesiące (axis=1):\n{max_axis1}")
print(f"Najlepsze regiony (axis=2):\n{max_axis2}")
```

### 2️⃣ Kilka największych/najmniejszych

```python
# Znajdź kilka najlepszych
wyniki = np.array([85, 92, 78, 96, 88, 91, 73, 89])
studenci = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Sortowanie indeksów (od największego)
sorted_indices = np.argsort(wyniki)[::-1]

print("Ranking studentów:")
for i, idx in enumerate(sorted_indices[:5]):  # top 5
    print(f"{i+1}. Student {studenci[idx]}: {wyniki[idx]} pkt")

# Alternatywnie - argpartition dla top N
n_top = 3
top_indices = np.argpartition(wyniki, -n_top)[-n_top:]
top_indices_sorted = top_indices[np.argsort(wyniki[top_indices])[::-1]]

print(f"\nTop {n_top} (argpartition):")
for i, idx in enumerate(top_indices_sorted):
    print(f"{i+1}. Student {studenci[idx]}: {wyniki[idx]} pkt")
```

## ⚠️ Częste błędy

### 1️⃣ Mylenie argmax z max

```python
dane = np.array([10, 5, 20, 15])

# argmax zwraca INDEKS
idx = np.argmax(dane)
print(f"argmax: {idx} (to jest indeks!)")

# max zwraca WARTOŚĆ
wartość = np.max(dane)
print(f"max: {wartość} (to jest wartość!)")

# Żeby dostać wartość z argmax:
wartość_z_argmax = dane[np.argmax(dane)]
print(f"Wartość przez argmax: {wartość_z_argmax}")
```

### 2️⃣ Problemy z NaN

```python
dane_nan = np.array([1.0, np.nan, 3.0, 2.0])

# argmax z NaN może dawać nieprzewidywalne wyniki
idx_max = np.argmax(dane_nan)
print(f"argmax z NaN: {idx_max} (wartość: {dane_nan[idx_max]})")

# Bezpieczniej - usuń NaN najpierw
dane_clean = dane_nan[~np.isnan(dane_nan)]
indices_clean = np.where(~np.isnan(dane_nan))[0]
idx_max_clean = np.argmax(dane_clean)
original_idx = indices_clean[idx_max_clean]

print(f"Po usunięciu NaN: {original_idx} (wartość: {dane_nan[original_idx]})")
```

## 🔗 Powiązane funkcje

```python
# Przydatne funkcje pokrewne
dane = np.array([[1, 8, 3], [4, 2, 9], [7, 5, 6]])

print("Różne funkcje min/max:")
print(f"argmax: {np.argmax(dane)}")
print(f"argmin: {np.argmin(dane)}")
print(f"max: {np.max(dane)}")  
print(f"min: {np.min(dane)}")
print(f"argsort: {np.argsort(dane.flatten())}")  # wszystkie indeksy posortowane
print(f"unravel_index: {np.unravel_index(np.argmax(dane), dane.shape)}")  # 2D coords
print(f"where max: {np.where(dane == np.max(dane))}")  # wszystkie pozycje max
```

## 📝 Podsumowanie

`argmax()` i `argmin()` to narzędzia do znajdowania pozycji ekstremów:

- 📍 Zwracają **indeksy**, nie wartości
- 🎯 `axis=None` - globalny ekstremat (spłaszczona tablica)
- 📊 `axis=0,1,2...` - ekstrematy wzdłuż konkretnej osi
- 🔧 Użyj `np.unravel_index()` dla współrzędnych 2D/3D
- ⚠️ Uważaj na NaN - może dawać nieprzewidywalne wyniki
- 🏆 Idealne do rankingów, znajdowania najlepszych/najgorszych

To jak GPS dla danych - wskazuje dokładnie gdzie są skarby! 💎📍