# 🔍 NumPy - numpy.where() - Warunki i selekcja

## 📚 Co to jest numpy.where()?

`numpy.where()` to super funkcja, która pozwala robić warunki "jeśli-to-tamto" na całych tablicach naraz! To jak magiczna różdżka, która mówi "jeśli prawda, to A, jeśli fałsz, to B" dla każdego elementu tablicy 🪄

## 🔧 Podstawowa składnia

```python
import numpy as np

# Podstawowe formy
numpy.where(condition, x, y)  # Jeśli condition, to x, inaczej y
numpy.where(condition)        # Tylko indeksy gdzie condition=True
```

## 💻 Praktyczne przykłady

### 1️⃣ Podstawowe warunki (if-else dla tablic)

```python
import numpy as np

# Podstawowa tablica
liczby = np.array([1, 5, 3, 8, 2, 9, 4, 6, 7])
print(f"Liczby: {liczby}")

# Jeśli liczba > 5, to "DUŻA", inaczej "mała"
wynik = np.where(liczby > 5, "DUŻA", "mała")
print(f"Wynik: {wynik}")

# Z liczbami - jeśli > 5, to pomnóż przez 2, inaczej zostaw
podwojone = np.where(liczby > 5, liczby * 2, liczby)
print(f"Podwojone duże: {podwojone}")
```

### 2️⃣ Znajdowanie indeksów (tylko condition)

```python
# Ta sama tablica
liczby = np.array([1, 5, 3, 8, 2, 9, 4, 6, 7])
print(f"Liczby: {liczby}")

# Znajdź indeksy gdzie liczba > 5
indeksy = np.where(liczby > 5)
print(f"Indeksy liczb > 5: {indeksy[0]}")  # (array([3, 5, 7, 8]),)

# Użyj indeksów do wyciągnięcia wartości
duze_liczby = liczby[indeksy]
print(f"Duże liczby: {duze_liczby}")
```

### 3️⃣ Tablice 2D

```python
# Macierz 3x3
macierz = np.array([[1, 8, 3], 
                    [4, 5, 9], 
                    [2, 7, 6]])

print("Macierz:")
print(macierz)

# Zastąp liczby > 5 przez 99, inne przez 0
zastapiona = np.where(macierz > 5, 99, 0)
print(f"\nZastąpiona (>5 → 99, inne → 0):")
print(zastapiona)

# Znajdź pozycje (współrzędne) liczb > 5
pozycje = np.where(macierz > 5)
print(f"\nWspółrzędne >5:")
print(f"Wiersze: {pozycje[0]}")
print(f"Kolumny: {pozycje[1]}")

# Pokaż wartości na tych pozycjach
wartosci = macierz[pozycje]
print(f"Wartości >5: {wartosci}")
```

## 🎯 Praktyczne przypadki użycia

### 📊 Przetwarzanie danych sprzedażowych

```python
# Dane sprzedaży miesięczne
sprzedaz = np.array([12000, 15000, 8000, 18000, 22000, 9000, 
                     16000, 19000, 11000, 21000, 13000, 17000])

miesiace = np.array(['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze',
                     'Lip', 'Sie', 'Wrz', 'Paź', 'Lis', 'Gru'])

print("Sprzedaż miesięczna:")
for m, s in zip(miesiace, sprzedaz):
    print(f"{m}: {s}")

# Klasyfikuj wyniki
# >20000 = "Świetnie", 15000-20000 = "Dobrze", <15000 = "Słabo"
ocena = np.where(sprzedaz > 20000, "Świetnie", 
                 np.where(sprzedaz >= 15000, "Dobrze", "Słabo"))

print(f"\nOceny miesięcy:")
for m, s, o in zip(miesiace, sprzedaz, ocena):
    print(f"{m}: {s} - {o}")

# Znajdź najlepsze miesiące (Świetnie)
najlepsze_idx = np.where(ocena == "Świetnie")
najlepsze_miesiace = miesiace[najlepsze_idx]
print(f"\nNajlepsze miesiące: {najlepsze_miesiace}")
```

### 🌡️ Analiza temperatur

