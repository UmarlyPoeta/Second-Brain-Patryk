## 🐼 Pandas - Advanced Indexing i MultiIndex

_Zaawansowane techniki indeksowania i praca z hierarchicznymi indeksami w Pandas_

---

### 📝 Wprowadzenie do zaawansowanego indeksowania

**Advanced indexing w Pandas** obejmuje:

1. **MultiIndex (hierarchiczne indeksy)** - wielopoziomowe indeksy
2. **Advanced selection** - `.loc`, `.iloc`, `.at`, `.iat`
3. **Boolean indexing** - filtrowanie z warunkami
4. **Query method** - SQL-like querying
5. **Index alignment** - automatyczne dopasowanie indeksów

---

### 🏗️ MultiIndex - Hierarchiczne indeksy

#### Tworzenie MultiIndex

```python
import pandas as pd
import numpy as np

# Metoda 1: Z list tupli
tuples = [
    ('A', 'X', 1), ('A', 'X', 2), ('A', 'Y', 1), ('A', 'Y', 2),
    ('B', 'X', 1), ('B', 'X', 2), ('B', 'Y', 1), ('B', 'Y', 2)
]
index = pd.MultiIndex.from_tuples(tuples, names=['Level1', 'Level2', 'Level3'])

data = np.random.randn(8, 3)
df_multi = pd.DataFrame(data, index=index, columns=['Value1', 'Value2', 'Value3'])

print("MultiIndex DataFrame:")
print(df_multi)
print(f"\nIndex levels: {df_multi.index.nlevels}")
print(f"Index names: {df_multi.index.names}")

# Metoda 2: Z produktu kartezjańskiego
arrays = [['A', 'A', 'B', 'B'], ['X', 'Y', 'X', 'Y']]
index2 = pd.MultiIndex.from_arrays(arrays, names=['Group', 'Subgroup'])

# Metoda 3: Z product
from itertools import product
index3 = pd.MultiIndex.from_product(
    [['Company1', 'Company2'], ['Q1', 'Q2', 'Q3', 'Q4'], [2022, 2023]], 
    names=['Company', 'Quarter', 'Year']
)

print(f"\nProduct index length: {len(index3)}")
print(f"Product index names: {index3.names}")
```

#### Navigating MultiIndex

```python
# Tworzenie przykładowego datasetu finansowego
companies = ['Apple', 'Google', 'Microsoft']
quarters = ['Q1', 'Q2', 'Q3', 'Q4']  
years = [2022, 2023]
metrics = ['Revenue', 'Profit', 'Expenses']

# MultiIndex dla wierszy i kolumn
row_index = pd.MultiIndex.from_product([companies, years, quarters], 
                                      names=['Company', 'Year', 'Quarter'])
col_index = pd.MultiIndex.from_product([['Financial', 'Operational'], metrics],
                                      names=['Category', 'Metric'])

# Dane przykładowe
np.random.seed(42)
data = np.random.randint(100, 1000, size=(len(row_index), len(col_index)))
df_finance = pd.DataFrame(data, index=row_index, columns=col_index)

print("Financial MultiIndex DataFrame:")
print(df_finance.head(8))

# Podstawowe operacje na MultiIndex
print(f"\nDataFrame shape: {df_finance.shape}")
print(f"Index levels: {df_finance.index.nlevels}")
print(f"Column levels: {df_finance.columns.nlevels}")

# Dostęp do poziomów indeksu
print(f"\nCompanies in dataset: {df_finance.index.get_level_values('Company').unique()}")
print(f"Years in dataset: {df_finance.index.get_level_values('Year').unique()}")
```

#### Advanced MultiIndex selection

```python
# Różne sposoby selekcji w MultiIndex
print("MultiIndex Selection Examples:")
print("=" * 50)

# 1. Pojedynczy poziom
apple_data = df_finance.loc['Apple']
print(f"Apple data shape: {apple_data.shape}")

# 2. Tuple indexing - konkretny wiersz
specific_row = df_finance.loc[('Apple', 2023, 'Q1')]
print(f"Apple Q1 2023 data:\n{specific_row}")

# 3. Slice notation
apple_2023 = df_finance.loc[('Apple', 2023), :]
print(f"\nApple 2023 all quarters shape: {apple_2023.shape}")

# 4. Cross-section (xs) - bardzo użyteczne
q1_all_companies = df_finance.xs('Q1', level='Quarter')
print(f"\nQ1 data for all companies shape: {q1_all_companies.shape}")

# 5. IndexSlice dla złożonych selekcji
idx = pd.IndexSlice
apple_google_2023 = df_finance.loc[idx[['Apple', 'Google'], 2023, :], :]
print(f"Apple & Google 2023 shape: {apple_google_2023.shape}")

# 6. Boolean indexing na MultiIndex
high_revenue_mask = df_finance[('Financial', 'Revenue')] > 500
high_revenue_companies = df_finance[high_revenue_mask]
print(f"High revenue entries: {len(high_revenue_companies)}")

# 7. Query na MultiIndex
query_result = df_finance.query("Company in ['Apple', 'Microsoft'] and Year == 2023")
print(f"Query result shape: {query_result.shape}")
```

