# 🔍 NumPy - numpy.unique() - Znajdowanie unikalnych wartości

## 📚 Co to jest numpy.unique()?

`numpy.unique()` to funkcja, która znajduje unikalne (niepowtarzające się) wartości w tablicy. To jak sortowanie kolekcji znaczków - zostawiasz tylko jeden egzemplarz każdego rodzaju! 🎯📮

## 🔧 Podstawowa składnia

```python
import numpy as np

# Podstawowa składnia
numpy.unique(array, return_index=False, return_inverse=False, 
            return_counts=False, axis=None)
```

## 💻 Praktyczne przykłady

### 1️⃣ Podstawowe znajdowanie unikalnych wartości

```python
import numpy as np

# Tablica z powtórzeniami
dane = np.array([1, 3, 2, 3, 1, 4, 2, 1, 4, 5])
print(f"Oryginalne dane: {dane}")

# Znajdź unikalne wartości
unikalne = np.unique(dane)
print(f"Unikalne wartości: {unikalne}")
# Wynik: [1 2 3 4 5] - automatycznie posortowane!
```

### 2️⃣ Zliczanie wystąpień (return_counts=True)

```python
# Te same dane
dane = np.array([1, 3, 2, 3, 1, 4, 2, 1, 4, 5])
print(f"Dane: {dane}")

# Unikalne wartości + ile razy występują
unikalne, liczby = np.unique(dane, return_counts=True)

print(f"Unikalne: {unikalne}")
print(f"Liczby wystąpień: {liczby}")

# Ładne podsumowanie
for wartość, ilość in zip(unikalne, liczby):
    print(f"Wartość {wartość} występuje {ilość} razy")

# Wynik:
# Wartość 1 występuje 3 razy
# Wartość 2 występuje 2 razy
# Wartość 3 występuje 2 razy
# Wartość 4 występuje 2 razy
# Wartość 5 występuje 1 razy
```

### 3️⃣ Znajdowanie pierwszych wystąpień (return_index=True)

```python
dane = np.array(['A', 'B', 'A', 'C', 'B', 'A', 'D'])
print(f"Dane: {dane}")

# Unikalne + indeksy pierwszego wystąpienia
unikalne, indeksy = np.unique(dane, return_index=True)

print(f"Unikalne: {unikalne}")
print(f"Pierwsze indeksy: {indeksy}")

# Sprawdzenie
for wartość, idx in zip(unikalne, indeksy):
    print(f"'{wartość}' po raz pierwszy na pozycji {idx}: {dane[idx]}")
```

### 4️⃣ Mapowanie na unikalne (return_inverse=True)

```python
dane = np.array([1, 3, 2, 3, 1, 4, 2])
print(f"Dane: {dane}")

# Unikalne + mapowanie zwrotne
unikalne, odwrotne = np.unique(dane, return_inverse=True)

print(f"Unikalne: {unikalne}")
print(f"Odwrotne mapowanie: {odwrotne}")

# Sprawdzenie - odtworzenie oryginalnych danych
odtworzone = unikalne[odwrotne]
print(f"Odtworzone: {odtworzone}")
print(f"Czy identyczne? {np.array_equal(dane, odtworzone)}")
```

## 🎯 Praktyczne przypadki użycia

### 📊 Analiza danych klientów

```python
# Dane klientów - kategorie wiekowe
klienci_wiek = np.array(['młody', 'średni', 'młody', 'starszy', 'średni', 
                         'młody', 'starszy', 'średni', 'młody'])

print(f"Kategorie wiekowe: {klienci_wiek}")

# Analiza segmentów
kategorie, liczby = np.unique(klienci_wiek, return_counts=True)

print(f"\nAnaliza segmentów klientów:")
total = len(klienci_wiek)
for kat, ile in zip(kategorie, liczby):
    procent = (ile / total) * 100
    print(f"{kat:8}: {ile:2} klientów ({procent:4.1f}%)")

# Znajdź dominującą grupę
dominujaca_idx = np.argmax(liczby)
dominujaca_grupa = kategorie[dominujaca_idx]
print(f"\nDominująca grupa: {dominujaca_grupa}")
```

### 🎯 Czyszczenie danych

