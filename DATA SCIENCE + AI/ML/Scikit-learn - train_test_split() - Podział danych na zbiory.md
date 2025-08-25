# 🎯 Scikit-learn - train_test_split() - Podział danych na zbiory

## 📚 Co to jest train_test_split()?

`train_test_split()` to funkcja, która dzieli dane na zbiór treningowy i testowy. To jak podział kolekji kart na część do nauki i część do sprawdzenia - potrzebujesz obu, żeby wiedzieć jak dobrze się uczysz! 🃏📚

## 🔧 Podstawowa składnia

```python
from sklearn.model_selection import train_test_split

# Podstawowa składnia
X_train, X_test, y_train, y_test = train_test_split(
    X, y,                    # dane wejściowe i wyjściowe
    test_size=0.25,         # rozmiar zbioru testowego (25%)
    random_state=42,        # dla reprodukowalności
    stratify=None           # stratyfikacja (dla klasyfikacji)
)
```

## 💻 Praktyczne przykłady

### 1️⃣ Podstawowy podział danych

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Przykładowe dane
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], 
              [11, 12], [13, 14], [15, 16], [17, 18], [19, 20]])
y = np.array([0, 0, 1, 1, 0, 1, 0, 1, 1, 0])

print(f"Dane wejściowe X: {X.shape}")
print(f"Dane wyjściowe y: {y.shape}")
print(f"X:\n{X}")
print(f"y: {y}")

# Podział 80/20
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% na testy
    random_state=42     # stały seed
)

print(f"\nPo podziale:")
print(f"X_train: {X_train.shape}, X_test: {X_test.shape}")
print(f"y_train: {y_train.shape}, y_test: {y_test.shape}")

print(f"\nZbiór treningowy (80%):")
print(f"X_train:\n{X_train}")
print(f"y_train: {y_train}")

print(f"\nZbiór testowy (20%):")
print(f"X_test:\n{X_test}")
print(f"y_test: {y_test}")
```

### 2️⃣ Różne proporcje podziału

```python
# Różne sposoby podziału
dane_X = np.random.randn(1000, 5)  # 1000 próbek, 5 cech
dane_y = np.random.randint(0, 3, 1000)  # 3 klasy

print(f"Dataset: {dane_X.shape}")

# 70/30 split
X_train_70, X_test_30, y_train_70, y_test_30 = train_test_split(
    dane_X, dane_y, test_size=0.30, random_state=42)

print(f"\nPodział 70/30:")
print(f"Train: {X_train_70.shape[0]} próbek ({X_train_70.shape[0]/1000*100:.0f}%)")
print(f"Test:  {X_test_30.shape[0]} próbek ({X_test_30.shape[0]/1000*100:.0f}%)")

# 60/20/20 split (train/validation/test)
# Pierwszy podział: 80/20 (train+val / test)
X_temp, X_test_final, y_temp, y_test_final = train_test_split(
    dane_X, dane_y, test_size=0.20, random_state=42)

# Drugi podział: z pozostałych 80% rób 75/25 = 60/20 z oryginalnego
X_train_final, X_val, y_train_final, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42)

print(f"\nPodział 60/20/20:")
print(f"Train:      {X_train_final.shape[0]} próbek ({X_train_final.shape[0]/1000*100:.0f}%)")
print(f"Validation: {X_val.shape[0]} próbek ({X_val.shape[0]/1000*100:.0f}%)")
print(f"Test:       {X_test_final.shape[0]} próbek ({X_test_final.shape[0]/1000*100:.0f}%)")
```

### 3️⃣ Stratified split (zachowanie proporcji klas)

```python
# Niezbalansowane dane
y_unbalanced = np.array([0]*80 + [1]*15 + [2]*5)  # 80%, 15%, 5%
X_unbalanced = np.random.randn(100, 3)

print("Rozkład oryginalny:")
unique, counts = np.unique(y_unbalanced, return_counts=True)
for cls, count in zip(unique, counts):
    print(f"Klasa {cls}: {count} próbek ({count/len(y_unbalanced)*100:.1f}%)")

# Zwykły podział (może nie zachować proporcji)
X_tr_norm, X_te_norm, y_tr_norm, y_te_norm = train_test_split(
    X_unbalanced, y_unbalanced, test_size=0.3, random_state=42)

print(f"\nZwykły podział - zbiór testowy:")
unique_test, counts_test = np.unique(y_te_norm, return_counts=True)
for cls, count in zip(unique_test, counts_test):
    print(f"Klasa {cls}: {count} próbek ({count/len(y_te_norm)*100:.1f}%)")