#### MultiIndex operations i transformations

```python
def demonstrate_multiindex_operations():
    """Demonstracja operacji na MultiIndex"""
    
    # Tworzenie bardziej realnych danych
    np.random.seed(42)
    dates = pd.date_range('2022-01-01', '2023-12-31', freq='M')
    products = ['ProductA', 'ProductB', 'ProductC']
    regions = ['North', 'South', 'East', 'West']
    
    # Hierarchiczny index
    index = pd.MultiIndex.from_product(
        [products, regions, dates], 
        names=['Product', 'Region', 'Date']
    )
    
    # Dane sprzedażowe
    sales_data = {
        'Sales': np.random.normal(1000, 200, len(index)),
        'Units': np.random.poisson(50, len(index)),
        'Price': np.random.uniform(10, 100, len(index))
    }
    
    df_sales = pd.DataFrame(sales_data, index=index)
    
    print("Sales DataFrame sample:")
    print(df_sales.head(10))
    
    # 1. Grouping po poziomach indeksu
    print(f"\nGroupBy operations on MultiIndex:")
    
    # Agregacja po produktach
    product_totals = df_sales.groupby(level='Product').agg({
        'Sales': ['sum', 'mean'],
        'Units': 'sum',
        'Price': 'mean'
    })
    print(f"Product totals shape: {product_totals.shape}")
    
    # Agregacja po produktach i regionach
    product_region_avg = df_sales.groupby(level=['Product', 'Region']).mean()
    print(f"Product-Region averages shape: {product_region_avg.shape}")
    
    # 2. Unstacking - pivot MultiIndex
    print(f"\nUnstacking operations:")
    
    # Unstack jednego poziomu
    unstacked_region = df_sales['Sales'].unstack('Region')
    print(f"Unstacked by region shape: {unstacked_region.shape}")
    
    # Unstack wielu poziomów
    unstacked_prod_reg = df_sales['Sales'].unstack(['Product', 'Region'])
    print(f"Unstacked by product & region shape: {unstacked_prod_reg.shape}")
    
    # 3. Stacking - odwrotność unstacking
    restacked = unstacked_region.stack('Region')
    print(f"Restacked shape: {restacked.shape}")
    print(f"Original shape: {df_sales['Sales'].shape}")
    
    # 4. Swapping i reordering poziomów
    swapped = df_sales.swaplevel('Product', 'Region')
    print(f"After swapping levels: {swapped.index.names}")
    
    # Reorder levels
    reordered = df_sales.reorder_levels(['Region', 'Product', 'Date'])
    print(f"After reordering: {reordered.index.names}")
    
    # 5. Droplevel - usuwanie poziomu
    single_level = df_sales.droplevel(['Product', 'Region'])
    print(f"After dropping levels: {single_level.index.names}")

demonstrate_multiindex_operations()
```

---

### 🎯 Advanced Selection Techniques

#### Mastering .loc, .iloc, .at, .iat

