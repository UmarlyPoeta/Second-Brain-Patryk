# ⚖️ Scikit-learn - StandardScaler - Standardyzacja danych

## 📚 Co to jest StandardScaler?

`StandardScaler` to narzędzie, które standardyzuje dane do średniej 0 i odchylenia standardowego 1. To jak ustawianie wszystkich instrumentów w orkiestrze na tę samą tonację! 🎼

## 🔧 Podstawowa składnia

```python
from sklearn.preprocessing import StandardScaler

# Tworzenie i użycie
scaler = StandardScaler()
scaler.fit(X_train)                    # naucz się parametrów
X_scaled = scaler.transform(X_train)   # zastosuj transformację
# LUB
X_scaled = scaler.fit_transform(X_train)  # jedno wywołanie
```

## 💻 Podstawowy przykład

```python
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Przykładowe dane o różnych skalach
dane = pd.DataFrame({
    'wiek': [25, 30, 45, 35, 50, 28, 42, 38],
    'dochod': [30000, 45000, 80000, 55000, 95000, 35000, 70000, 60000],
    'zadluzenie': [5000, 12000, 25000, 8000, 30000, 3000, 18000, 15000],
    'staz_pracy': [2, 5, 20, 10, 25, 3, 15, 12]
})

print("Oryginalne dane:")
print(dane)
print(f"\nStatystyki oryginalnych danych:")
print(dane.describe())

# Standardyzacja
scaler = StandardScaler()
dane_scaled = scaler.fit_transform(dane)
dane_scaled_df = pd.DataFrame(dane_scaled, columns=dane.columns)

print(f"\nDane po standardyzacji:")
print(dane_scaled_df.round(3))
print(f"\nStatystyki po standardyzacji:")
print(dane_scaled_df.describe().round(3))

print(f"\nParametry scalera:")
print(f"Średnie: {scaler.mean_.round(2)}")
print(f"Odchylenia std: {scaler.scale_.round(2)}")
```

## 🎯 Praktyczne zastosowania

### 🏦 Przygotowanie danych bankowych

```python
# Symulacja danych klientów banku
np.random.seed(42)
n_klientow = 1000

klienci_bank = pd.DataFrame({
    'wiek': np.random.randint(18, 75, n_klientow),
    'roczny_dochod': np.random.normal(50000, 20000, n_klientow),
    'zadluzenie': np.random.exponential(15000, n_klientow),
    'liczba_kart': np.random.randint(1, 6, n_klientow),
    'historia_lat': np.random.randint(0, 30, n_klientow),
    'oszczednosci': np.random.exponential(25000, n_klientow)
})

# Usuń ujemne dochody i ogranicz zadłużenie
klienci_bank['roczny_dochod'] = np.clip(klienci_bank['roczny_dochod'], 20000, 150000)
klienci_bank['zadluzenie'] = np.clip(klienci_bank['zadluzenie'], 0, 100000)
klienci_bank['oszczednosci'] = np.clip(klienci_bank['oszczednosci'], 0, 200000)

print("=== DANE BANKOWE PRZED STANDARDYZACJĄ ===")
print(klienci_bank.describe().round(0))

# Porównanie skal
print(f"\nRóżnice w skalach:")
for col in klienci_bank.columns:
    min_val = klienci_bank[col].min()
    max_val = klienci_bank[col].max()
    range_val = max_val - min_val
    print(f"{col:15}: min={min_val:8.0f}, max={max_val:8.0f}, zakres={range_val:8.0f}")

# Standardyzacja
scaler_bank = StandardScaler()
klienci_scaled = scaler_bank.fit_transform(klienci_bank)
klienci_scaled_df = pd.DataFrame(klienci_scaled, columns=klienci_bank.columns)

print(f"\n=== PO STANDARDYZACJI ===")
print(klienci_scaled_df.describe().round(3))

# Sprawdź czy średnia ≈ 0 i std ≈ 1
print(f"\nSprawdzenie standardyzacji:")
for col in klienci_scaled_df.columns:
    mean = klienci_scaled_df[col].mean()
    std = klienci_scaled_df[col].std()
    print(f"{col:15}: średnia={mean:+6.3f}, std={std:6.3f}")
```

### 🏠 Model ML - przewidywanie cen domów

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Symulacja danych o domach
np.random.seed(123)
n_houses = 1000

domy = pd.DataFrame({
    'powierzchnia': np.random.normal(120, 40),     # m²
    'pokoje': np.random.randint(2, 7),            # liczba pokoi
    'wiek': np.random.randint(0, 50),             # lata
    'odleglosc_centrum': np.random.exponential(10), # km
    'powierzchnia_dzialki': np.random.normal(500, 200) # m²
})

