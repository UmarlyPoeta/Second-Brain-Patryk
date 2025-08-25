## 🐼 Pandas - GroupBy Operations

_Zaawansowane techniki grupowania i agregacji danych_

---

### 📝 Wprowadzenie do GroupBy

**GroupBy** implementuje strategię "Split-Apply-Combine":
1. **Split** - podział danych na grupy
2. **Apply** - zastosowanie funkcji do każdej grupy
3. **Combine** - połączenie wyników w jeden obiekt

```python
import pandas as pd
import numpy as np

# Przykładowe dane sprzedażowe
sales_df = pd.DataFrame({
    'Sprzedawca': ['Anna', 'Jan', 'Anna', 'Piotr', 'Jan', 'Anna', 'Piotr'],
    'Region': ['Północ', 'Południe', 'Północ', 'Wschód', 'Południe', 'Północ', 'Wschód'],
    'Produkt': ['A', 'B', 'A', 'C', 'B', 'C', 'A'],
    'Sprzedaż': [100, 150, 120, 80, 200, 90, 110],
    'Zysk': [20, 45, 25, 15, 60, 18, 22],
    'Data': pd.date_range('2023-01-01', periods=7)
})
```

---

### 🎯 Podstawowe grupowanie

```python
# Grupowanie po jednej kolumnie
grouped_by_seller = sales_df.groupby('Sprzedawca')

# Podstawowe agregacje
print("Suma sprzedaży wg sprzedawcy:")
print(grouped_by_seller['Sprzedaż'].sum())

print("\nŚredni zysk wg sprzedawcy:")
print(grouped_by_seller['Zysk'].mean())

# Wiele statystyk jednocześnie
stats = grouped_by_seller['Sprzedaż'].agg(['sum', 'mean', 'count', 'std'])
print("\nStatystyki sprzedaży:")
print(stats)

# Różne funkcje dla różnych kolumn
multi_agg = grouped_by_seller.agg({
    'Sprzedaż': ['sum', 'mean'],
    'Zysk': ['sum', 'max'],
    'Produkt': 'count'
})
print("\nWiele agregacji:")
print(multi_agg)
```

---

### 🔄 Grupowanie wielopoziomowe

```python
# Grupowanie po wielu kolumnach
multi_grouped = sales_df.groupby(['Region', 'Sprzedawca'])

# Hierarchiczne wyniki
hierarchical_sum = multi_grouped['Sprzedaż'].sum()
print("Suma sprzedaży wg regionu i sprzedawcy:")
print(hierarchical_sum)

# Unstacking dla lepszej czytelności
unstacked = hierarchical_sum.unstack(fill_value=0)
print("\nTablica przestawna:")
print(unstacked)

# Grupowanie po poziomach
print("\nSuma wg regionów (poziom 0):")
print(hierarchical_sum.groupby(level=0).sum())

print("\nŚrednia wg sprzedawców (poziom 1):")
print(hierarchical_sum.groupby(level=1).mean())
```

---

### ⚙️ Własne funkcje agregujące

```python
# Proste funkcje własne
def range_calc(series):
    return series.max() - series.min()

def profit_margin(group):
    return (group['Zysk'].sum() / group['Sprzedaż'].sum()) * 100

# Zastosowanie własnych funkcji
sales_range = sales_df.groupby('Region')['Sprzedaż'].agg(range_calc)
print("Rozstęp sprzedaży wg regionów:")
print(sales_range)

# Funkcja operująca na całej grupie
margins = sales_df.groupby('Region').apply(profit_margin)
print("\nMarża zysku wg regionów (%):")
print(margins)

# Kombinacja własnych i wbudowanych funkcji
complex_agg = sales_df.groupby('Sprzedawca').agg({
    'Sprzedaż': ['sum', 'mean', range_calc],
    'Zysk': ['sum', lambda x: x.max() - x.min()]
})
print("\nZłożona agregacja:")
print(complex_agg)
```

---

### 🔍 Transform i Apply