```python
def advanced_selection_demo():
    """Demonstracja zaawansowanych technik selekcji"""
    
    # Przygotowanie danych
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=1000, freq='H')
    
    df = pd.DataFrame({
        'timestamp': dates,
        'sensor_id': np.random.choice(['S1', 'S2', 'S3', 'S4'], 1000),
        'temperature': np.random.normal(20, 5, 1000),
        'humidity': np.random.normal(60, 10, 1000),
        'pressure': np.random.normal(1013, 50, 1000),
        'status': np.random.choice(['OK', 'WARNING', 'ERROR'], 1000, p=[0.7, 0.2, 0.1])
    })
    
    df.set_index('timestamp', inplace=True)
    
    print("Sensor data sample:")
    print(df.head())
    
    # 1. LOC - label-based selection
    print(f"\n1. LOC Examples:")
    
    # Selekcja po indeksie czasowym
    morning_data = df.loc['2023-01-01 08:00:00':'2023-01-01 12:00:00']
    print(f"Morning data shape: {morning_data.shape}")
    
    # Selekcja z warunkami
    high_temp_s1 = df.loc[(df['sensor_id'] == 'S1') & (df['temperature'] > 25)]
    print(f"High temp S1 records: {len(high_temp_s1)}")
    
    # Selekcja kolumn i wierszy
    temp_humidity_subset = df.loc[df['status'] == 'ERROR', ['temperature', 'humidity']]
    print(f"Error status temp/humidity shape: {temp_humidity_subset.shape}")
    
    # 2. ILOC - position-based selection
    print(f"\n2. ILOC Examples:")
    
    # Pierwszych 100 rekordów, pierwsze 3 kolumny
    first_records = df.iloc[:100, :3]
    print(f"First records shape: {first_records.shape}")
    
    # Co 10. rekord
    every_tenth = df.iloc[::10]
    print(f"Every 10th record shape: {every_tenth.shape}")
    
    # Ostatnie 50 rekordów, konkretne kolumny
    last_temp_pressure = df.iloc[-50:, [0, 2]]  # sensor_id, pressure
    print(f"Last 50 temp/pressure shape: {last_temp_pressure.shape}")
    
    # 3. AT i IAT - pojedyncze wartości (najszybsze)
    print(f"\n3. AT/IAT Examples:")
    
    import time
    
    # AT - label based single value access
    first_timestamp = df.index[0]
    
    start = time.time()
    temp_at = df.at[first_timestamp, 'temperature']
    at_time = time.time() - start
    
    # LOC equivalent (wolniejsze)
    start = time.time()
    temp_loc = df.loc[first_timestamp, 'temperature']
    loc_time = time.time() - start
    
    # IAT - position based single value access  
    start = time.time()
    temp_iat = df.iat[0, 1]  # First row, second column (temperature)
    iat_time = time.time() - start
    
    print(f"AT access time: {at_time:.6f}s")
    print(f"LOC access time: {loc_time:.6f}s")
    print(f"IAT access time: {iat_time:.6f}s")
    print(f"Values equal: {temp_at == temp_loc == temp_iat}")

advanced_selection_demo()
```

#### Boolean indexing advanced patterns

```python
def advanced_boolean_indexing():
    """Zaawansowane wzorce boolean indexing"""
    
    # Dane sprzedażowe e-commerce
    np.random.seed(42)
    n_records = 10000
    
    df_ecommerce = pd.DataFrame({
        'order_id': range(1, n_records + 1),
        'customer_id': np.random.randint(1, 2000, n_records),
        'product_category': np.random.choice(
            ['Electronics', 'Clothing', 'Books', 'Home', 'Sports'], n_records
        ),
        'order_value': np.random.exponential(100, n_records),
        'discount_percent': np.random.uniform(0, 30, n_records),
        'customer_age': np.random.normal(40, 15, n_records),
        'is_premium': np.random.choice([True, False], n_records, p=[0.2, 0.8]),
        'order_date': pd.date_range('2023-01-01', periods=n_records, freq='H')
    })
    
    print("E-commerce data sample:")
    print(df_ecommerce.head())
    
    # 1. Kompleksowe warunki boolean
    print(f"\n1. Complex Boolean Conditions:")
    
    # Młodzi klienci premium z dużymi zamówieniami
    young_premium_high_value = df_ecommerce[
        (df_ecommerce['customer_age'] < 30) & 
        (df_ecommerce['is_premium'] == True) & 
        (df_ecommerce['order_value'] > 200)
    ]
    print(f"Young premium high-value customers: {len(young_premium_high_value)}")
    
    # 2. ISIN - sprawdzanie przynależności
    electronics_books = df_ecommerce[
        df_ecommerce['product_category'].isin(['Electronics', 'Books'])
    ]
    print(f"Electronics & Books orders: {len(electronics_books)}")
    
    # 3. String methods w boolean indexing
    weekend_orders = df_ecommerce[
        df_ecommerce['order_date'].dt.dayname().isin(['Saturday', 'Sunday'])
    ]
    print(f"Weekend orders: {len(weekend_orders)}")
    
    # 4. Quantile-based filtering
    q75_value = df_ecommerce['order_value'].quantile(0.75)
    high_value_orders = df_ecommerce[df_ecommerce['order_value'] > q75_value]
    print(f"Top 25% value orders: {len(high_value_orders)}")
    
    # 5. Rolling conditions
    df_ecommerce = df_ecommerce.sort_values('order_date')
    df_ecommerce['rolling_avg_7d'] = (
        df_ecommerce.set_index('order_date')['order_value']
        .rolling('7D').mean().values
    )
    
    # Zamówienia powyżej 7-dniowej średniej
    above_rolling_avg = df_ecommerce[
        df_ecommerce['order_value'] > df_ecommerce['rolling_avg_7d']
    ]
    print(f"Above 7-day rolling average: {len(above_rolling_avg)}")
    
    # 6. Multiple dataframe conditions
    # Top customers (by order count)
    top_customers = (
        df_ecommerce.groupby('customer_id')
        .size()
        .nlargest(100)
        .index
    )
    
    top_customer_orders = df_ecommerce[
        df_ecommerce['customer_id'].isin(top_customers)
    ]
    print(f"Top 100 customers orders: {len(top_customer_orders)}")
    
    return df_ecommerce

df_sample = advanced_boolean_indexing()
```