# Stratified split (zachowuje proporcje)
X_tr_strat, X_te_strat, y_tr_strat, y_te_strat = train_test_split(
    X_unbalanced, y_unbalanced, test_size=0.3, random_state=42, 
    stratify=y_unbalanced)

print(f"\nStratified split - zbiór testowy:")
unique_strat, counts_strat = np.unique(y_te_strat, return_counts=True)
for cls, count in zip(unique_strat, counts_strat):
    print(f"Klasa {cls}: {count} próbek ({count/len(y_te_strat)*100:.1f}%)")
```

## 🎯 Praktyczne przypadki użycia

### 📊 Przygotowanie danych do klasyfikacji

```python
# Symulacja danych klientów banku
np.random.seed(42)
n_klientow = 1000

# Cechy klientów
dane_klientow = pd.DataFrame({
    'wiek': np.random.randint(18, 70, n_klientow),
    'dochod': np.random.randint(20000, 120000, n_klientow),
    'zadluzenie': np.random.randint(0, 50000, n_klientow),
    'staz_pracy': np.random.randint(0, 30, n_klientow),
    'liczba_produktow': np.random.randint(1, 8, n_klientow)
})

# Target - czy klient złożył reklamację (0/1)
# Więcej reklamacji dla młodszych z wysokim zadłużeniem
prob_reklamacji = (
    (dane_klientow['wiek'] < 30).astype(int) * 0.3 + 
    (dane_klientow['zadluzenie'] > 30000).astype(int) * 0.4 +
    np.random.random(n_klientow) * 0.3
)
dane_klientow['reklamacja'] = (prob_reklamacji > 0.5).astype(int)

print("Dataset klientów banku:")
print(dane_klientow.head())
print(f"\nRozmiar: {dane_klientow.shape}")
print(f"Reklamacje: {dane_klientow['reklamacja'].value_counts().to_dict()}")

# Przygotowanie do ML
X = dane_klientow.drop('reklamacja', axis=1)
y = dane_klientow['reklamacja']

# Podział z zachowaniem proporcji reklamacji
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.25, 
    random_state=42,
    stratify=y  # zachowaj proporcje reklamacji
)

print(f"\nPodział danych:")
print(f"Trening: {X_train.shape[0]} klientów")
print(f"Test: {X_test.shape[0]} klientów")

print(f"\nProporcje reklamacji:")
print(f"Trening: {y_train.value_counts().to_dict()}")
print(f"Test: {y_test.value_counts().to_dict()}")
```

### 🏠 Regresja - przewidywanie cen domów

```python
# Symulacja danych o domach
np.random.seed(123)
n_homes = 800

# Cechy domów
domy = pd.DataFrame({
    'powierzchnia': np.random.randint(50, 300, n_homes),
    'pokoje': np.random.randint(2, 8, n_homes),
    'wiek_domu': np.random.randint(0, 50, n_homes),
    'odleglosc_centrum': np.random.uniform(0.5, 20.0, n_homes),
    'garaz': np.random.choice([0, 1], n_homes, p=[0.3, 0.7])
})

# Cena zależy od cech (uproszczony model)
domy['cena'] = (
    domy['powierzchnia'] * 3000 +
    domy['pokoje'] * 20000 +
    (50 - domy['wiek_domu']) * 1000 +
    (20 - domy['odleglosc_centrum']) * 2000 +
    domy['garaz'] * 30000 +
    np.random.normal(0, 50000, n_homes)  # szum
).round(0)

print("Dataset domów:")
print(domy.head())
print(f"\nStatystyki ceny:")
print(domy['cena'].describe())

# Przygotowanie do regresji
X_domy = domy.drop('cena', axis=1)
y_cena = domy['cena']

# Podział 80/20
X_train_domy, X_test_domy, y_train_cena, y_test_cena = train_test_split(
    X_domy, y_cena,
    test_size=0.2,
    random_state=42
)

print(f"\nPodział danych o domach:")
print(f"Trening: {X_train_domy.shape[0]} domów")
print(f"Test: {X_test_domy.shape[0]} domów")

print(f"\nŚrednie ceny:")
print(f"Trening: {y_train_cena.mean():,.0f} PLN")
print(f"Test: {y_test_cena.mean():,.0f} PLN")
```

### 📈 Szeregi czasowe - specjalny przypadek

```python
# Dane czasowe wymagają specjalnego podejścia
# Nie możemy losowo mieszać - musimy zachować kolejność!

dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
ts_data = pd.DataFrame({
    'data': dates,
    'sprzedaz': np.random.randn(len(dates)).cumsum() + 100 + 
                np.sin(np.arange(len(dates)) * 2 * np.pi / 365) * 20  # sezonowość
})

print(f"Dane czasowe: {ts_data.shape}")
print(ts_data.head())

