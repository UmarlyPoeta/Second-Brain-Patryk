# 🔢 NumPy - numpy.sort() - Sortowanie tablic

## 📚 Co to jest numpy.sort()?

`numpy.sort()` to funkcja, która sortuje elementy tablicy w określonej kolejności. To jak porządkowanie książek na półce - możesz ustawić je alfabetycznie, od najmniejszej do największej, itp! 📚⬆️

## 🔧 Podstawowa składnia

```python
import numpy as np

# Podstawowa składnia
numpy.sort(array, axis=-1, kind=None, order=None)
# LUB (metoda tablicy)
array.sort()  # sortuje w miejscu (in-place)
```

## 💻 Praktyczne przykłady

### 1️⃣ Sortowanie podstawowe

```python
import numpy as np

# Tablica 1D
liczby = np.array([64, 34, 25, 12, 22, 11, 90])
print(f"Oryginalne: {liczby}")

# Sortowanie (tworzy kopię)
posortowane = np.sort(liczby)
print(f"Posortowane: {posortowane}")
print(f"Oryginalne (bez zmian): {liczby}")

# Sortowanie w miejscu (zmienia oryginalną tablicę)
liczby.sort()
print(f"Po sort(): {liczby}")
```

### 2️⃣ Sortowanie malejące

```python
# Dla sortowania malejącego użyj [::-1]
liczby = np.array([64, 34, 25, 12, 22, 11, 90])
print(f"Oryginalne: {liczby}")

# Sortowanie rosnące, potem odwrócenie
malejace = np.sort(liczby)[::-1]
print(f"Malejąco: {malejace}")

# Alternatywnie z -
minus_sort = -np.sort(-liczby)
print(f"Przez minus: {minus_sort}")
```

### 3️⃣ Sortowanie stringów

```python
# Sortowanie alfabetyczne
imiona = np.array(['Zofia', 'Anna', 'Marek', 'Piotr', 'Ewa'])
print(f"Oryginalne: {imiona}")

posortowane_imiona = np.sort(imiona)
print(f"Alfabetycznie: {posortowane_imiona}")

# Sortowanie po długości (trzeba użyć argsort + key function)
dlugosci = np.array([len(name) for name in imiona])
indeksy_dlugosci = np.argsort(dlugosci)
po_dlugosci = imiona[indeksy_dlugosci]
print(f"Po długości: {po_dlugosci}")
```

## 🎯 Sortowanie tablic 2D (axis parameter)

### 1️⃣ Sortowanie wierszy (axis=1)

```python
# Macierz 3x4
macierz = np.array([[64, 34, 25, 12],
                    [90, 88, 76, 50],
                    [23, 45, 67, 89]])

print("Oryginalna macierz:")
print(macierz)

# Sortuj każdy wiersz osobno
wiersze_sort = np.sort(macierz, axis=1)
print(f"\nWiersze posortowane:")
print(wiersze_sort)
```

### 2️⃣ Sortowanie kolumn (axis=0)

```python
# Ta sama macierz
print("Oryginalna macierz:")
print(macierz)

# Sortuj każdą kolumnę osobno
kolumny_sort = np.sort(macierz, axis=0)
print(f"\nKolumny posortowane:")
print(kolumny_sort)
```

### 3️⃣ Sortowanie całej macierzy (spłaszczonej)

```python
# Sortowanie wszystkich elementów
wszystko_sort = np.sort(macierz, axis=None)
print(f"\nWszystkie elementy posortowane:")
print(wszystko_sort)
```

## 🔍 Praktyczne przypadki użycia

### 📊 Analiza wyników egzaminów

```python
# Wyniki egzaminów studentów (wiersze=studenci, kolumny=przedmioty)
wyniki = np.array([[85, 92, 78, 88],  # Student 1: Mat, Fiz, Chem, Bio
                   [76, 84, 90, 82],  # Student 2
                   [94, 88, 85, 91],  # Student 3
                   [68, 72, 75, 79],  # Student 4
                   [89, 95, 87, 93]]) # Student 5

przedmioty = ['Matematyka', 'Fizyka', 'Chemia', 'Biologia']

print("Wyniki egzaminów:")
print(wyniki)

# Sortuj oceny każdego studenta (najgorsze → najlepsze)
wyniki_sort = np.sort(wyniki, axis=1)
print(f"\nWyniki studentów posortowane (rosnąco):")
print(wyniki_sort)

# Najlepsze i najgorsze wyniki każdego studenta
print(f"\nAnaliza per student:")
for i in range(len(wyniki)):
    student_wyniki = wyniki_sort[i]
    najgorszy = student_wyniki[0]
    najlepszy = student_wyniki[-1]
    srednia = np.mean(student_wyniki)
    print(f"Student {i+1}: najgorszy={najgorszy}, najlepszy={najlepszy}, średnia={srednia:.1f}")

# Sortuj wyniki w każdym przedmiocie
przedmioty_sort = np.sort(wyniki, axis=0)
print(f"\nWyniki w przedmiotach (najgorsze → najlepsze):")
for j, przedmiot in enumerate(przedmioty):
    print(f"{przedmiot}: {przedmioty_sort[:, j]}")
```