---

### 🔍 Query Method - SQL-like Operations

#### Basic and advanced queries

```python
def demonstrate_query_method():
    """Demonstracja query method w Pandas"""
    
    # Używamy wcześniej utworzonych danych e-commerce
    df = df_sample.copy()
    
    print("Query Method Examples:")
    print("=" * 40)
    
    # 1. Podstawowe queries
    print("1. Basic Queries:")
    
    # Proste warunki
    premium_customers = df.query("is_premium == True")
    print(f"Premium customers: {len(premium_customers)}")
    
    # Warunki numeryczne
    high_value = df.query("order_value > 200 and discount_percent < 10")
    print(f"High value, low discount: {len(high_value)}")
    
    # String conditions
    electronics = df.query("product_category == 'Electronics'")
    print(f"Electronics orders: {len(electronics)}")
    
    # 2. Złożone warunki
    print(f"\n2. Complex Conditions:")
    
    # Multiple conditions
    complex_query = df.query("""
        (customer_age > 25 and customer_age < 50) and
        (product_category in ['Electronics', 'Home']) and
        (order_value > @df.order_value.median())
    """)
    print(f"Complex query results: {len(complex_query)}")
    
    # 3. Variables w query
    print(f"\n3. Using Variables:")
    
    min_age = 30
    max_age = 60
    categories = ['Clothing', 'Books']
    
    var_query = df.query(
        "customer_age >= @min_age and customer_age <= @max_age and "
        "product_category in @categories"
    )
    print(f"Variable query results: {len(var_query)}")
    
    # 4. Date queries
    print(f"\n4. Date Queries:")
    
    # Query na daty (requires string conversion for query)
    df['order_date_str'] = df['order_date'].dt.strftime('%Y-%m-%d')
    
    january_orders = df.query("order_date_str >= '2023-01-01' and order_date_str < '2023-02-01'")
    print(f"January orders: {len(january_orders)}")
    
    # 5. Performance comparison
    print(f"\n5. Performance Comparison:")
    
    import time
    
    # Boolean indexing
    start = time.time()
    bool_result = df[(df['order_value'] > 150) & (df['customer_age'] < 40)]
    bool_time = time.time() - start
    
    # Query method
    start = time.time()
    query_result = df.query("order_value > 150 and customer_age < 40")
    query_time = time.time() - start
    
    print(f"Boolean indexing: {bool_time:.6f}s")
    print(f"Query method: {query_time:.6f}s")
    print(f"Results equal: {len(bool_result) == len(query_result)}")

demonstrate_query_method()
```

#### Query with mathematical expressions

