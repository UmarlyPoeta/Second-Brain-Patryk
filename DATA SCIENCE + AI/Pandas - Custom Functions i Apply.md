## 🔧 Pandas - Custom Functions i Apply

_Zaawansowane techniki tworzenia i wykorzystania custom functions w Pandas_

---

### 📝 Wprowadzenie do custom functions

**Custom functions w Pandas** to potężne narzędzia do:

1. **Apply methods** - `.apply()`, `.applymap()`, `.map()`
2. **Lambda functions** - anonimowe funkcje dla prostych operacji
3. **User-defined functions** - złożone custom funkcje
4. **Vectorized functions** - optimized custom operations
5. **Window functions** - rolling i expanding calculations

---

### 🎯 Apply Methods - Fundamenty

#### Understanding apply, map, applymap

```python
import pandas as pd
import numpy as np
import time

def demonstrate_apply_methods():
    """Demonstracja różnych apply methods"""
    
    # Test data
    np.random.seed(42)
    df = pd.DataFrame({
        'A': np.random.randn(1000),
        'B': np.random.randn(1000),
        'C': np.random.choice(['X', 'Y', 'Z'], 1000),
        'D': np.random.randint(1, 100, 1000)
    })
    
    print("Apply Methods Comparison:")
    print("=" * 40)
    
    # 1. DataFrame.apply() - działanie na wierszach lub kolumnach
    print("1. DataFrame.apply():")
    
    # Apply na kolumnach (axis=0, domyślny)
    column_means = df[['A', 'B', 'D']].apply(np.mean)
    print("Column means:")
    print(column_means)
    
    # Apply na wierszach (axis=1)
    def row_sum_squares(row):
        return row['A']**2 + row['B']**2
    
    row_results = df.apply(row_sum_squares, axis=1)
    print(f"\nRow-wise results shape: {row_results.shape}")
    
    # 2. Series.apply() - transformacja każdego elementu
    print(f"\n2. Series.apply():")
    
    def categorize_value(x):
        if x > 1:
            return 'High'
        elif x > 0:
            return 'Medium'
        else:
            return 'Low'
    
    categorized = df['A'].apply(categorize_value)
    print(f"Categorized values:")
    print(categorized.value_counts())
    
    # 3. Series.map() - mapping values (faster dla dict lookups)
    print(f"\n3. Series.map():")
    
    mapping_dict = {'X': 1, 'Y': 2, 'Z': 3}
    mapped_values = df['C'].map(mapping_dict)
    print(f"Mapped values:")
    print(mapped_values.head())
    
    # 4. DataFrame.applymap() - element-wise na wszystkich columns
    print(f"\n4. DataFrame.applymap():")
    
    # Apply function to every element
    df_subset = df[['A', 'B']].head(3)
    rounded_df = df_subset.applymap(lambda x: round(x, 2))
    print("Original:")
    print(df_subset)
    print("Rounded:")
    print(rounded_df)
    
    # 5. Performance comparison
    print(f"\n5. Performance Comparison:")
    
    # Test function
    def test_function(x):
        return x * 2 + 1
    
    test_series = df['A']
    
    # apply
    start = time.time()
    result_apply = test_series.apply(test_function)
    apply_time = time.time() - start
    
    # vectorized operation
    start = time.time()
    result_vectorized = test_series * 2 + 1
    vectorized_time = time.time() - start
    
    print(f"Apply time: {apply_time:.6f}s")
    print(f"Vectorized time: {vectorized_time:.6f}s")
    print(f"Vectorized speedup: {apply_time/vectorized_time:.1f}x")
    print(f"Results equal: {np.allclose(result_apply, result_vectorized)}")

demonstrate_apply_methods()
```

#### Advanced apply patterns

