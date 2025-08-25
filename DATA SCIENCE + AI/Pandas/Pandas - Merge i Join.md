## 🐼 Pandas - Merge i Join

_Łączenie danych z różnych źródeł_

---

### 📝 Wprowadzenie do łączenia danych

**Łączenie (joining)** to proces kombinowania danych z dwóch lub więcej DataFrame'ów na podstawie wspólnych kluczy. Pandas oferuje kilka metod:

- `pd.merge()` - główna funkcja do łączenia
- `DataFrame.join()` - łączenie po indeksie  
- `pd.concat()` - konkatenacja wzdłuż osi

```python
import pandas as pd
import numpy as np

# Przykładowe dane
customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Anna', 'Jan', 'Katarzyna', 'Piotr', 'Magdalena'],
    'city': ['Warszawa', 'Kraków', 'Gdańsk', 'Wrocław', 'Poznań']
})

orders = pd.DataFrame({
    'order_id': [101, 102, 103, 104, 105, 106],
    'customer_id': [1, 2, 1, 3, 2, 6],
    'product': ['Laptop', 'Mysz', 'Klawiatura', 'Monitor', 'Słuchawki', 'Tablet'],
    'amount': [2500, 50, 150, 800, 200, 1200]
})
```

---

### 🔄 Typy merge'ów

```python
# Inner join - tylko pasujące rekordy
inner_merge = pd.merge(customers, orders, on='customer_id', how='inner')
print("Inner join:")
print(inner_merge)
print(f"Liczba wierszy: {len(inner_merge)}")

# Left join - wszystkie z lewego DataFrame
left_merge = pd.merge(customers, orders, on='customer_id', how='left')
print("\nLeft join:")
print(left_merge)
print(f"Liczba wierszy: {len(left_merge)}")

# Right join - wszystkie z prawego DataFrame  
right_merge = pd.merge(customers, orders, on='customer_id', how='right')
print("\nRight join:")
print(right_merge)
print(f"Liczba wierszy: {len(right_merge)}")

# Outer join - wszystkie rekordy z obu DataFrame'ów
outer_merge = pd.merge(customers, orders, on='customer_id', how='outer')
print("\nOuter join:")
print(outer_merge)
print(f"Liczba wierszy: {len(outer_merge)}")
```

---

### 🔑 Łączenie po różnych kluczach

```python
# Łączenie po różnych nazwach kolumn
customers_alt = customers.copy()
customers_alt.rename(columns={'customer_id': 'cust_id'}, inplace=True)

merged_diff_names = pd.merge(
    customers_alt, 
    orders, 
    left_on='cust_id', 
    right_on='customer_id',
    how='inner'
)
print("Łączenie po różnych nazwach kolumn:")
print(merged_diff_names.head())

# Łączenie po wielu kolumnach
products = pd.DataFrame({
    'product': ['Laptop', 'Mysz', 'Klawiatura', 'Monitor'],
    'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics'],
    'price': [2500, 50, 150, 800]
})

orders_with_cat = pd.DataFrame({
    'order_id': [101, 102, 103, 104],
    'product': ['Laptop', 'Mysz', 'Klawiatura', 'Monitor'],
    'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics'],
    'quantity': [1, 2, 1, 1]
})

multi_key_merge = pd.merge(
    products, 
    orders_with_cat, 
    on=['product', 'category'],
    how='inner'
)
print("\nŁączenie po wielu kolumnach:")
print(multi_key_merge)
```

---

### 📋 Suffixes i konflikt nazw

```python
# Dane z konfliktującymi nazwami kolumn
customers_detailed = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'name': ['Anna', 'Jan', 'Katarzyna'],
    'phone': ['123456789', '987654321', '555666777']
})

orders_detailed = pd.DataFrame({
    'order_id': [101, 102, 103],
    'customer_id': [1, 2, 1],
    'name': ['Laptop Dell', 'Mysz Logitech', 'Klawiatura'],  # konflikt!
    'price': [2500, 50, 150]
})

# Użycie suffixes do rozróżnienia
merged_with_suffix = pd.merge(
    customers_detailed,
    orders_detailed,
    on='customer_id',
    suffixes=('_customer', '_product')
)
print("Merge z suffixes:")
print(merged_with_suffix)

# Alternatywnie - rename przed merge
orders_renamed = orders_detailed.rename(columns={'name': 'product_name'})
clean_merge = pd.merge(customers_detailed, orders_renamed, on='customer_id')
print("\nMerge po rename:")
print(clean_merge)
```

---

### 🔍 Join po indeksie