```python
# Dane z błędami i duplikatami
dane_brudne = np.array([1.5, 2.0, 1.5, -999, 3.2, 2.0, -999, 4.1, 1.5])
print(f"Dane brudne: {dane_brudne}")

# Znajdź unikalne wartości bez błędnych (-999)
czyste = dane_brudne[dane_brudne != -999]
unikalne_czyste = np.unique(czyste)

print(f"Unikalne czyste wartości: {unikalne_czyste}")

# Sprawdź jakie wartości są duplikatami
wszystkie_unikalne, liczby = np.unique(dane_brudne, return_counts=True)
duplikaty = wszystkie_unikalne[liczby > 1]

print(f"Wartości występujące więcej niż raz: {duplikaty}")
```

### 📈 Analiza sprzedaży produktów

```python
# Lista sprzedanych produktów
produkty = np.array(['Laptop', 'Mysz', 'Laptop', 'Klawiatura', 'Mysz', 
                     'Monitor', 'Laptop', 'Klawiatura', 'Mysz', 'Laptop'])

print(f"Sprzedane produkty: {produkty}")

# Analiza sprzedaży
unikalne_produkty, sprzedaz = np.unique(produkty, return_counts=True)

print(f"\nRaport sprzedaży:")
# Sortuj po liczbie sprzedaży (malejąco)
sorted_idx = np.argsort(sprzedaz)[::-1]
for i in sorted_idx:
    produkt = unikalne_produkty[i]
    ilosc = sprzedaz[i]
    print(f"{produkt:12}: {ilosc} sztuk")

# Top produkt
top_produkt = unikalne_produkty[np.argmax(sprzedaz)]
print(f"\nNajlepiej sprzedający się: {top_produkt}")
```

### 🎲 Analiza wyników eksperymentów

```python
# Wyniki rzutów kostką
rzuty = np.array([1, 3, 6, 2, 3, 1, 4, 2, 6, 1, 5, 3, 2, 4, 6, 
                  1, 3, 5, 2, 4, 6, 1, 3, 2, 5])

print(f"Rzuty kostką: {rzuty}")
print(f"Liczba rzutów: {len(rzuty)}")

# Analiza wyników
wyniki, częstotliwość = np.unique(rzuty, return_counts=True)

print(f"\nAnaliza wyników:")
for wynik, czest in zip(wyniki, częstotliwość):
    prawdopodobienstwo = czest / len(rzuty) * 100
    print(f"Wynik {wynik}: {czest:2} razy ({prawdopodobienstwo:5.1f}%)")

# Sprawdź czy kostka jest uczciwa (każdy wynik ~16.67%)
expected = len(rzuty) / 6
print(f"\nOczekiwana częstotliwość: {expected:.1f} na wynik")

# Odchylenie od oczekiwanej częstotliwości
odchylenia = np.abs(częstotliwość - expected)
max_odchylenie = np.max(odchylenia)
print(f"Maksymalne odchylenie: {max_odchylenie:.1f}")
```

## 🔍 Zaawansowane użycie

### 1️⃣ Unikalne wiersze w macierzy 2D

```python
# Macierz z duplikatami wierszy
macierz = np.array([[1, 2, 3],
                    [4, 5, 6],
                    [1, 2, 3],  # duplikat
                    [7, 8, 9],
                    [4, 5, 6]]) # duplikat

print("Oryginalna macierz:")
print(macierz)

# Znajdź unikalne wiersze (axis=0)
unikalne_wiersze = np.unique(macierz, axis=0)
print(f"\nUnikalne wiersze:")
print(unikalne_wiersze)

# Z dodatkowymi informacjami
unikalne, indeksy, odwrotne, liczby = np.unique(macierz, axis=0, 
                                                return_index=True,
                                                return_inverse=True,
                                                return_counts=True)
print(f"\nLiczby wystąpień wierszy: {liczby}")
```

### 2️⃣ Unikalne kolumny

```python
# Macierz z duplikatami kolumn
macierz = np.array([[1, 4, 1, 7],
                    [2, 5, 2, 8],
                    [3, 6, 3, 9]])

print("Oryginalna macierz:")
print(macierz)

# Znajdź unikalne kolumny (axis=1)
unikalne_kolumny = np.unique(macierz, axis=1)
print(f"\nUnikalne kolumny:")
print(unikalne_kolumny)
```