```python
def advanced_apply_patterns():
    """Zaawansowane wzorce użycia apply"""
    
    # Complex test data
    np.random.seed(42)
    df = pd.DataFrame({
        'customer_id': range(1000),
        'age': np.random.normal(35, 10, 1000).astype(int),
        'income': np.random.exponential(50000, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000),
        'purchase_history': [np.random.randint(1, 20, np.random.randint(1, 10)).tolist() 
                            for _ in range(1000)],
        'last_purchase_date': pd.date_range('2020-01-01', periods=1000, freq='D')
    })
    
    print("Advanced Apply Patterns:")
    print("=" * 40)
    
    # 1. Multiple column operations
    print("1. Multiple Column Operations:")
    
    def customer_segmentation(row):
        """Complex segmentation logic"""
        score = 0
        
        # Age factor
        if 25 <= row['age'] <= 45:
            score += 2
        elif row['age'] > 45:
            score += 1
        
        # Income factor
        if row['income'] > 75000:
            score += 3
        elif row['income'] > 50000:
            score += 2
        elif row['income'] > 25000:
            score += 1
        
        # Category factor
        if row['category'] == 'A':
            score += 2
        elif row['category'] == 'B':
            score += 1
        
        # Purchase history factor
        avg_purchase = np.mean(row['purchase_history'])
        if avg_purchase > 15:
            score += 2
        elif avg_purchase > 10:
            score += 1
        
        # Segment classification
        if score >= 7:
            return 'Premium'
        elif score >= 4:
            return 'Standard'
        else:
            return 'Basic'
    
    df['segment'] = df.apply(customer_segmentation, axis=1)
    print("Segmentation results:")
    print(df['segment'].value_counts())
    
    # 2. Conditional operations with apply
    print(f"\n2. Conditional Operations:")
    
    def conditional_discount(row):
        """Apply different discount logic per segment"""
        base_discount = 0
        
        if row['segment'] == 'Premium':
            base_discount = 0.20
        elif row['segment'] == 'Standard':
            base_discount = 0.10
        else:
            base_discount = 0.05
        
        # Additional discount dla high income
        if row['income'] > 80000:
            base_discount += 0.05
        
        # Additional discount dla loyal customers (many purchases)
        if len(row['purchase_history']) > 7:
            base_discount += 0.03
        
        return min(base_discount, 0.30)  # Cap at 30%
    
    df['discount_rate'] = df.apply(conditional_discount, axis=1)
    
    print("Discount rate statistics:")
    print(df.groupby('segment')['discount_rate'].describe())
    
    # 3. Complex string operations
    print(f"\n3. Complex String Operations:")
    
    df['customer_code'] = df['category'] + df['customer_id'].astype(str)
    
    def generate_customer_summary(row):
        """Generate complex customer summary"""
        summary_parts = []
        
        # Basic info
        summary_parts.append(f"ID:{row['customer_id']}")
        summary_parts.append(f"Age:{row['age']}")
        
        # Income bracket
        if row['income'] > 75000:
            income_bracket = 'HIGH'
        elif row['income'] > 40000:
            income_bracket = 'MED'
        else:
            income_bracket = 'LOW'
        summary_parts.append(f"Inc:{income_bracket}")
        
        # Purchase pattern
        purchases = row['purchase_history']
        avg_purchase = np.mean(purchases)
        purchase_pattern = f"Avg:{avg_purchase:.1f}"
        summary_parts.append(purchase_pattern)
        
        # Days since last purchase
        days_since = (pd.Timestamp.now() - row['last_purchase_date']).days
        summary_parts.append(f"Days:{days_since}")
        
        return "|".join(summary_parts)
    
    df['summary'] = df.apply(generate_customer_summary, axis=1)
    print("Sample customer summaries:")
    print(df['summary'].head(3).values)
    
    return df

df_advanced = advanced_apply_patterns()
```

---

### 🚀 Optimizing Custom Functions

#### Vectorized alternatives to apply