# Realistyczne ograniczenia
domy['powierzchnia'] = np.clip(domy['powierzchnia'], 50, 300)
domy['odleglosc_centrum'] = np.clip(domy['odleglosc_centrum'], 1, 50)
domy['powierzchnia_dzialki'] = np.clip(domy['powierzchnia_dzialki'], 200, 1500)

# Cena zależy od wszystkich cech (uproszczony model)
domy['cena'] = (
    domy['powierzchnia'] * 4000 +                    # 4k za m²
    domy['pokoje'] * 15000 +                         # 15k za pokój
    (50 - domy['wiek']) * 1000 +                     # -1k za rok wieku
    (20 - domy['odleglosc_centrum']) * 2000 +        # -2k za km od centrum
    domy['powierzchnia_dzialki'] * 50 +              # 50 za m² działki
    np.random.normal(0, 30000)                       # szum
)
domy['cena'] = np.clip(domy['cena'], 100000, 2000000)  # realistyczny zakres

print("=== PORÓWNANIE MODELI Z I BEZ STANDARDYZACJI ===")

# Przygotowanie danych
X = domy.drop('cena', axis=1)
y = domy['cena']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Dane treningowe: {X_train.shape}")
print(f"Zakresy cech w danych treningowych:")
for col in X_train.columns:
    min_val = X_train[col].min()
    max_val = X_train[col].max()
    print(f"  {col:20}: {min_val:8.1f} - {max_val:8.1f}")

# MODEL 1: Bez standardyzacji
model_raw = LinearRegression()
model_raw.fit(X_train, y_train)
y_pred_raw = model_raw.predict(X_test)

mse_raw = mean_squared_error(y_test, y_pred_raw)
r2_raw = r2_score(y_test, y_pred_raw)

print(f"\n=== MODEL BEZ STANDARDYZACJI ===")
print(f"R² Score: {r2_raw:.4f}")
print(f"RMSE: {np.sqrt(mse_raw):,.0f} PLN")
print(f"Współczynniki modelu:")
for feature, coef in zip(X_train.columns, model_raw.coef_):
    print(f"  {feature:20}: {coef:10.2f}")

# MODEL 2: Ze standardyzacją
scaler_houses = StandardScaler()
X_train_scaled = scaler_houses.fit_transform(X_train)
X_test_scaled = scaler_houses.transform(X_test)  # WAŻNE: tylko transform!

model_scaled = LinearRegression()
model_scaled.fit(X_train_scaled, y_train)
y_pred_scaled = model_scaled.predict(X_test_scaled)

mse_scaled = mean_squared_error(y_test, y_pred_scaled)
r2_scaled = r2_score(y_test, y_pred_scaled)

print(f"\n=== MODEL ZE STANDARDYZACJĄ ===")
print(f"R² Score: {r2_scaled:.4f}")
print(f"RMSE: {np.sqrt(mse_scaled):,.0f} PLN")
print(f"Współczynniki modelu (standaryzowane):")
for feature, coef in zip(X_train.columns, model_scaled.coef_):
    print(f"  {feature:20}: {coef:10.2f}")

# Interpretacja współczynników po standardyzacji
print(f"\nINTERPRETACJA (zmiana ceny przy zmianie o 1 odchylenie std):")
for feature, coef, std_dev in zip(X_train.columns, model_scaled.coef_, scaler_houses.scale_):
    print(f"  {feature:20}: {coef:+8.0f} PLN/std ({std_dev:.1f} jednostek)")