```python
# Transform - zachowuje oryginalny kształt danych
# Dodanie średniej grupy do każdego wiersza
sales_df['Avg_by_seller'] = sales_df.groupby('Sprzedawca')['Sprzedaż'].transform('mean')

# Normalizacja względem grupy
sales_df['Sales_normalized'] = sales_df.groupby('Region')['Sprzedaż'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Ranking w grupie
sales_df['Rank_in_region'] = sales_df.groupby('Region')['Sprzedaż'].rank(ascending=False)

print("DataFrame z dodatkowymi kolumnami:")
print(sales_df[['Sprzedawca', 'Region', 'Sprzedaż', 'Avg_by_seller', 'Rank_in_region']])

# Apply - może zwrócić różne kształty
def group_summary(group):
    return pd.Series({
        'total_sales': group['Sprzedaż'].sum(),
        'total_profit': group['Zysk'].sum(),
        'transactions': len(group),
        'avg_per_transaction': group['Sprzedaż'].mean(),
        'best_product': group.loc[group['Sprzedaż'].idxmax(), 'Produkt']
    })

region_summary = sales_df.groupby('Region').apply(group_summary)
print("\nPodsumowanie regionów:")
print(region_summary)
```

---

### 🕐 Grupowanie czasowe

```python
# Dane z większym zakresem czasowym
time_data = pd.DataFrame({
    'Data': pd.date_range('2023-01-01', '2023-12-31', freq='D'),
    'Sprzedaż': np.random.randint(50, 200, 365),
    'Kategoria': np.random.choice(['A', 'B', 'C'], 365)
})

# Ustawienie indeksu czasowego
time_data = time_data.set_index('Data')

# Grupowanie po okresach czasowych
monthly = time_data['Sprzedaż'].resample('M').sum()
print("Sprzedaż miesięczna:")
print(monthly.head())

# Grupowanie po dniu tygodnia
by_weekday = time_data.groupby(time_data.index.dayofweek)['Sprzedaż'].mean()
weekday_names = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
by_weekday.index = weekday_names
print("\nŚrednia sprzedaż wg dnia tygodnia:")
print(by_weekday)

# Kombinacja grupowania czasowego i kategorycznego
monthly_by_category = time_data.groupby([pd.Grouper(freq='M'), 'Kategoria'])['Sprzedaż'].sum()
print("\nSprzedaż miesięczna wg kategorii:")
print(monthly_by_category.head(10))
```

---

### 🎲 Próbkowanie w grupach

```python
# Losowe próbkowanie z każdej grupy
# Po 2 losowe rekordy z każdego regionu
sampled = sales_df.groupby('Region').sample(n=2, random_state=42)
print("Losowe próbki z każdego regionu:")
print(sampled)

# Procent z każdej grupy
sampled_pct = sales_df.groupby('Sprzedawca').sample(frac=0.5, random_state=42)
print("\n50% rekordów od każdego sprzedawcy:")
print(sampled_pct)

# Pierwsze/ostatnie n rekordów z grupy
first_sales = sales_df.groupby('Region').head(2)
print("\nPierwsze 2 sprzedaże z każdego regionu:")
print(first_sales)

last_sales = sales_df.groupby('Region').tail(1)
print("\nOstatnia sprzedaż z każdego regionu:")
print(last_sales)
```

---

### 🔄 Iterowanie przez grupy

```python
# Iteracja przez wszystkie grupy
print("Iteracja przez regiony:")
for name, group in sales_df.groupby('Region'):
    print(f"\n=== Region: {name} ===")
    print(f"Liczba transakcji: {len(group)}")
    print(f"Łączna sprzedaż: {group['Sprzedaż'].sum()}")
    print(f"Najlepszy sprzedawca: {group.loc[group['Sprzedaż'].idxmax(), 'Sprzedawca']}")

# Dostęp do konkretnej grupy
north_group = sales_df.groupby('Region').get_group('Północ')
print(f"\nGrupa 'Północ':")
print(north_group)

# Lista wszystkich grup
all_groups = dict(list(sales_df.groupby('Region')))
print(f"\nNazwy grup: {list(all_groups.keys())}")
```