```python
def optimize_custom_functions():
    """Techniki optymalizacji custom functions"""
    
    # Test data
    np.random.seed(42)
    n = 100000
    df = pd.DataFrame({
        'values': np.random.randn(n),
        'categories': np.random.choice(['A', 'B', 'C'], n),
        'flags': np.random.choice([True, False], n),
        'amounts': np.random.exponential(100, n)
    })
    
    print("Function Optimization Strategies:")
    print("=" * 50)
    
    # Example 1: Conditional logic optimization
    print("1. Conditional Logic Optimization:")
    
    # ❌ Slow: Apply with complex function
    def slow_categorization(row):
        if row['values'] > 1:
            return 'High'
        elif row['values'] > 0:
            return 'Medium'
        elif row['values'] > -1:
            return 'Low'
        else:
            return 'Very Low'
    
    start = time.time()
    result_slow = df.head(10000).apply(slow_categorization, axis=1)
    slow_time = time.time() - start
    
    # ✅ Fast: Vectorized with np.select
    conditions = [
        df['values'] > 1,
        df['values'] > 0,
        df['values'] > -1
    ]
    choices = ['High', 'Medium', 'Low']
    
    start = time.time()
    result_fast = pd.Series(np.select(conditions, choices, default='Very Low'), index=df.index)
    fast_time = time.time() - start
    
    print(f"Slow apply (10k rows): {slow_time:.6f}s")
    print(f"Fast vectorized (100k rows): {fast_time:.6f}s")
    print(f"Estimated speedup: {(slow_time * 10)/fast_time:.0f}x")
    
    # Example 2: Mathematical operations optimization
    print(f"\n2. Mathematical Operations:")
    
    # ❌ Slow: Apply with mathematical function
    def slow_math_func(row):
        return np.sqrt(row['values']**2 + row['amounts']**2) * (1 if row['flags'] else 0.5)
    
    start = time.time()
    result_math_slow = df.head(10000).apply(slow_math_func, axis=1)
    math_slow_time = time.time() - start
    
    # ✅ Fast: Vectorized mathematical operations
    start = time.time()
    multiplier = np.where(df['flags'], 1, 0.5)
    result_math_fast = np.sqrt(df['values']**2 + df['amounts']**2) * multiplier
    math_fast_time = time.time() - start
    
    print(f"Slow math apply (10k rows): {math_slow_time:.6f}s")
    print(f"Fast math vectorized (100k rows): {math_fast_time:.6f}s")
    print(f"Estimated speedup: {(math_slow_time * 10)/math_fast_time:.0f}x")
    
    # Example 3: String operations optimization
    print(f"\n3. String Operations:")
    
    df['text_col'] = df['categories'] + '_' + df.index.astype(str)
    
    # ❌ Slow: Apply dla string operations
    def slow_string_func(text):
        parts = text.split('_')
        return f"{parts[0].lower()}:{len(parts[1])}"
    
    start = time.time()
    result_string_slow = df['text_col'].head(10000).apply(slow_string_func)
    string_slow_time = time.time() - start
    
    # ✅ Fast: Vectorized string operations
    start = time.time()
    text_series = df['text_col']
    parts_0 = text_series.str.split('_').str[0].str.lower()
    parts_1_len = text_series.str.split('_').str[1].str.len()
    result_string_fast = parts_0 + ':' + parts_1_len.astype(str)
    string_fast_time = time.time() - start
    
    print(f"Slow string apply (10k rows): {string_slow_time:.6f}s")
    print(f"Fast string vectorized (100k rows): {string_fast_time:.6f}s")
    print(f"Estimated speedup: {(string_slow_time * 10)/string_fast_time:.0f}x")
    
    # Example 4: Using numba dla kompilacji JIT
    try:
        from numba import jit, vectorize
        
        print(f"\n4. Numba JIT Compilation:")
        
        # Standard function
        def standard_complex_func(values, amounts):
            result = np.zeros(len(values))
            for i in range(len(values)):
                if values[i] > 0:
                    result[i] = np.log(1 + amounts[i]) * values[i]
                else:
                    result[i] = -np.sqrt(abs(values[i]) + 1)
            return result
        
        # JIT compiled function
        @jit(nopython=True)
        def jit_complex_func(values, amounts):
            result = np.zeros(len(values))
            for i in range(len(values)):
                if values[i] > 0:
                    result[i] = np.log(1 + amounts[i]) * values[i]
                else:
                    result[i] = -np.sqrt(abs(values[i]) + 1)
            return result
        
        # Benchmark
        values_array = df['values'].values
        amounts_array = df['amounts'].values
        
        start = time.time()
        result_standard = standard_complex_func(values_array[:10000], amounts_array[:10000])
        standard_jit_time = time.time() - start
        
        start = time.time()
        result_jit = jit_complex_func(values_array, amounts_array)
        jit_time = time.time() - start
        
        print(f"Standard function (10k rows): {standard_jit_time:.6f}s")
        print(f"JIT compiled (100k rows): {jit_time:.6f}s")
        print(f"Estimated speedup: {(standard_jit_time * 10)/jit_time:.0f}x")
        
    except ImportError:
        print("4. Numba not available - install with: pip install numba")

optimize_custom_functions()
```

#### Caching and memoization