# Dla szeregów czasowych - podział chronologiczny (nie losowy!)
split_date = '2023-01-01'
train_mask = ts_data['data'] < split_date
test_mask = ts_data['data'] >= split_date

ts_train = ts_data[train_mask]
ts_test = ts_data[test_mask]

print(f"\nPodział czasowy:")
print(f"Trening: {ts_train.shape[0]} dni (do {split_date})")
print(f"Test: {ts_test.shape[0]} dni (od {split_date})")

# UWAGA: Nie używaj train_test_split dla danych czasowych!
# To zniszczy kolejność chronologiczną
```

## ⚠️ Częste błędy i pułapki

### 1️⃣ Niezgodne rozmiary X i y

```python
# BŁĄD - różne długości
try:
    X_bad = np.random.randn(100, 5)
    y_bad = np.random.randint(0, 2, 90)  # 90 vs 100!
    
    X_tr, X_te, y_tr, y_te = train_test_split(X_bad, y_bad, test_size=0.2)
except ValueError as e:
    print(f"Błąd: {e}")
    print("X i y muszą mieć tę samą liczbę próbek!")
```

### 2️⃣ Zapomnienie o random_state

```python
# Bez random_state - wyniki się różnią
X_demo = np.random.randn(20, 2)
y_demo = np.random.randint(0, 2, 20)

# Pierwszy podział
X_tr1, X_te1, y_tr1, y_te1 = train_test_split(X_demo, y_demo, test_size=0.5)

# Drugi podział (różny!)
X_tr2, X_te2, y_tr2, y_te2 = train_test_split(X_demo, y_demo, test_size=0.5)

print("Bez random_state - różne podziały:")
print(f"Pierwszy test: {y_te1}")
print(f"Drugi test: {y_te2}")
print(f"Identyczne? {np.array_equal(y_te1, y_te2)}")

# Z random_state - wyniki identyczne
X_tr3, X_te3, y_tr3, y_te3 = train_test_split(X_demo, y_demo, test_size=0.5, random_state=42)
X_tr4, X_te4, y_tr4, y_te4 = train_test_split(X_demo, y_demo, test_size=0.5, random_state=42)

print(f"\nZ random_state=42:")
print(f"Pierwsze uruchomienie: {y_te3}")
print(f"Drugie uruchomienie: {y_te4}")
print(f"Identyczne? {np.array_equal(y_te3, y_te4)}")
```

## 🎯 Best Practices

### ✅ Dobre praktyki

```python
# 1. Zawsze używaj random_state dla reprodukowalności
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.25, random_state=42)

# 2. Używaj stratify dla niezbalansowanych klas
if len(np.unique(y)) < 50:  # klasyfikacja
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)

# 3. Standardowy podział 80/20 lub 70/30
standard_split = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Sprawdź rozmiary po podziale
print(f"Train size: {X_tr.shape}, Test size: {X_te.shape}")
```

### ❌ Unikaj

```python
# Nie używaj dla szeregów czasowych
# train_test_split(time_series_X, time_series_y)  # ŹLE!

# Nie zapominaj o test_size
# train_test_split(X, y)  # Użyje domyślnego 25%

# Nie ignoruj niezbalansowania klas
# train_test_split(X, highly_imbalanced_y)  # Użyj stratify!
```

## 📚 Alternatywy i rozszerzenia

```python
from sklearn.model_selection import StratifiedShuffleSplit, TimeSeriesSplit

# StratifiedShuffleSplit - wielokrotne stratified splits
splitter = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
for train_idx, test_idx in splitter.split(X, y):
    X_tr_fold, X_te_fold = X[train_idx], X[test_idx]
    y_tr_fold, y_te_fold = y[train_idx], y[test_idx]
    print(f"Fold - Train: {len(train_idx)}, Test: {len(test_idx)}")

# TimeSeriesSplit - dla danych czasowych
ts_splitter = TimeSeriesSplit(n_splits=3)
for train_idx, test_idx in ts_splitter.split(X):
    print(f"Time split - Train: {len(train_idx)}, Test: {len(test_idx)}")
```

## 📝 Podsumowanie

`train_test_split()` to podstawa machine learningu:

- 🔄 Dzieli dane na zbiór treningowy i testowy
- 🎯 `test_size` określa proporcję (domyślnie 0.25)
- 🎲 `random_state` dla reprodukowalnych wyników  
- ⚖️ `stratify` zachowuje proporcje klas
- 📊 Zwraca X_train, X_test, y_train, y_test
- ⚠️ Nie dla szeregów czasowych (potrzebna chronologia)
- 🎪 Standard to 80/20 lub 70/30 split

To jak dzielenie się pizzą - część na teraz, część na potem do sprawdzenia czy była dobra! 🍕📊