```python
# Temperatury w ciągu miesiąca
temperatury = np.array([2, 5, -1, 8, 12, 15, 18, 20, 17, 14, 
                        9, 6, 3, 0, -3, 1, 7, 11, 16, 19, 
                        22, 25, 23, 18, 13, 8, 4, 2, -1, 3])

print(f"Średnia temperatura: {np.mean(temperatury):.1f}°C")

# Klasyfikuj dni
# >20°C = "Ciepło", 10-20°C = "Miło", 0-10°C = "Chłodno", <0°C = "Mróz"
kategorie = np.where(temperatury > 20, "Ciepło",
                     np.where(temperatury >= 10, "Miło",
                              np.where(temperatury >= 0, "Chłodno", "Mróz")))

# Policz dni w każdej kategorii
unique, counts = np.unique(kategorie, return_counts=True)
print(f"\nRozkład dni:")
for kat, ilosc in zip(unique, counts):
    print(f"{kat}: {ilosc} dni")

# Znajdź dni mrozowe
mrozowe_dni = np.where(temperatury < 0)[0] + 1  # +1 bo dni liczą się od 1
print(f"\nDni mrozowe: {mrozowe_dni}")
```

### 🎯 Czyszczenie danych (Data Cleaning)

```python
# Dane z błędami
dane_brudne = np.array([25, 30, -999, 28, 35, 0, 32, -999, 29, 31])
print(f"Dane brudne: {dane_brudne}")

# -999 i 0 to błędne wartości, zastąp średnią
# Najpierw znajdź dobre wartości
dobre_wartosci = dane_brudne[(dane_brudne != -999) & (dane_brudne != 0)]
srednia = np.mean(dobre_wartosci)
print(f"Średnia z dobrych wartości: {srednia:.1f}")

# Zastąp błędne wartości średnią
dane_czyste = np.where((dane_brudne == -999) | (dane_brudne == 0), 
                       srednia, dane_brudne)

print(f"Dane czyste: {dane_czyste}")

# Alternatywnie - usuń błędne wartości
indeksy_dobrych = np.where((dane_brudne != -999) & (dane_brudne != 0))
tylko_dobre = dane_brudne[indeksy_dobrych]
print(f"Tylko dobre dane: {tylko_dobre}")
```

## 🔍 Zaawansowane użycie

### 1️⃣ Złożone warunki

```python
# Dane studentów: [wiek, ocena, frekwencja%]
studenci = np.array([[20, 4.5, 95], 
                     [19, 3.2, 85], 
                     [21, 4.8, 98], 
                     [18, 2.1, 60], 
                     [22, 4.0, 90]])

print("Studenci [wiek, ocena, frekwencja%]:")
print(studenci)

# Złożony warunek: ocena >= 4.0 AND frekwencja >= 90%
dobry_student = (studenci[:, 1] >= 4.0) & (studenci[:, 2] >= 90)

# Znajdź dobrych studentów
indeksy_dobrych = np.where(dobry_student)
dobrzy_studenci = studenci[indeksy_dobrych]

print(f"\nDobrzy studenci:")
print(dobrzy_studenci)

# Przyznaj stypendium (1000 dla dobrych, 0 dla innych)
stypendium = np.where(dobry_student, 1000, 0)
print(f"\nStypendium: {stypendium}")
```

### 2️⃣ Wielopoziomowe warunki

```python
# Oceny z egzaminu
oceny = np.array([95, 87, 76, 68, 92, 55, 78, 85, 91, 62])
print(f"Oceny: {oceny}")

# System oceniania:
# 90-100: A, 80-89: B, 70-79: C, 60-69: D, <60: F
stopnie = np.where(oceny >= 90, 'A',
                   np.where(oceny >= 80, 'B',
                            np.where(oceny >= 70, 'C',
                                     np.where(oceny >= 60, 'D', 'F'))))

print(f"Stopnie: {stopnie}")

# Policz każdy stopień
for stopien in ['A', 'B', 'C', 'D', 'F']:
    ilosc = np.sum(stopnie == stopien)
    print(f"Stopień {stopien}: {ilosc}")
```

### 3️⃣ Warunki na podstawie innych tablic

```python
# Dane pogodowe
temperatura = np.array([25, 30, 18, 35, 22, 28, 15])
wiatr = np.array([5, 15, 8, 3, 12, 7, 20])  # km/h
deszcz = np.array([0, 0, 5, 0, 2, 0, 8])    # mm

print("Pogoda [temp, wiatr, deszcz]:")
for i in range(len(temperatura)):
    print(f"Dzień {i+1}: {temperatura[i]}°C, {wiatr[i]}km/h, {deszcz[i]}mm")

# Idealne warunki: temp 20-30°C, wiatr <10km/h, brak deszczu
idealne = (temperatura >= 20) & (temperatura <= 30) & (wiatr < 10) & (deszcz == 0)

dni_idealne = np.where(idealne)[0] + 1
print(f"\nIdealne dni: {dni_idealne}")

# Rekomendacja aktywności
aktywnosc = np.where(idealne, "Piknik",
                     np.where(temperatura > 30, "Plaża",
                              np.where(deszcz > 0, "Dom", "Spacer")))

print(f"\nRekomendacje:")
for i, akt in enumerate(aktywnosc):
    print(f"Dzień {i+1}: {akt}")
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ Mieszanie & i and

```python
arr = np.array([1, 2, 3, 4, 5])