```python
def demonstrate_caching_techniques():
    """Demonstracja caching techniques dla expensive functions"""
    
    from functools import lru_cache
    import hashlib
    
    # Test data
    np.random.seed(42)
    df = pd.DataFrame({
        'input_values': np.random.choice([1, 2, 3, 4, 5], 10000),  # Limited unique values
        'multiplier': np.random.choice([0.5, 1.0, 1.5, 2.0], 10000)
    })
    
    print("Caching Techniques:")
    print("=" * 30)
    
    # Example 1: LRU Cache dla expensive computations
    print("1. LRU Cache for Expensive Functions:")
    
    # Expensive function bez cache
    def expensive_computation(x):
        """Simulate expensive computation"""
        time.sleep(0.001)  # Simulate delay
        return x ** 3 + 2 * x ** 2 + x + 1
    
    # Same function z LRU cache
    @lru_cache(maxsize=128)
    def cached_expensive_computation(x):
        """Same function with caching"""
        time.sleep(0.001)  # Simulate delay
        return x ** 3 + 2 * x ** 2 + x + 1
    
    # Benchmark without cache
    start = time.time()
    results_no_cache = df['input_values'].head(1000).apply(expensive_computation)
    no_cache_time = time.time() - start
    
    # Benchmark with cache
    start = time.time()
    results_with_cache = df['input_values'].head(1000).apply(cached_expensive_computation)
    cache_time = time.time() - start
    
    print(f"Without cache (1000 calls): {no_cache_time:.4f}s")
    print(f"With cache (1000 calls): {cache_time:.4f}s")
    print(f"Cache speedup: {no_cache_time/cache_time:.1f}x")
    print(f"Cache info: {cached_expensive_computation.cache_info()}")
    
    # Example 2: Manual caching with dictionaries
    print(f"\n2. Manual Dictionary Caching:")
    
    computation_cache = {}
    
    def manually_cached_function(x, multiplier):
        """Function z manual caching"""
        # Create cache key
        cache_key = (x, multiplier)
        
        if cache_key not in computation_cache:
            # Expensive computation
            result = (x ** 2 * multiplier) + np.sin(x) * multiplier
            computation_cache[cache_key] = result
            return result
        else:
            return computation_cache[cache_key]
    
    # Apply function z manual caching
    def apply_cached_function(row):
        return manually_cached_function(row['input_values'], row['multiplier'])
    
    start = time.time()
    cached_results = df.head(5000).apply(apply_cached_function, axis=1)
    manual_cache_time = time.time() - start
    
    print(f"Manual cache time (5000 calls): {manual_cache_time:.4f}s")
    print(f"Cache size: {len(computation_cache)} entries")
    print(f"Unique combinations in data: {df[['input_values', 'multiplier']].drop_duplicates().shape[0]}")
    
    # Example 3: Pandas-specific caching with groupby
    print(f"\n3. GroupBy-based Optimization:")
    
    def complex_group_function(group_data):
        """Complex operation on grouped data"""
        return {
            'mean': group_data.mean(),
            'std': group_data.std(),
            'custom_metric': (group_data ** 2).sum() / len(group_data)
        }
    
    # Group once, apply multiple operations
    grouped = df.groupby(['input_values', 'multiplier'])
    
    start = time.time()
    group_results = grouped['input_values'].apply(lambda x: complex_group_function(x))
    groupby_time = time.time() - start
    
    print(f"GroupBy optimization time: {groupby_time:.4f}s")
    print(f"Number of groups: {grouped.ngroups}")

demonstrate_caching_techniques()
```

---

### 🎨 Advanced Function Patterns

#### Closures and function factories