### 💰 Analiza zarobków

```python
# Zarobki w różnych działach (tysiące PLN)
zarobki = np.array([
    [4.5, 5.2, 6.1, 4.8, 5.5],  # IT
    [3.2, 3.8, 4.1, 3.5, 3.9],  # Marketing
    [2.8, 3.1, 3.4, 2.9, 3.2],  # HR
    [3.5, 4.0, 4.5, 3.8, 4.2]   # Sprzedaż
])

dzialy = ['IT', 'Marketing', 'HR', 'Sprzedaż']

print("Zarobki w działach (tys. PLN):")
for i, dzial in enumerate(dzialy):
    print(f"{dzial:10}: {zarobki[i]}")

# Sortuj zarobki w każdym dziale
zarobki_sort = np.sort(zarobki, axis=1)
print(f"\nZarobki posortowane w działach:")
for i, dzial in enumerate(dzialy):
    sorted_pay = zarobki_sort[i]
    print(f"{dzial:10}: {sorted_pay}")
    print(f"           Mediana: {np.median(sorted_pay):.1f}k, Rozstęp: {sorted_pay[-1]-sorted_pay[0]:.1f}k")
```

### 🎯 Ranking i percentyle

```python
# Wyniki testów wydajności (im wyżej tym lepiej)
wydajnosc = np.array([87, 92, 78, 94, 85, 89, 76, 91, 83, 88])
print(f"Wyniki wydajności: {wydajnosc}")

# Sortuj dla analizy percentyli
wydajnosc_sort = np.sort(wydajnosc)
print(f"Posortowane: {wydajnosc_sort}")

# Oblicz percentyle
n = len(wydajnosc_sort)
percentyl_25 = wydajnosc_sort[int(0.25 * n)]
percentyl_50 = wydajnosc_sort[int(0.50 * n)]  # mediana
percentyl_75 = wydajnosc_sort[int(0.75 * n)]

print(f"25. percentyl: {percentyl_25}")
print(f"50. percentyl (mediana): {percentyl_50}")
print(f"75. percentyl: {percentyl_75}")

# Klasyfikuj wyniki
def klasyfikuj_wynik(wynik):
    if wynik >= percentyl_75:
        return "Wysoki"
    elif wynik >= percentyl_50:
        return "Średni"
    elif wynik >= percentyl_25:
        return "Niski"
    else:
        return "Bardzo niski"

print(f"\nKlasyfikacja wyników:")
for wynik in wydajnosc:
    klasa = klasyfikuj_wynik(wynik)
    print(f"Wynik {wynik}: {klasa}")
```

## 🚀 Zaawansowane sortowanie

### 1️⃣ Różne algorytmy sortowania

```python
# Różne algorytmy (kind parameter)
dane = np.random.randint(1, 100, 10)
print(f"Dane do sortowania: {dane}")

# Quicksort (domyślny, szybki dla większości przypadków)
quicksort = np.sort(dane, kind='quicksort')
print(f"Quicksort: {quicksort}")

# Mergesort (stabilny, O(n log n) zawsze)
mergesort = np.sort(dane, kind='mergesort')
print(f"Mergesort: {mergesort}")

# Heapsort (nie stabilny, ale zawsze O(n log n))
heapsort = np.sort(dane, kind='heapsort')
print(f"Heapsort: {heapsort}")

print("Wszystkie dają ten sam wynik (są posortowane!)")
```

### 2️⃣ Sortowanie struktur danych

```python
# Structured arrays
dtype = [('imie', 'U10'), ('wiek', int), ('wynagrodzenie', float)]
pracownicy = np.array([
    ('Anna', 28, 5500.0),
    ('Jan', 35, 6200.0),
    ('Maria', 24, 4800.0),
    ('Piotr', 31, 5800.0)
], dtype=dtype)

print("Pracownicy:")
print(pracownicy)

# Sortuj po wieku
po_wieku = np.sort(pracownicy, order='wiek')
print(f"\nPo wieku:")
print(po_wieku)

# Sortuj po wynagrodzeniu
po_wynagrodzeniu = np.sort(pracownicy, order='wynagrodzenie')
print(f"\nPo wynagrodzeniu:")
print(po_wynagrodzeniu)

# Sortowanie wielokryterialne (najpierw wiek, potem wynagrodzenie)
wielokryterialne = np.sort(pracownicy, order=['wiek', 'wynagrodzenie'])
print(f"\nWielokryterialne (wiek, potem wynagrodzenie):")
print(wielokryterialne)
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ sort() vs np.sort()

```python
oryginalne = np.array([3, 1, 4, 1, 5])
kopia = oryginalne.copy()