```

### 🎯 Klasyfikacja z różnymi algorytmami

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Wygeneruj dane klasyfikacyjne
np.random.seed(456)
n_samples = 1000

# Cechy o bardzo różnych skalach
X_class = pd.DataFrame({
    'feature_small': np.random.normal(0, 1, n_samples),      # skala 0-1
    'feature_medium': np.random.normal(50, 15, n_samples),   # skala 20-80
    'feature_large': np.random.normal(5000, 1500, n_samples) # skala 2000-8000
})

# Target zależy od kombinacji cech
y_class = (
    (X_class['feature_small'] > 0).astype(int) +
    (X_class['feature_medium'] > 50).astype(int) + 
    (X_class['feature_large'] > 5000).astype(int)
)
# Klasy: 0, 1, 2, 3 (liczba warunków spełnionych)

print("=== WPŁYW STANDARDYZACJI NA RÓŻNE ALGORYTMY ===")
print(f"Rozkład klas: {np.bincount(y_class)}")

# Podział danych
X_train_cl, X_test_cl, y_train_cl, y_test_cl = train_test_split(
    X_class, y_class, test_size=0.2, random_state=42, stratify=y_class
)

# Standardyzacja
scaler_cl = StandardScaler()
X_train_cl_scaled = scaler_cl.fit_transform(X_train_cl)
X_test_cl_scaled = scaler_cl.transform(X_test_cl)

# Różne algorytmy
algorithms = {
    'KNN': KNeighborsClassifier(n_neighbors=5),
    'SVM': SVC(kernel='rbf', random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

results = []

for name, algorithm in algorithms.items():
    # Bez standardyzacji
    alg_raw = algorithm
    alg_raw.fit(X_train_cl, y_train_cl)
    acc_raw = accuracy_score(y_test_cl, alg_raw.predict(X_test_cl))
    
    # Ze standardyzacją
    alg_scaled = algorithm.__class__(**algorithm.get_params())  # kopia
    alg_scaled.fit(X_train_cl_scaled, y_train_cl)
    acc_scaled = accuracy_score(y_test_cl, alg_scaled.predict(X_test_cl_scaled))
    
    # Poprawa
    improvement = acc_scaled - acc_raw
    
    print(f"\n{name}:")
    print(f"  Bez standardyzacji: {acc_raw:.4f}")
    print(f"  Ze standardyzacją:  {acc_scaled:.4f}")
    print(f"  Poprawa:           {improvement:+.4f}")
    
    results.append({
        'Algorytm': name,
        'Bez_std': acc_raw,
        'Ze_std': acc_scaled,
        'Poprawa': improvement
    })

results_df = pd.DataFrame(results)
print(f"\n=== PODSUMOWANIE ===")
print(results_df.round(4))

# Który algorytm najbardziej skorzystał?
best_improvement = results_df.loc[results_df['Poprawa'].idxmax()]
print(f"\nNajbardziej skorzystał: {best_improvement['Algorytm']} (+{best_improvement['Poprawa']:.4f})")
```

## ⚠️ Ważne uwagi

### 1️⃣ Fit vs Transform

```python
# BŁĘDNY sposób - leakage danych
# scaler = StandardScaler()
# X_all_scaled = scaler.fit_transform(X_all)  # ŹLE! Używa info z test set

# PRAWIDŁOWY sposób
X_train_ex, X_test_ex = train_test_split(X_class, test_size=0.2, random_state=42)

scaler_ex = StandardScaler()
# 1. Fit tylko na train
X_train_scaled_ex = scaler_ex.fit_transform(X_train_ex)
# 2. Transform test (bez fit!)
X_test_scaled_ex = scaler_ex.transform(X_test_ex)

print("=== PRAWIDŁOWE UŻYCIE SCALER ===")
print(f"Train - średnia: {X_train_scaled_ex.mean(axis=0).round(3)}")
print(f"Test - średnia: {X_test_scaled_ex.mean(axis=0).round(3)}")
print("Test może mieć średnią != 0 - to jest OK!")
```

### 2️⃣ Kiedy używać, a kiedy nie

```python
print("=== KIEDY UŻYWAĆ STANDARDSCALER? ===")
print("✅ UŻYWAJ dla:")
print("   - KNN, SVM, Neural Networks")
print("   - Logistic Regression, Linear Regression") 
print("   - PCA, Clustering (K-means)")
print("   - Gdy cechy mają bardzo różne skale")

print("\n❌ NIE UŻYWAJ dla:")
print("   - Tree-based algorithms (Random Forest, XGBoost)")
print("   - Naive Bayes")
print("   - Gdy wszystkie cechy mają podobne skale")

# Demonstracja - Random Forest nie potrzebuje standardyzacji
rf_raw = RandomForestClassifier(n_estimators=50, random_state=42)
rf_raw.fit(X_train_cl, y_train_cl)
acc_rf_raw = accuracy_score(y_test_cl, rf_raw.predict(X_test_cl))

rf_scaled = RandomForestClassifier(n_estimators=50, random_state=42)
rf_scaled.fit(X_train_cl_scaled, y_train_cl)
acc_rf_scaled = accuracy_score(y_test_cl, rf_scaled.predict(X_test_cl_scaled))

print(f"\nRandom Forest - demonstracja:")
print(f"Bez standardyzacji: {acc_rf_raw:.4f}")
print(f"Ze standardyzacją:  {acc_rf_scaled:.4f}")
print(f"Różnica:           {abs(acc_rf_scaled - acc_rf_raw):.4f} (minimalna)")
```

## 📝 Podsumowanie

`StandardScaler` to kluczowe narzędzie preprocessing:

- ⚖️ Przekształca dane do średniej=0, std=1
- 🎯 Używaj TYLKO `fit()` na train, potem `transform()` na test
- 💪 Kluczowe dla KNN, SVM, Neural Networks, PCA
- 🚫 Niepotrzebne dla Random Forest, XGBoost
- 📊 Pozwala porównywać współczynniki modeli
- ⚠️ Uważaj na data leakage - nie fit na całym datasecie!
- 🔄 `fit_transform()` dla train, `transform()` dla test/production

To jak dostrojenie instrumentów przed koncertem! 🎼✨