```python
def demonstrate_advanced_function_patterns():
    """Zaawansowane wzorce funkcji w Pandas"""
    
    # Test data
    np.random.seed(42)
    df = pd.DataFrame({
        'sales': np.random.exponential(1000, 1000),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 1000),
        'product': np.random.choice(['A', 'B', 'C'], 1000),
        'date': pd.date_range('2023-01-01', periods=1000, freq='D')
    })
    
    print("Advanced Function Patterns:")
    print("=" * 40)
    
    # 1. Function factories
    print("1. Function Factories:")
    
    def create_threshold_classifier(thresholds):
        """Factory tworzące classifier functions"""
        def classifier(value):
            for i, threshold in enumerate(sorted(thresholds)):
                if value <= threshold:
                    return f"Level_{i+1}"
            return f"Level_{len(thresholds)+1}"
        return classifier
    
    # Create different classifiers
    sales_classifier = create_threshold_classifier([500, 1000, 2000])
    performance_classifier = create_threshold_classifier([200, 800, 1500])
    
    # Apply classifiers
    df['sales_level'] = df['sales'].apply(sales_classifier)
    df['performance_level'] = df['sales'].apply(performance_classifier)
    
    print("Sales levels distribution:")
    print(df['sales_level'].value_counts())
    print("\nPerformance levels distribution:")
    print(df['performance_level'].value_counts())
    
    # 2. Closures z state
    print(f"\n2. Closures with State:")
    
    def create_running_calculator():
        """Closure z running state"""
        running_sum = 0
        count = 0
        
        def calculate(value):
            nonlocal running_sum, count
            running_sum += value
            count += 1
            return running_sum / count  # Running average
        
        return calculate
    
    # Create calculator instance
    running_avg_calculator = create_running_calculator()
    
    # Apply to subset of data
    sample_data = df['sales'].head(10)
    running_averages = sample_data.apply(running_avg_calculator)
    
    print("Running averages for first 10 sales:")
    for i, (sale, avg) in enumerate(zip(sample_data, running_averages)):
        print(f"Sale {i+1}: {sale:.2f}, Running Avg: {avg:.2f}")
    
    # 3. Multi-stage functions
    print(f"\n3. Multi-stage Functions:")
    
    def create_multi_stage_processor(stages):
        """Multi-stage processor"""
        def process(value):
            result = value
            for stage_name, stage_func in stages.items():
                result = stage_func(result)
            return result
        return process
    
    # Define processing stages
    stages = {
        'normalize': lambda x: x / 1000,  # Convert to thousands
        'log_transform': lambda x: np.log1p(x) if x > 0 else 0,
        'scale': lambda x: x * 10  # Scale up
    }
    
    multi_processor = create_multi_stage_processor(stages)
    df['processed_sales'] = df['sales'].apply(multi_processor)
    
    print("Original vs processed sales (first 5 rows):")
    print(df[['sales', 'processed_sales']].head())
    
    # 4. Conditional function application
    print(f"\n4. Conditional Function Application:")
    
    def create_conditional_processor(conditions_functions):
        """Apply different functions based na conditions"""
        def process(row):
            for condition, func in conditions_functions:
                if condition(row):
                    return func(row)
            return None  # No condition met
        
        return process
    
    # Define conditional functions
    def high_sales_bonus(row):
        return row['sales'] * 0.1 if row['sales'] > 1500 else 0
    
    def regional_bonus(row):
        multipliers = {'North': 1.2, 'South': 1.0, 'East': 1.1, 'West': 0.9}
        return row['sales'] * (multipliers.get(row['region'], 1.0) - 1)
    
    def product_bonus(row):
        bonuses = {'A': 100, 'B': 150, 'C': 75}
        return bonuses.get(row['product'], 0)
    
    # Conditional functions
    conditional_functions = [
        (lambda row: row['sales'] > 1500, high_sales_bonus),
        (lambda row: row['region'] in ['North', 'East'], regional_bonus),
        (lambda row: True, product_bonus)  # Default case
    ]
    
    conditional_processor = create_conditional_processor(conditional_functions)
    df['bonus'] = df.apply(conditional_processor, axis=1)
    
    print("Bonus statistics by condition:")
    print(f"High sales (>1500): {len(df[df['sales'] > 1500])} records")
    print(f"Regional bonus eligible: {len(df[df['region'].isin(['North', 'East'])])} records")
    print(f"Average bonus: {df['bonus'].mean():.2f}")

demonstrate_advanced_function_patterns()
```

#### Error handling in custom functions