# ŹLE - Python 'and' nie działa z tablicami
try:
    # wrong = np.where((arr > 2) and (arr < 5), "OK", "NO")  # BŁĄD!
    pass
except ValueError as e:
    print(f"Błąd z 'and': Użyj & zamiast and")

# DOBRZE - NumPy & z nawiasami
correct = np.where((arr > 2) & (arr < 5), "OK", "NO")
print(f"Poprawnie: {correct}")
```

### 2️⃣ Zapomnienie nawiasów

```python
arr = np.array([1, 2, 3, 4, 5])

# ŹLE - brak nawiasów może dać nieoczekiwany wynik
# wrong = np.where(arr > 2 & arr < 5, "OK", "NO")  # Błędny priorytet!

# DOBRZE - zawsze używaj nawiasów
correct = np.where((arr > 2) & (arr < 5), "OK", "NO")
print(f"Z nawiasami: {correct}")
```

### 3️⃣ Różne typy danych

```python
# NumPy będzie próbować dopasować typy
arr = np.array([1, 2, 3, 4, 5])

# To może dać nieoczekiwany wynik
mixed = np.where(arr > 3, "duże", arr)
print(f"Mieszane typy: {mixed}")  # Wszystko będzie stringiem!
print(f"Typ: {mixed.dtype}")

# Lepiej być spójnym
int_result = np.where(arr > 3, 99, arr)  # Liczby
str_result = np.where(arr > 3, "duże", "małe")  # Stringi
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Używaj nawiasów dla złożonych warunków
dane = np.array([1, 2, 3, 4, 5])
good = np.where((dane > 2) & (dane < 5), "środek", "krawędź")

# 2. Bądź spójny z typami danych
consistent = np.where(dane > 3, 1, 0)  # Wszystko int

# 3. Używaj zmiennych dla czytelności
warunek = (dane > 2) & (dane < 5)
readable = np.where(warunek, "środek", "krawędź")

# 4. Dla prostych przypadków używaj boolean indexing
simple = dane[dane > 3]  # Szybsze niż np.where dla samej selekcji
```

### ❌ Unikaj

```python
# Nie używaj where tam gdzie wystarczy boolean indexing
arr = np.array([1, 2, 3, 4, 5])

# ŹLE - niepotrzebnie skomplikowane
# slow = arr[np.where(arr > 3)]

# DOBRZE - proste i szybkie
fast = arr[arr > 3]
```

## 🔗 Powiązane funkcje

- `np.select()` - wielokrotne warunki (alternatywa dla zagnieżdżonych where)
- `np.choose()` - wybór z tablicy opcji
- Boolean indexing: `arr[arr > 5]`
- `np.nonzero()` - indeksy niezerowych elementów
- `np.argwhere()` - współrzędne niezerowych elementów

## 📚 Przykład z np.select()

```python
# Alternatywa dla zagnieżdżonych where
oceny = np.array([95, 87, 76, 68, 92, 55])

# Zamiast zagnieżdżonych where:
warunki = [
    oceny >= 90,
    oceny >= 80,
    oceny >= 70,
    oceny >= 60
]

wybory = ['A', 'B', 'C', 'D']

stopnie = np.select(warunki, wybory, default='F')
print(f"Z np.select(): {stopnie}")
```

## 📝 Podsumowanie

`numpy.where()` to potężne narzędzie do warunków:

- 🔍 Dwie formy: z wyborem wartości i tylko indeksy
- ⚡ Działa na całych tablicach naraz (vectorized)
- 🎯 Używaj `&` i `|` zamiast `and` i `or`
- 📐 Zawsze używaj nawiasów w złożonych warunkach
- 🧹 Świetne do czyszczenia danych i klasyfikacji

To jak mieć osobistego asystenta, który przegląda każdy element i podejmuje decyzje! 🤖✨