```python
def advanced_query_patterns():
    """Zaawansowane wzorce query"""
    
    df = df_sample.copy()
    
    # 1. Mathematical expressions w query
    print("1. Mathematical Expressions in Query:")
    
    # Calculated fields w query
    margin_query = df.query("order_value * (1 - discount_percent/100) > 100")
    print(f"Orders with net value > 100: {len(margin_query)}")
    
    # Trigonometric i inne funkcje
    df['sin_age'] = np.sin(df['customer_age'] / 10)  # Normalize for sin
    trig_query = df.query("sin_age > 0.5")
    print(f"Trigonometric condition: {len(trig_query)}")
    
    # 2. String operations w query
    print(f"\n2. String Operations:")
    
    # String length
    df['category_length'] = df['product_category'].str.len()
    long_category_names = df.query("category_length > 5")
    print(f"Long category names: {len(long_category_names)}")
    
    # 3. Quantile-based queries
    print(f"\n3. Quantile-based Queries:")
    
    # Dynamic quantile calculation
    q25 = df['order_value'].quantile(0.25)
    q75 = df['order_value'].quantile(0.75)
    
    iqr_query = df.query("order_value >= @q25 and order_value <= @q75")
    print(f"IQR range orders: {len(iqr_query)}")
    
    # 4. Multi-level boolean logic
    print(f"\n4. Multi-level Boolean Logic:")
    
    complex_logic = df.query("""
        (
            (product_category == 'Electronics' and order_value > 300) or
            (product_category == 'Clothing' and discount_percent > 20) or
            (is_premium == True and customer_age > 50)
        ) and
        order_value > 50
    """)
    print(f"Complex boolean logic: {len(complex_logic)}")
    
    # 5. Performance optimization tips
    def optimized_query_patterns():
        """Wzorce dla optymalnej wydajności query"""
        
        # ✅ Dobrze - używaj indeksów
        df_indexed = df.set_index('customer_id')
        indexed_query = df_indexed.query("index > 1000 and order_value > 200")
        
        # ✅ Dobrze - proste warunki na początku
        optimized = df.query("""
            order_value > 100 and
            product_category == 'Electronics' and  
            customer_age > 25
        """)
        
        # ❌ Unikaj - złożone string operations w query
        # Lepiej pre-compute
        df['is_electronics'] = df['product_category'] == 'Electronics'
        better_query = df.query("is_electronics and order_value > 100")
        
        return len(optimized), len(better_query)
    
    opt1, opt2 = optimized_query_patterns()
    print(f"\nOptimization examples: {opt1}, {opt2}")

advanced_query_patterns()
```

---

### 🔄 Index Alignment i Reindexing

#### Automatic index alignment

```python
def demonstrate_index_alignment():
    """Demonstracja automatic index alignment"""
    
    # Tworzenie Series z różnymi indeksami
    s1 = pd.Series([1, 2, 3, 4, 5], index=['A', 'B', 'C', 'D', 'E'])
    s2 = pd.Series([10, 20, 30, 40], index=['C', 'D', 'E', 'F'])
    
    print("Series 1:")
    print(s1)
    print("\nSeries 2:")
    print(s2)
    
    # Automatic alignment podczas operacji
    print(f"\n1. Automatic Alignment:")
    
    result = s1 + s2
    print("s1 + s2 (automatic alignment):")
    print(result)
    print(f"Note: Missing values become NaN")
    
    # 2. Alignment z różnymi strategiami
    print(f"\n2. Different Fill Strategies:")
    
    # Add with fill_value
    result_fill_zero = s1.add(s2, fill_value=0)
    print("Add with fill_value=0:")
    print(result_fill_zero)
    
    # Multiply with fill_value
    result_fill_one = s1.multiply(s2, fill_value=1)
    print("\nMultiply with fill_value=1:")
    print(result_fill_one)
    
    # 3. DataFrame alignment
    print(f"\n3. DataFrame Alignment:")
    
    df1 = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    }, index=[1, 2, 3])
    
    df2 = pd.DataFrame({
        'B': [10, 20, 30],
        'C': [40, 50, 60]  
    }, index=[2, 3, 4])
    
    print("DataFrame 1:")
    print(df1)
    print("\nDataFrame 2:")
    print(df2)
    
    df_sum = df1 + df2
    print("\nDataFrame sum (aligned):")
    print(df_sum)
    
    # 4. Manual alignment z reindex
    print(f"\n4. Manual Alignment:")
    
    # Align to specific index
    s2_aligned = s2.reindex(s1.index)
    print("s2 reindexed to match s1:")
    print(s2_aligned)
    
    # Forward fill missing values
    s2_ffill = s2.reindex(s1.index, method='ffill')
    print("\nReindex with forward fill:")
    print(s2_ffill)
    
    # Backward fill
    s2_bfill = s2.reindex(s1.index, method='bfill')  
    print("\nReindex with backward fill:")
    print(s2_bfill)

demonstrate_index_alignment()
```

#### Advanced reindexing techniques