```python
def demonstrate_error_handling():
    """Error handling w custom functions"""
    
    # Test data z potential issues
    df = pd.DataFrame({
        'numbers': [1, 2, 0, -1, np.nan, 5, 'invalid', 10],
        'text': ['hello', '', None, 'world', 'test', np.nan, 'pandas', 'python'],
        'dates': ['2023-01-01', '2023-02-01', 'invalid-date', '2023-03-01', 
                 None, '2023-04-01', '2023-05-01', '2023-06-01']
    })
    
    print("Error Handling in Custom Functions:")
    print("=" * 50)
    
    # 1. Basic try-except w apply
    print("1. Basic Try-Except:")
    
    def safe_sqrt(x):
        """Safe square root z error handling"""
        try:
            if pd.isna(x):
                return np.nan
            x_float = float(x)
            if x_float < 0:
                return np.nan  # Or could return complex number
            return np.sqrt(x_float)
        except (ValueError, TypeError):
            return np.nan
    
    df['sqrt_numbers'] = df['numbers'].apply(safe_sqrt)
    print("Square root results:")
    print(df[['numbers', 'sqrt_numbers']])
    
    # 2. Multiple error handling strategies
    print(f"\n2. Multiple Error Handling Strategies:")
    
    def robust_text_processor(text):
        """Robust text processing z multiple error checks"""
        try:
            # Handle None/NaN
            if pd.isna(text):
                return {'length': 0, 'upper_count': 0, 'error': 'null_value'}
            
            # Convert to string
            text_str = str(text)
            
            # Handle empty string
            if len(text_str) == 0:
                return {'length': 0, 'upper_count': 0, 'error': 'empty_string'}
            
            # Process text
            length = len(text_str)
            upper_count = sum(1 for c in text_str if c.isupper())
            
            return {
                'length': length,
                'upper_count': upper_count,
                'error': None
            }
        
        except Exception as e:
            return {
                'length': -1,
                'upper_count': -1,
                'error': f'processing_error_{type(e).__name__}'
            }
    
    text_results = df['text'].apply(robust_text_processor)
    
    # Extract results into separate columns
    df['text_length'] = text_results.apply(lambda x: x['length'])
    df['text_upper_count'] = text_results.apply(lambda x: x['upper_count'])
    df['text_error'] = text_results.apply(lambda x: x['error'])
    
    print("Text processing results:")
    print(df[['text', 'text_length', 'text_upper_count', 'text_error']])
    
    # 3. Date parsing z fallback strategies
    print(f"\n3. Date Parsing with Fallbacks:")
    
    def flexible_date_parser(date_input):
        """Flexible date parser z multiple strategies"""
        if pd.isna(date_input):
            return {'parsed_date': pd.NaT, 'parse_method': 'null_input'}
        
        # Strategy 1: Standard parsing
        try:
            parsed = pd.to_datetime(date_input)
            return {'parsed_date': parsed, 'parse_method': 'standard'}
        except:
            pass
        
        # Strategy 2: Try different formats
        formats = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%Y%m%d']
        for fmt in formats:
            try:
                parsed = pd.to_datetime(date_input, format=fmt)
                return {'parsed_date': parsed, 'parse_method': f'format_{fmt}'}
            except:
                continue
        
        # Strategy 3: Extract year if possible
        try:
            year_match = pd.Series([str(date_input)]).str.extract(r'(\d{4})')
            if not year_match.iloc[0, 0]:
                raise ValueError("No year found")
            year = int(year_match.iloc[0, 0])
            if 1900 <= year <= 2100:
                fallback_date = pd.to_datetime(f"{year}-01-01")
                return {'parsed_date': fallback_date, 'parse_method': 'year_only'}
        except:
            pass
        
        # Final fallback
        return {'parsed_date': pd.NaT, 'parse_method': 'failed'}
    
    date_results = df['dates'].apply(flexible_date_parser)
    df['parsed_dates'] = date_results.apply(lambda x: x['parsed_date'])
    df['parse_method'] = date_results.apply(lambda x: x['parse_method'])
    
    print("Date parsing results:")
    print(df[['dates', 'parsed_dates', 'parse_method']])
    
    # 4. Logging errors dla debugging
    print(f"\n4. Error Logging:")
    
    error_log = []
    
    def logging_function(row):
        """Function z error logging"""
        try:
            # Attempt some operation
            result = float(row['numbers']) * 2
            if result > 10:
                result = result / 2  # Some conditional logic
            return result
        
        except Exception as e:
            # Log the error
            error_entry = {
                'index': row.name if hasattr(row, 'name') else 'unknown',
                'error_type': type(e).__name__,
                'error_message': str(e),
                'input_value': row['numbers']
            }
            error_log.append(error_entry)
            return np.nan
    
    df['processed_numbers'] = df.apply(logging_function, axis=1)
    
    print("Processing results:")
    print(df[['numbers', 'processed_numbers']])
    
    if error_log:
        print("\nError log:")
        error_df = pd.DataFrame(error_log)
        print(error_df)

demonstrate_error_handling()
```

---

### 🔄 Rolling i Window Functions

#### Custom rolling functions