# np.sort() tworzy KOPIĘ
sorted_copy = np.sort(oryginalne)
print(f"Po np.sort() - oryginalne: {oryginalne}")  # bez zmian!
print(f"Kopia posortowana: {sorted_copy}")

# .sort() modyfikuje W MIEJSCU
kopia.sort()
print(f"Po .sort() - tablica: {kopia}")  # zmieniona!
```

### 2️⃣ Sortowanie z NaN

```python
dane_nan = np.array([3.1, np.nan, 1.5, 2.8, np.nan])
print(f"Z NaN: {dane_nan}")

posortowane = np.sort(dane_nan)
print(f"Posortowane: {posortowane}")
# NaN zawsze idą na koniec!
```

### 3️⃣ Problemy z axis

```python
macierz = np.array([[3, 1], [2, 4]])
print("Macierz 2x2:")
print(macierz)

# axis=0 (kolumny) vs axis=1 (wiersze)
print(f"axis=0 (sortuj kolumny):\n{np.sort(macierz, axis=0)}")
print(f"axis=1 (sortuj wiersze):\n{np.sort(macierz, axis=1)}")
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Używaj np.sort() jeśli nie chcesz modyfikować oryginału
original = np.array([3, 1, 4])
sorted_copy = np.sort(original)  # original bez zmian

# 2. Używaj .sort() dla oszczędności pamięci przy dużych tablicach
big_array = np.random.rand(1000000)
big_array.sort()  # modyfikuje w miejscu, oszczędza pamięć

# 3. Określaj axis dla jasności w 2D+
matrix = np.random.rand(3, 4)
rows_sorted = np.sort(matrix, axis=1)  # jasne że sortujemy wiersze

# 4. Łącz z argsort() dla indeksów
data = np.array([64, 34, 25, 12])
indices = np.argsort(data)  # indeksy sortowania
```

### ❌ Unikaj

```python
# Nie sortuj niepotrzebnie - to kosztuje czas
for i in range(1000):
    # slow = np.sort(some_array)  # jeśli nie używasz wyniku!
    pass

# Nie mieszaj sort() i np.sort()
arr = np.array([3, 1, 4])
# arr.sort()  # teraz arr jest zmienione
# result = np.sort(arr)  # już i tak posortowane!
```

## 🔗 Powiązane funkcje

- `np.argsort()` - indeksy elementów po sortowaniu
- `np.lexsort()` - sortowanie leksykograficzne (wielokryterialne)
- `np.partition()` - częściowe sortowanie (k najmniejszych)
- `np.argpartition()` - indeksy częściowego sortowania
- `np.searchsorted()` - znalezienie pozycji dla wstawienia

## 📚 Przykład z argsort()

```python
# argsort() - bardzo przydatne!
studenci = np.array(['Anna', 'Jan', 'Maria'])
oceny = np.array([85, 92, 78])

print(f"Studenci: {studenci}")
print(f"Oceny: {oceny}")

# Indeksy sortowania po ocenach (rosnąco)
indeksy = np.argsort(oceny)
print(f"Indeksy sortowania: {indeksy}")

# Sortuj studentów po ocenach
studenci_po_ocenach = studenci[indeksy]
oceny_posortowane = oceny[indeksy]

print(f"Ranking (od najgorszego):")
for student, ocena in zip(studenci_po_ocenach, oceny_posortowane):
    print(f"{student}: {ocena}")
```

## 📝 Podsumowanie

`numpy.sort()` to podstawowe narzędzie do sortowania:

- 📊 `np.sort()` tworzy kopię, `.sort()` modyfikuje w miejscu
- ⬆️ Domyślnie sortuje rosnąco, dla malejącego użyj `[::-1]`
- 📐 `axis=0` dla kolumn, `axis=1` dla wierszy, `axis=None` dla wszystkich
- 🚀 Różne algorytmy: quicksort, mergesort, heapsort
- 🔍 Łącz z `argsort()` dla sortowania powiązanych danych
- ⚠️ NaN zawsze idą na koniec

To jak sprzątanie pokoju - wszystko ma swoje miejsce w odpowiedniej kolejności! 🧹✨