```python
def advanced_reindexing():
    """Zaawansowane techniki reindexing"""
    
    # Time series data dla demonstracji
    dates = pd.date_range('2023-01-01', periods=10, freq='D')
    ts = pd.Series(np.random.randn(10), index=dates)
    
    print("Original time series:")
    print(ts)
    
    # 1. Reindexing z nowym frequency
    print(f"\n1. Frequency Change:")
    
    # Resample to hourly (upsampling)
    hourly_index = pd.date_range('2023-01-01', '2023-01-10', freq='6H')
    ts_hourly = ts.reindex(hourly_index)
    print(f"Reindexed to 6-hourly: {len(ts_hourly)} points")
    
    # Interpolation
    ts_interpolated = ts.reindex(hourly_index).interpolate()
    print(f"With interpolation, non-null: {ts_interpolated.count()}")
    
    # 2. Custom reindexing functions
    print(f"\n2. Custom Reindexing:")
    
    def custom_fill_func(series, new_index):
        """Custom funkcja do fill missing values podczas reindex"""
        result = series.reindex(new_index)
        
        # Fill with moving average of neighboring values
        for i, idx in enumerate(new_index):
            if pd.isna(result.iloc[i]):
                # Find nearest non-null values
                before_vals = series[series.index < idx]
                after_vals = series[series.index > idx]
                
                if not before_vals.empty and not after_vals.empty:
                    result.iloc[i] = (before_vals.iloc[-1] + after_vals.iloc[0]) / 2
                elif not before_vals.empty:
                    result.iloc[i] = before_vals.iloc[-1]
                elif not after_vals.empty:
                    result.iloc[i] = after_vals.iloc[0]
        
        return result
    
    custom_filled = custom_fill_func(ts, hourly_index)
    print(f"Custom fill non-null: {custom_filled.count()}")
    
    # 3. MultiIndex reindexing
    print(f"\n3. MultiIndex Reindexing:")
    
    # Create MultiIndex DataFrame
    arrays = [['A', 'A', 'B', 'B'], ['X', 'Y', 'X', 'Y']]
    multi_index = pd.MultiIndex.from_arrays(arrays, names=['Level1', 'Level2'])
    df_multi = pd.DataFrame(np.random.randn(4, 3), index=multi_index, columns=['Col1', 'Col2', 'Col3'])
    
    print("Original MultiIndex DataFrame:")
    print(df_multi)
    
    # New MultiIndex with additional combinations
    new_arrays = [['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C'], 
                  ['X', 'Y', 'Z', 'X', 'Y', 'Z', 'X', 'Y']]
    new_multi_index = pd.MultiIndex.from_arrays(new_arrays, names=['Level1', 'Level2'])
    
    reindexed_multi = df_multi.reindex(new_multi_index)
    print("\nReindexed MultiIndex DataFrame:")
    print(reindexed_multi)
    
    # 4. Alignment z różnymi DataFrame shapes
    print(f"\n4. Shape-Changing Alignment:")
    
    df_wide = pd.DataFrame(np.random.randn(3, 5), 
                          index=['X', 'Y', 'Z'], 
                          columns=['A', 'B', 'C', 'D', 'E'])
    
    df_tall = pd.DataFrame(np.random.randn(5, 3),
                          index=['X', 'Y', 'Z', 'W', 'V'],
                          columns=['A', 'B', 'C'])
    
    print(f"Wide DataFrame shape: {df_wide.shape}")
    print(f"Tall DataFrame shape: {df_tall.shape}")
    
    # Align both to common shape
    aligned_wide, aligned_tall = df_wide.align(df_tall, fill_value=0)
    print(f"Aligned wide shape: {aligned_wide.shape}")
    print(f"Aligned tall shape: {aligned_tall.shape}")
    
    # Operation on aligned DataFrames
    result = aligned_wide + aligned_tall
    print(f"Operation result shape: {result.shape}")

advanced_reindexing()
```

---

### 🎛️ Index Manipulation i Performance

#### Index operations performance