```python
def demonstrate_custom_rolling_functions():
    """Custom rolling i window functions"""
    
    # Time series data
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    ts_data = pd.DataFrame({
        'date': dates,
        'value': np.cumsum(np.random.randn(100)) + 100,  # Random walk
        'volume': np.random.exponential(1000, 100),
        'category': np.random.choice(['A', 'B'], 100)
    }).set_index('date')
    
    print("Custom Rolling Functions:")
    print("=" * 40)
    
    # 1. Basic custom rolling functions
    print("1. Basic Custom Rolling Functions:")
    
    def rolling_volatility(series, window):
        """Custom volatility calculation"""
        return series.rolling(window).std() / series.rolling(window).mean()
    
    def rolling_sharpe_ratio(series, window, risk_free_rate=0.02):
        """Rolling Sharpe ratio calculation"""
        returns = series.pct_change().dropna()
        rolling_mean = returns.rolling(window).mean() * 252  # Annualized
        rolling_std = returns.rolling(window).std() * np.sqrt(252)  # Annualized
        return (rolling_mean - risk_free_rate) / rolling_std
    
    # Apply custom rolling functions
    ts_data['volatility_10d'] = rolling_volatility(ts_data['value'], 10)
    ts_data['sharpe_10d'] = rolling_sharpe_ratio(ts_data['value'], 10)
    
    print("Rolling metrics (last 10 rows):")
    print(ts_data[['value', 'volatility_10d', 'sharpe_10d']].tail(10))
    
    # 2. Advanced custom window functions
    print(f"\n2. Advanced Window Functions:")
    
    def custom_trend_strength(series):
        """Calculate trend strength w rolling window"""
        if len(series) < 5:
            return np.nan
        
        # Linear regression slope as trend indicator
        x = np.arange(len(series))
        y = series.values
        
        # Simple linear regression
        n = len(x)
        slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)
        
        # Normalize by series mean
        trend_strength = slope / np.mean(y) if np.mean(y) != 0 else 0
        return trend_strength
    
    def rolling_percentile_rank(series):
        """Rolling percentile rank of current value"""
        if len(series) < 2:
            return 0.5
        
        current_value = series.iloc[-1]
        historical_values = series.iloc[:-1]
        
        percentile_rank = (historical_values < current_value).sum() / len(historical_values)
        return percentile_rank
    
    # Apply advanced rolling functions
    ts_data['trend_strength'] = ts_data['value'].rolling(20).apply(custom_trend_strength)
    ts_data['percentile_rank'] = ts_data['value'].rolling(30).apply(rolling_percentile_rank)
    
    print("Advanced rolling metrics (last 10 rows):")
    print(ts_data[['value', 'trend_strength', 'percentile_rank']].tail(10))
    
    # 3. Multi-column rolling functions
    print(f"\n3. Multi-column Rolling Functions:")
    
    def rolling_correlation(df_window):
        """Rolling correlation between value and volume"""
        if len(df_window) < 5:
            return np.nan
        return df_window['value'].corr(df_window['volume'])
    
    def rolling_value_volume_ratio(df_window):
        """Custom ratio calculation"""
        if len(df_window) < 3:
            return np.nan
        
        avg_value = df_window['value'].mean()
        avg_volume = df_window['volume'].mean()
        
        return avg_value / avg_volume if avg_volume != 0 else np.nan
    
    # Apply multi-column rolling functions
    ts_data['rolling_corr'] = ts_data.rolling(15).apply(rolling_correlation)
    ts_data['value_volume_ratio'] = ts_data.rolling(10).apply(rolling_value_volume_ratio)
    
    print("Multi-column rolling metrics (last 10 rows):")
    print(ts_data[['value', 'volume', 'rolling_corr', 'value_volume_ratio']].tail(10))
    
    # 4. Conditional rolling functions
    print(f"\n4. Conditional Rolling Functions:")
    
    def conditional_rolling_mean(group):
        """Rolling mean tylko dla specific conditions"""
        def calculate_conditional_mean(series):
            if len(series) < 5:
                return np.nan
            
            # Only include values above median
            median_val = series.median()
            above_median = series[series > median_val]
            
            return above_median.mean() if len(above_median) > 0 else np.nan
        
        return group['value'].rolling(10).apply(calculate_conditional_mean)
    
    # Apply conditional rolling by category
    ts_data['conditional_mean'] = ts_data.groupby('category').apply(conditional_rolling_mean).values
    
    print("Conditional rolling metrics by category (last 10 rows):")
    print(ts_data[['category', 'value', 'conditional_mean']].tail(10))
    
    return ts_data

ts_result = demonstrate_custom_rolling_functions()
```

---

### 💡 Best Practices for Custom Functions

#### Performance optimization checklist