```python
# Ustawienie indeksów
customers_indexed = customers.set_index('customer_id')
orders_indexed = orders.set_index('customer_id')

# Join po indeksie
index_join = customers_indexed.join(orders_indexed, how='left')
print("Join po indeksie:")
print(index_join)

# Multiple DataFrames join
additional_data = pd.DataFrame({
    'customer_id': [1, 2, 3, 4],
    'registration_date': pd.date_range('2022-01-01', periods=4),
    'status': ['Active', 'Active', 'Inactive', 'Active']
}).set_index('customer_id')

multiple_join = customers_indexed.join([orders_indexed, additional_data], how='outer')
print("\nJoin wielu DataFrame'ów:")
print(multiple_join.head())
```

---

### 🔗 Concat - konkatenacja

```python
# Konkatenacja wierszowa (vertical)
df1 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

df2 = pd.DataFrame({
    'A': [7, 8, 9],  
    'B': [10, 11, 12]
})

vertical_concat = pd.concat([df1, df2])
print("Konkatenacja wierszowa:")
print(vertical_concat)

# Reset indeksu
vertical_concat_reset = pd.concat([df1, df2], ignore_index=True)
print("\nZ resetem indeksu:")
print(vertical_concat_reset)

# Konkatenacja kolumnowa (horizontal)
df3 = pd.DataFrame({
    'C': [13, 14, 15],
    'D': [16, 17, 18]
})

horizontal_concat = pd.concat([df1, df3], axis=1)
print("\nKonkatenacja kolumnowa:")
print(horizontal_concat)

# Concat z kluczami (hierarchical index)
keyed_concat = pd.concat([df1, df2], keys=['Group1', 'Group2'])
print("\nConcat z kluczami:")
print(keyed_concat)
```

---

### ⚠️ Walidacja merge'ów

```python
# Sprawdzanie typów join'ów
try:
    # one_to_one - oczekujemy relacji 1:1
    validated_merge = pd.merge(
        customers, 
        orders.drop_duplicates('customer_id'), 
        on='customer_id', 
        validate='one_to_one'
    )
except pd.errors.MergeError as e:
    print(f"Błąd walidacji: {e}")

# one_to_many - klient może mieć wiele zamówień
valid_one_to_many = pd.merge(
    customers, 
    orders, 
    on='customer_id', 
    validate='one_to_many'
)
print("Poprawny one_to_many merge:")
print(valid_one_to_many.head())

# Sprawdzanie duplikatów przed merge
print(f"Duplikaty w customers: {customers['customer_id'].duplicated().sum()}")
print(f"Duplikaty w orders: {orders['customer_id'].duplicated().sum()}")

# Indicator - sprawdzanie pochodzenia wierszy
merge_with_indicator = pd.merge(
    customers, 
    orders, 
    on='customer_id', 
    how='outer',
    indicator=True
)
print("\nMerge z indicator:")
print(merge_with_indicator['_merge'].value_counts())
print(merge_with_indicator[merge_with_indicator['_merge'] == 'right_only'])
```

---

### 🚀 Zaawansowane techniki

```python
# Fuzzy matching - przybliżone dopasowanie
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Przykład z podobnymi nazwami
companies1 = pd.DataFrame({
    'name': ['Apple Inc.', 'Google LLC', 'Microsoft Corp'],
    'revenue': [365, 280, 168]
})

companies2 = pd.DataFrame({
    'name': ['Apple Inc', 'Google', 'Microsoft Corporation'],
    'employees': [154000, 135000, 181000]
})

# Manual fuzzy matching (dla małych datasets)
def find_best_match(name, candidates, threshold=0.8):
    best_match = None
    best_score = 0
    for candidate in candidates:
        score = similarity(name, candidate)
        if score > best_score and score >= threshold:
            best_score = score
            best_match = candidate
    return best_match

companies1['best_match'] = companies1['name'].apply(
    lambda x: find_best_match(x, companies2['name'].tolist())
)
print("Fuzzy matching results:")
print(companies1)

# Conditional merge - łączenie z warunkami
large_orders = orders[orders['amount'] > 100]
customers_with_large_orders = pd.merge(customers, large_orders, on='customer_id')
print("\nKlienci z dużymi zamówieniami:")
print(customers_with_large_orders)

# Aggregate before merge
customer_stats = orders.groupby('customer_id').agg({
    'amount': ['sum', 'count', 'mean'],
    'order_id': 'count'
}).round(2)

# Flatten column names
customer_stats.columns = ['total_amount', 'order_count', 'avg_amount', 'total_orders']
customer_stats = customer_stats.reset_index()

enriched_customers = pd.merge(customers, customer_stats, on='customer_id', how='left')
print("\nKlienci ze statystykami:")
print(enriched_customers)
```