```python
def index_performance_analysis():
    """Analiza wydajności operacji na indeksach"""
    
    import time
    
    # Przygotowanie danych testowych
    n = 100000
    
    # DataFrame bez indeksu (default RangeIndex)
    df_no_index = pd.DataFrame({
        'id': range(n),
        'value': np.random.randn(n),
        'category': np.random.choice(['A', 'B', 'C'], n)
    })
    
    # DataFrame z indeksem na 'id'  
    df_indexed = df_no_index.set_index('id')
    
    # DataFrame z MultiIndex
    df_no_index['subcategory'] = np.random.choice(['X', 'Y'], n)
    df_multi_indexed = df_no_index.set_index(['category', 'subcategory'])
    
    print("Performance Analysis of Index Operations:")
    print("=" * 50)
    
    # 1. Selection performance
    print("1. Selection Performance:")
    
    # Random IDs dla testów
    test_ids = np.random.choice(range(n), 1000, replace=False)
    
    # No index - boolean mask
    start = time.time()
    result_no_index = df_no_index[df_no_index['id'].isin(test_ids)]
    no_index_time = time.time() - start
    
    # With index - loc
    start = time.time()
    result_indexed = df_indexed.loc[test_ids]
    indexed_time = time.time() - start
    
    print(f"No index (boolean): {no_index_time:.6f}s")
    print(f"With index (loc): {indexed_time:.6f}s")
    print(f"Speedup: {no_index_time/indexed_time:.2f}x")
    
    # 2. Groupby performance
    print(f"\n2. GroupBy Performance:")
    
    # Groupby bez indeksu
    start = time.time()
    grouped_no_index = df_no_index.groupby('category')['value'].mean()
    no_index_group_time = time.time() - start
    
    # Groupby z indeksem  
    start = time.time()
    grouped_multi_index = df_multi_indexed.groupby(level='category')['value'].mean()
    multi_index_group_time = time.time() - start
    
    print(f"GroupBy no index: {no_index_group_time:.6f}s")
    print(f"GroupBy MultiIndex: {multi_index_group_time:.6f}s")
    print(f"Speedup: {no_index_group_time/multi_index_group_time:.2f}x")
    
    # 3. Sorting performance
    print(f"\n3. Sorting Performance:")
    
    # Sort values vs sort_index
    df_unsorted = df_indexed.sample(frac=1)  # Shuffle
    
    start = time.time()
    sorted_values = df_unsorted.sort_values('value')
    sort_values_time = time.time() - start
    
    start = time.time()
    sorted_index = df_unsorted.sort_index()
    sort_index_time = time.time() - start
    
    print(f"Sort by values: {sort_values_time:.6f}s")
    print(f"Sort by index: {sort_index_time:.6f}s")
    print(f"Index sorting speedup: {sort_values_time/sort_index_time:.2f}x")
    
    # 4. Memory usage
    print(f"\n4. Memory Usage:")
    
    def get_memory_usage(df):
        return df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    
    print(f"No index memory: {get_memory_usage(df_no_index):.2f} MB")
    print(f"Single index memory: {get_memory_usage(df_indexed):.2f} MB") 
    print(f"Multi index memory: {get_memory_usage(df_multi_indexed):.2f} MB")

index_performance_analysis()
```

#### Index optimization strategies