### 3️⃣ Złożone typy danych

```python
# Rekordy strukturalne
dtype = [('imie', 'U10'), ('wiek', int), ('miasto', 'U10')]
dane = np.array([('Anna', 25, 'Warszawa'),
                 ('Jan', 30, 'Kraków'),
                 ('Anna', 25, 'Warszawa'),  # duplikat
                 ('Maria', 28, 'Gdańsk')], dtype=dtype)

print("Dane:")
print(dane)

# Unikalne rekordy
unikalne_rekordy = np.unique(dane)
print(f"\nUnikalne rekordy:")
print(unikalne_rekordy)
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ Domyślne sortowanie

```python
dane = np.array([5, 1, 3, 1, 5, 2])
unikalne = np.unique(dane)

print(f"Dane: {dane}")
print(f"Unikalne (posortowane!): {unikalne}")
# unique() ZAWSZE sortuje wyniki!
```

### 2️⃣ Praca z NaN

```python
# Tablice z NaN
dane_nan = np.array([1.0, np.nan, 2.0, np.nan, 1.0])
print(f"Dane z NaN: {dane_nan}")

unikalne = np.unique(dane_nan)
print(f"Unikalne z NaN: {unikalne}")
# NaN jest traktowany jako unikalna wartość!
```

### 3️⃣ Typy danych

```python
# Różne typy mogą dać nieoczekiwane wyniki
dane_mixed = np.array([1, 1.0, 2, 2.0])
print(f"Mieszane typy: {dane_mixed}")
print(f"Dtype: {dane_mixed.dtype}")

unikalne = np.unique(dane_mixed)
print(f"Unikalne: {unikalne}")
# 1 i 1.0 to ta sama wartość po konwersji!
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Używaj return_counts dla analizy częstotliwości
dane = np.array([1, 2, 1, 3, 2, 1])
unikalne, liczby = np.unique(dane, return_counts=True)

# 2. Łącz z innymi funkcjami dla analizy
najczęstsza_wartość = unikalne[np.argmax(liczby)]

# 3. Sprawdzaj typy danych przed użyciem
print(f"Typ danych: {dane.dtype}")

# 4. Używaj axis= dla wielowymiarowych danych
# np.unique(macierz, axis=0)  # wiersze
# np.unique(macierz, axis=1)  # kolumny
```

### ❌ Unikaj

```python
# Nie oczekuj oryginalnej kolejności
dane = np.array([3, 1, 4, 1, 5])
# unique() zawsze sortuje!

# Nie używaj w pętlach dla dużych danych
# for i in range(len(big_array)):
#     uniques = np.unique(big_array[:i])  # WOLNE!
```

## 🔗 Powiązane funkcje

- `np.bincount()` - zliczanie dla liczb całkowitych
- `collections.Counter` - zliczanie w Python (może być szybsze dla małych danych)
- `pd.Series.value_counts()` - w Pandas
- `np.in1d()` / `np.isin()` - sprawdzanie członkostwa
- `np.setdiff1d()` - różnica zbiorów

## 📚 Alternatywne metody

### Collections.Counter (Python)
```python
from collections import Counter

dane = [1, 3, 2, 3, 1, 4, 2, 1]
counter = Counter(dane)

print(f"Counter: {counter}")
print(f"Najczęstszy: {counter.most_common(1)}")
```

### Pandas value_counts()
```python
import pandas as pd

dane = np.array([1, 3, 2, 3, 1, 4, 2, 1])
series = pd.Series(dane)
counts = series.value_counts()

print("Pandas value_counts:")
print(counts)
```

## 📝 Podsumowanie

`numpy.unique()` to podstawowe narzędzie do analizy unikalnych wartości:

- 🔍 Znajduje unikalne wartości (zawsze posortowane)
- 📊 `return_counts=True` dla analizy częstotliwości
- 🎯 `return_index=True` dla pierwszych wystąpień
- 🔄 `return_inverse=True` dla mapowania
- 📐 `axis=` dla tablic wielowymiarowych
- ⚠️ Uważaj na NaN i różne typy danych

To jak organizowanie biblioteki - każda książka ma swoje miejsce! 📚✨