---

### 🔧 Obsługa brakujących danych po merge

```python
# Dane po outer merge z NaN
outer_result = pd.merge(customers, orders, on='customer_id', how='outer')

# Wypełnianie NaN wartościami domyślnymi
filled_result = outer_result.copy()
filled_result['name'] = filled_result['name'].fillna('Unknown Customer')
filled_result['amount'] = filled_result['amount'].fillna(0)
filled_result['product'] = filled_result['product'].fillna('No Order')

print("Dane po wypełnieniu NaN:")
print(filled_result)

# Identyfikacja niekompletnych merges
incomplete_customers = outer_result[outer_result['order_id'].isna()]
incomplete_orders = outer_result[outer_result['name'].isna()]

print(f"\nKlienci bez zamówień: {len(incomplete_customers)}")
print(f"Zamówienia bez klientów: {len(incomplete_orders)}")
```

---

### 💻 Praktyczne zastosowania

```python
# 1. Analiza cohort - łączenie danych czasowych
first_orders = orders.groupby('customer_id')['order_id'].min().reset_index()
first_orders.columns = ['customer_id', 'first_order_id']

cohort_analysis = pd.merge(orders, first_orders, on='customer_id')
print("Dane do analizy cohort:")
print(cohort_analysis.head())

# 2. Ranking klientów
customer_rankings = orders.groupby('customer_id').agg({
    'amount': 'sum'
}).reset_index()
customer_rankings['rank'] = customer_rankings['amount'].rank(ascending=False)

customers_ranked = pd.merge(customers, customer_rankings, on='customer_id', how='left')
print("\nRanking klientów:")
print(customers_ranked.sort_values('rank'))

# 3. Product affinity - co kupują razem
order_products = orders[['customer_id', 'product']].drop_duplicates()

# Self join do znalezienia par produktów
product_pairs = pd.merge(
    order_products, 
    order_products, 
    on='customer_id', 
    suffixes=('_1', '_2')
)
product_pairs = product_pairs[product_pairs['product_1'] != product_pairs['product_2']]

affinity_counts = product_pairs.groupby(['product_1', 'product_2']).size().reset_index()
affinity_counts.columns = ['product_1', 'product_2', 'frequency']
print("\nAfinowość produktów:")
print(affinity_counts.sort_values('frequency', ascending=False))

# 4. Time-based join - łączenie z tolerancją czasową
# (wymaga pandas >= 1.1.0)
time_series1 = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=5, freq='H'),
    'value1': [1, 2, 3, 4, 5]
})

time_series2 = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01 00:30', periods=4, freq='H'),
    'value2': [10, 20, 30, 40]
})

# Nearest time join (simplified example)
def nearest_time_join(df1, df2, tolerance='30min'):
    result_list = []
    for _, row1 in df1.iterrows():
        time_diff = abs(df2['timestamp'] - row1['timestamp'])
        if time_diff.min() <= pd.Timedelta(tolerance):
            closest_idx = time_diff.idxmin()
            merged_row = pd.concat([row1, df2.loc[closest_idx]])
            result_list.append(merged_row)
    return pd.DataFrame(result_list)

time_merged = nearest_time_join(time_series1, time_series2)
print("\nTime-based join:")
print(time_merged)
```

---

### ⚡ Performance tips

```python
# 1. Sortowanie przed merge dla lepszej wydajności
customers_sorted = customers.sort_values('customer_id')
orders_sorted = orders.sort_values('customer_id')

# 2. Użyj categoricals dla join keys
customers['customer_id'] = customers['customer_id'].astype('category')
orders['customer_id'] = orders['customer_id'].astype('category')

# 3. Index przed multiple joins
customers_idx = customers.set_index('customer_id')

# 4. Chunk processing dla dużych datasets
def chunk_merge(left_df, right_df, chunk_size=10000):
    chunks = []
    for i in range(0, len(left_df), chunk_size):
        chunk = left_df.iloc[i:i+chunk_size]
        merged_chunk = pd.merge(chunk, right_df, on='customer_id')
        chunks.append(merged_chunk)
    return pd.concat(chunks, ignore_index=True)
```

---

### 🎯 Następny krok

Poznasz **Pivot Tables w Pandas**:

- Tworzenie pivot tables
- Multi-level pivots
- Crosstab analysis
- Reshaping data
- Advanced aggregations