---

### 📊 Window Functions w grupach

```python
# Sortowanie i window functions w grupach
sales_sorted = sales_df.sort_values(['Region', 'Data'])

# Cumulative sum w ramach grupy
sales_sorted['Cumsum_by_region'] = sales_sorted.groupby('Region')['Sprzedaż'].cumsum()

# Moving average w ramach grupy  
sales_sorted['MA3_by_region'] = sales_sorted.groupby('Region')['Sprzedaż'].rolling(
    window=3, min_periods=1
).mean().reset_index(level=0, drop=True)

# Lag/Lead w ramach grupy
sales_sorted['Prev_sale'] = sales_sorted.groupby('Region')['Sprzedaż'].shift(1)
sales_sorted['Next_sale'] = sales_sorted.groupby('Region')['Sprzedaż'].shift(-1)

print("Window functions w grupach:")
print(sales_sorted[['Region', 'Sprzedaż', 'Cumsum_by_region', 'MA3_by_region']])
```

---

### 💻 Praktyczne zastosowania

```python
# 1. Analiza ABC (Pareto) w grupach
def abc_analysis(group, value_col='Sprzedaż'):
    group = group.sort_values(value_col, ascending=False)
    group['Cumsum'] = group[value_col].cumsum()
    total = group[value_col].sum()
    group['Cumsum_pct'] = (group['Cumsum'] / total) * 100
    
    def classify(pct):
        if pct <= 80:
            return 'A'
        elif pct <= 95:
            return 'B'
        else:
            return 'C'
    
    group['ABC_Category'] = group['Cumsum_pct'].apply(classify)
    return group

abc_by_region = sales_df.groupby('Region').apply(lambda x: abc_analysis(x))
print("Analiza ABC wg regionów:")
print(abc_by_region[['Region', 'Produkt', 'Sprzedaż', 'ABC_Category']])

# 2. Top N w każdej grupie
top_sellers_by_region = sales_df.groupby('Region').apply(
    lambda x: x.nlargest(2, 'Sprzedaż')
)
print("\nTop 2 sprzedaże w każdym regionie:")
print(top_sellers_by_region[['Sprzedawca', 'Sprzedaż']])

# 3. Outliers w grupach (używając IQR)
def find_outliers(group, col='Sprzedaż'):
    Q1 = group[col].quantile(0.25)
    Q3 = group[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return group[(group[col] < lower_bound) | (group[col] > upper_bound)]

outliers = sales_df.groupby('Region').apply(find_outliers)
print(f"\nOutliers znalezione w {len(outliers)} przypadkach")

# 4. Porównanie z średnią grupy
def compare_to_group_avg(group, col='Sprzedaż'):
    group_avg = group[col].mean()
    group['Vs_group_avg'] = ((group[col] / group_avg) - 1) * 100
    return group

compared = sales_df.groupby('Sprzedawca').apply(compare_to_group_avg)
print("\nPorównanie do średniej grupy (%):")
print(compared[['Sprzedawca', 'Sprzedaż', 'Vs_group_avg']])
```

---

### ⚡ Optymalizacja wydajności

```python
# 1. Użyj categoricals dla kolumn z ograniczoną liczbą wartości
sales_df['Region'] = sales_df['Region'].astype('category')
sales_df['Sprzedawca'] = sales_df['Sprzedawca'].astype('category')

# 2. NumPy functions są szybsze
# Zamiast: .agg(lambda x: x.max() - x.min())
# Użyj: .agg(lambda x: np.ptp(x))

# 3. Unikaj apply gdy możliwe, używaj built-in functions

# 4. Pre-sortowanie dla lepszej wydajności
sales_df_sorted = sales_df.sort_values(['Region', 'Sprzedawca'])
```

---

### 🎯 Następny krok

Poznasz **Merge i Join w Pandas**:

- Różne typy join'ów
- Łączenie na podstawie kluczy
- Handling conflicts
- Performance considerations
- Validate options