```python
class IndexOptimizer:
    """Klasa do optymalizacji indeksów w Pandas"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.analysis = {}
    
    def analyze_columns(self):
        """Analizuj kolumny pod kątem kandydatów na indeks"""
        
        results = {}
        
        for col in self.df.columns:
            if self.df[col].dtype in ['object', 'category', 'int64', 'datetime64[ns]']:
                unique_ratio = self.df[col].nunique() / len(self.df)
                has_nulls = self.df[col].isnull().any()
                
                results[col] = {
                    'unique_count': self.df[col].nunique(),
                    'unique_ratio': unique_ratio,
                    'has_nulls': has_nulls,
                    'dtype': str(self.df[col].dtype),
                    'memory_usage': self.df[col].memory_usage(deep=True),
                    'index_recommendation': self._get_index_recommendation(unique_ratio, has_nulls)
                }
        
        self.analysis = results
        return results
    
    def _get_index_recommendation(self, unique_ratio, has_nulls):
        """Rekomendacja czy kolumna nadaje się na indeks"""
        if has_nulls:
            return "Not recommended (has nulls)"
        elif unique_ratio > 0.95:
            return "Excellent (high uniqueness)"
        elif unique_ratio > 0.7:
            return "Good (moderate uniqueness)"
        elif unique_ratio > 0.3:
            return "Fair (low uniqueness - consider MultiIndex)"
        else:
            return "Poor (too few unique values)"
    
    def suggest_optimal_index(self, frequent_operations=None):
        """Zasugeruj optymalny indeks based na częstych operacjach"""
        
        if not self.analysis:
            self.analyze_columns()
        
        # Default scoring
        scores = {}
        for col, stats in self.analysis.items():
            score = 0
            
            # Uniqueness score
            score += stats['unique_ratio'] * 40
            
            # No nulls bonus
            if not stats['has_nulls']:
                score += 20
            
            # Data type preferences
            if 'int' in stats['dtype'] or 'datetime' in stats['dtype']:
                score += 15
            elif stats['dtype'] == 'category':
                score += 10
            
            # Memory efficiency (lower is better)
            memory_penalty = min(stats['memory_usage'] / 1024 / 1024, 10)  # Max 10 point penalty
            score -= memory_penalty
            
            scores[col] = score
        
        # Adjust scores based on frequent operations
        if frequent_operations:
            for operation in frequent_operations:
                if operation['type'] == 'selection' and 'column' in operation:
                    scores[operation['column']] += 30
                elif operation['type'] == 'groupby' and 'column' in operation:
                    scores[operation['column']] += 25
                elif operation['type'] == 'sort' and 'column' in operation:
                    scores[operation['column']] += 15
        
        # Return sorted recommendations
        sorted_recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'primary_recommendation': sorted_recommendations[0] if sorted_recommendations else None,
            'all_scores': sorted_recommendations,
            'multiindex_candidates': [col for col, score in sorted_recommendations[:3]]
        }
    
    def create_optimized_dataframe(self, index_config):
        """Utwórz zoptymalizowany DataFrame z recomme nded indeksem"""
        
        df_optimized = self.df.copy()
        
        if isinstance(index_config, str):
            # Single column index
            df_optimized = df_optimized.set_index(index_config)
        elif isinstance(index_config, list):
            # MultiIndex
            df_optimized = df_optimized.set_index(index_config)
        
        return df_optimized
    
    def benchmark_configurations(self, test_operations):
        """Benchmark różnych konfiguracji indeksu"""
        
        import time
        
        configs = [
            {'name': 'No Index', 'config': None},
            {'name': 'Single Best', 'config': self.suggest_optimal_index()['primary_recommendation'][0]},
            {'name': 'MultiIndex Top 2', 'config': self.suggest_optimal_index()['multiindex_candidates'][:2]}
        ]
        
        results = {}
        
        for config in configs:
            if config['config'] is None:
                test_df = self.df.copy()
            else:
                test_df = self.create_optimized_dataframe(config['config'])
            
            config_results = {}
            
            for operation in test_operations:
                start_time = time.time()
                
                if operation['type'] == 'selection':
                    if 'index' in str(test_df.index.names).lower():
                        # Use index-based selection
                        _ = test_df.loc[test_df.index.isin(operation['values'])]
                    else:
                        # Use column-based selection
                        _ = test_df[test_df[operation['column']].isin(operation['values'])]
                
                elif operation['type'] == 'groupby':
                    if operation['column'] in test_df.index.names:
                        _ = test_df.groupby(level=operation['column']).mean()
                    else:
                        _ = test_df.groupby(operation['column']).mean()
                
                operation_time = time.time() - start_time
                config_results[operation['name']] = operation_time
            
            results[config['name']] = config_results
        
        return results

# Przykład użycia OptimizeR
def demonstrate_index_optimizer():
    """Demonstracja użycia Index Optimizer"""
    
    # Tworzenie przykładowych danych
    np.random.seed(42)
    n = 50000
    
    df_test = pd.DataFrame({
        'customer_id': np.random.randint(1, 10000, n),
        'product_id': np.random.randint(1, 1000, n),  
        'order_date': pd.date_range('2022-01-01', periods=n, freq='H'),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n),
        'value': np.random.exponential(100, n),
        'quantity': np.random.poisson(3, n)
    })
    
    # Tworzenie optimizera
    optimizer = IndexOptimizer(df_test)
    
    # Analiza kolumn
    analysis = optimizer.analyze_columns()
    print("Column Analysis:")
    print("=" * 50)
    for col, stats in analysis.items():
        print(f"{col:15}: {stats['index_recommendation']:30} "
              f"(unique: {stats['unique_ratio']:.3f})")
    
    # Sugestie optymalizacji
    suggestions = optimizer.suggest_optimal_index([
        {'type': 'selection', 'column': 'customer_id'},
        {'type': 'groupby', 'column': 'category'},
        {'type': 'selection', 'column': 'product_id'}
    ])
    
    print(f"\nRecommendations:")
    print(f"Primary: {suggestions['primary_recommendation']}")
    print(f"MultiIndex candidates: {suggestions['multiindex_candidates']}")
    
    # Benchmark konfiguracji
    test_ops = [
        {
            'type': 'selection',
            'name': 'customer_selection', 
            'column': 'customer_id',
            'values': np.random.choice(range(1, 10000), 100)
        },
        {
            'type': 'groupby',
            'name': 'category_groupby',
            'column': 'category'
        }
    ]
    
    benchmark_results = optimizer.benchmark_configurations(test_ops)
    
    print(f"\nBenchmark Results:")
    print("=" * 50)
    for config, results in benchmark_results.items():
        print(f"\n{config}:")
        for op_name, time_taken in results.items():
            print(f"  {op_name}: {time_taken:.6f}s")

demonstrate_index_optimizer()
```

---

### 🔗 Powiązane tematy

- [[Pandas - Wprowadzenie do DataFrame]] - Podstawy Pandas
- [[Pandas - Performance Optimization]] - Optymalizacja wydajności
- [[Pandas - GroupBy Operations]] - Operacje grupowe
- [[EDA - Exploratory Data Analysis]] - Analiza eksploracyjna danych