```python
def custom_functions_best_practices():
    """Best practices dla custom functions w Pandas"""
    
    best_practices = """
    ✅ PERFORMANCE:
    - Preferuj vectorized operations nad .apply()
    - Używaj np.where() dla simple conditional logic
    - Consider .map() dla dictionary lookups
    - Profile functions przed optimization
    
    ✅ ERROR HANDLING:
    - Always handle NaN values explicitly
    - Use try-except dla potentially failing operations
    - Provide meaningful fallback values
    - Log errors for debugging purposes
    
    ✅ FUNCTION DESIGN:
    - Keep functions pure (no side effects)
    - Use type hints dla better documentation
    - Return consistent data types
    - Consider using @lru_cache dla expensive computations
    
    ✅ CODE ORGANIZATION:
    - Use function factories dla configurable functions
    - Implement closures gdy potrzebujesz state
    - Create utility modules dla reusable functions
    - Document function parameters i return values
    
    ✅ TESTING:
    - Test funkcje z edge cases (empty, NaN, extreme values)
    - Verify results z known test cases
    - Benchmark performance regularly
    - Test error handling paths
    """
    
    print("Custom Functions Best Practices:")
    print("=" * 50)
    print(best_practices)

custom_functions_best_practices()

# Przykład comprehensive custom function class
class PandasFunctionLibrary:
    """Library optimized custom functions dla Pandas"""
    
    @staticmethod
    @lru_cache(maxsize=1000)
    def cached_expensive_computation(x, power=2):
        """Cached expensive mathematical computation"""
        time.sleep(0.001)  # Simulate expensive operation
        return x ** power
    
    @staticmethod
    def safe_divide(numerator, denominator, default=0):
        """Safe division z error handling"""
        try:
            if pd.isna(numerator) or pd.isna(denominator):
                return np.nan
            if denominator == 0:
                return default
            return numerator / denominator
        except (TypeError, ValueError):
            return default
    
    @staticmethod
    def robust_string_analyzer(text):
        """Robust string analysis funkcja"""
        if pd.isna(text):
            return {'length': 0, 'words': 0, 'has_numbers': False}
        
        try:
            text_str = str(text)
            return {
                'length': len(text_str),
                'words': len(text_str.split()),
                'has_numbers': bool(pd.Series([text_str]).str.contains(r'\d').iloc[0])
            }
        except Exception:
            return {'length': -1, 'words': -1, 'has_numbers': False}
    
    @classmethod
    def create_threshold_classifier(cls, thresholds, labels=None):
        """Factory method dla threshold classification"""
        if labels is None:
            labels = [f"Level_{i+1}" for i in range(len(thresholds) + 1)]
        
        def classifier(value):
            if pd.isna(value):
                return 'Unknown'
            
            for i, threshold in enumerate(sorted(thresholds)):
                if value <= threshold:
                    return labels[i]
            return labels[-1]
        
        return classifier

# Test comprehensive library
def test_function_library():
    """Test PandasFunctionLibrary"""
    
    # Test data
    df = pd.DataFrame({
        'values': [1, 5, 10, None, 0, -1],
        'denominators': [2, 0, 5, 3, None, 1],
        'text': ['hello world', '', None, '123 test', 'CAPS', 'normal text']
    })
    
    lib = PandasFunctionLibrary()
    
    print("Testing Function Library:")
    print("=" * 30)
    
    # Test cached computation
    df['computed'] = df['values'].apply(lambda x: lib.cached_expensive_computation(x, 3))
    print("Cached computation results:")
    print(df[['values', 'computed']])
    
    # Test safe division
    df['division'] = df.apply(lambda row: lib.safe_divide(row['values'], row['denominators']), axis=1)
    print(f"\nSafe division results:")
    print(df[['values', 'denominators', 'division']])
    
    # Test string analyzer
    string_results = df['text'].apply(lib.robust_string_analyzer)
    df['text_length'] = string_results.apply(lambda x: x['length'])
    df['text_words'] = string_results.apply(lambda x: x['words'])
    df['text_has_numbers'] = string_results.apply(lambda x: x['has_numbers'])
    
    print(f"\nString analysis results:")
    print(df[['text', 'text_length', 'text_words', 'text_has_numbers']])

test_function_library()
```

---

### 🔗 Powiązane tematy

- [[Pandas - Performance Optimization]] - Optymalizacja wydajności
- [[Pandas - Advanced Indexing i MultiIndex]] - Zaawansowane indeksowanie
- [[NumPy - Performance Optimization]] - Optymalizacja NumPy
- [[Feature Engineering - Podstawy]] - Inżynieria cech