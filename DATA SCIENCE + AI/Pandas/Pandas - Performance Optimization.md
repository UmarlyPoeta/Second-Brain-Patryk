## ⚡ Pandas - Performance Optimization

_Techniki optymalizacji wydajności w Pandas dla dużych zbiorów danych_

---

### 📝 Wprowadzenie do optymalizacji Pandas

**Performance optimization w Pandas** obejmuje:

1. **Efficient data types** - wybór optymalnych typów danych
2. **Vectorized operations** - wykorzystanie operacji vectorized
3. **Memory management** - zarządzanie pamięcią
4. **Chunking** - przetwarzanie danych w kawałkach
5. **Parallel processing** - przetwarzanie równoległe
6. **Index optimization** - optymalizacja indeksów

---

### 🔢 Optymalizacja typów danych

#### Automatic dtype optimization

```python
import pandas as pd
import numpy as np
import time

def optimize_dtypes(df):
    """Automatyczna optymalizacja typów danych"""
    
    original_memory = df.memory_usage(deep=True).sum()
    print(f"Original memory usage: {original_memory / 1024 / 1024:.2f} MB")
    
    optimized_df = df.copy()
    
    for col in optimized_df.columns:
        col_type = optimized_df[col].dtype
        
        # Numeric columns
        if col_type != 'object' and col_type.name != 'category' and 'datetime' not in str(col_type):
            c_min = optimized_df[col].min()
            c_max = optimized_df[col].max()
            
            if str(col_type)[:3] == 'int':
                # Integer optimization
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    optimized_df[col] = optimized_df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    optimized_df[col] = optimized_df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    optimized_df[col] = optimized_df[col].astype(np.int32)
                else:
                    optimized_df[col] = optimized_df[col].astype(np.int64)
            else:
                # Float optimization
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    optimized_df[col] = optimized_df[col].astype(np.float32)
                else:
                    optimized_df[col] = optimized_df[col].astype(np.float64)
        
        # Object columns - candidate dla category
        elif col_type == 'object':
            num_unique_values = len(optimized_df[col].unique())
            num_total_values = len(optimized_df[col])
            
            if num_unique_values / num_total_values < 0.5:  # Less than 50% unique
                optimized_df[col] = optimized_df[col].astype('category')
    
    optimized_memory = optimized_df.memory_usage(deep=True).sum()
    print(f"Optimized memory usage: {optimized_memory / 1024 / 1024:.2f} MB")
    print(f"Memory reduction: {(1 - optimized_memory/original_memory) * 100:.1f}%")
    
    return optimized_df

# Przykład optymalizacji
def create_test_dataframe():
    """Tworzenie test dataframe z nieoptymalnymi typami"""
    
    np.random.seed(42)
    n = 100000
    
    df = pd.DataFrame({
        'id': range(n),  # Can be int32
        'small_int': np.random.randint(0, 100, n),  # Can be int8
        'category_col': np.random.choice(['A', 'B', 'C', 'D'], n),  # Should be category
        'large_int': np.random.randint(0, 1000000, n),  # Needs int32
        'float_col': np.random.random(n) * 100,  # Can be float32
        'text_col': ['text_' + str(i % 50) for i in range(n)]  # Should be category
    })
    
    return df

# Test optymalizacji
print("Data Type Optimization Example:")
print("=" * 50)

df_original = create_test_dataframe()
print("Original dtypes:")
print(df_original.dtypes)

df_optimized = optimize_dtypes(df_original)
print(f"\nOptimized dtypes:")
print(df_optimized.dtypes)
```

#### Manual dtype specification

```python
def demonstrate_dtype_strategies():
    """Demonstracja różnych strategii typów danych"""
    
    # Przygotowanie danych CSV (symulacja)
    csv_data = """id,score,category,is_active,timestamp
1,85.5,A,True,2023-01-01 10:00:00
2,92.1,B,False,2023-01-02 11:30:00
3,78.3,A,True,2023-01-03 09:15:00
4,91.7,C,True,2023-01-04 14:20:00
5,83.2,B,False,2023-01-05 16:45:00"""
    
    # Strategy 1: Default reading (inefficient)
    from io import StringIO
    
    start_time = time.time()
    df_default = pd.read_csv(StringIO(csv_data))
    default_time = time.time() - start_time
    
    print("Strategy 1 - Default dtypes:")
    print(df_default.dtypes)
    print(f"Memory: {df_default.memory_usage(deep=True).sum()} bytes")
    
    # Strategy 2: Optimized dtypes specification
    optimized_dtypes = {
        'id': 'int32',
        'score': 'float32', 
        'category': 'category',
        'is_active': 'bool'
    }
    
    start_time = time.time()
    df_optimized = pd.read_csv(
        StringIO(csv_data),
        dtype=optimized_dtypes,
        parse_dates=['timestamp']
    )
    optimized_time = time.time() - start_time
    
    print(f"\nStrategy 2 - Optimized dtypes:")
    print(df_optimized.dtypes)
    print(f"Memory: {df_optimized.memory_usage(deep=True).sum()} bytes")
    
    # Strategy 3: Using converters for complex transformations
    def score_converter(x):
        """Custom converter dla score column"""
        return np.float32(x) if float(x) > 80 else np.float32(x * 0.5)
    
    start_time = time.time()
    df_converted = pd.read_csv(
        StringIO(csv_data),
        dtype={'id': 'int32', 'category': 'category'},
        converters={'score': score_converter},
        parse_dates=['timestamp']
    )
    converted_time = time.time() - start_time
    
    print(f"\nStrategy 3 - With converters:")
    print(df_converted[['id', 'score', 'category']])
    
    print(f"\nReading times:")
    print(f"Default: {default_time:.6f}s")
    print(f"Optimized: {optimized_time:.6f}s") 
    print(f"With converters: {converted_time:.6f}s")

demonstrate_dtype_strategies()
```

---

### ⚡ Vectorized Operations

#### Avoiding Python loops

```python
def vectorization_examples():
    """Przykłady vectorization w Pandas"""
    
    # Tworzenie test data
    np.random.seed(42)
    n = 1000000
    
    df = pd.DataFrame({
        'values': np.random.randn(n),
        'categories': np.random.choice(['A', 'B', 'C'], n),
        'flags': np.random.choice([True, False], n)
    })
    
    print("Vectorization Performance Comparison:")
    print("=" * 50)
    
    # Example 1: Mathematical operations
    print("1. Mathematical Operations:")
    
    # ❌ Slow: Python loop
    start = time.time()
    result_loop = []
    for idx, row in df.head(10000).iterrows():  # Smaller subset for demo
        result_loop.append(row['values'] ** 2 + 10)
    loop_time = time.time() - start
    
    # ✅ Fast: Vectorized
    start = time.time()
    result_vectorized = df['values'] ** 2 + 10
    vectorized_time = time.time() - start
    
    print(f"Loop time (10k records): {loop_time:.6f}s")
    print(f"Vectorized time (1M records): {vectorized_time:.6f}s")
    print(f"Estimated speedup: {(loop_time * 100) / vectorized_time:.0f}x")
    
    # Example 2: Conditional operations
    print(f"\n2. Conditional Operations:")
    
    # ❌ Slow: Apply with lambda
    start = time.time()
    result_apply = df.head(100000).apply(
        lambda row: 'High' if row['values'] > 0 else 'Low', axis=1
    )
    apply_time = time.time() - start
    
    # ✅ Fast: Vectorized conditions
    start = time.time()
    result_vectorized_cond = np.where(df['values'] > 0, 'High', 'Low')
    vectorized_cond_time = time.time() - start
    
    # ✅ Even faster: Using pandas methods
    start = time.time()
    result_pandas_cond = df['values'].map({True: 'High', False: 'Low'}.__getitem__) if False else pd.Series(np.where(df['values'] > 0, 'High', 'Low'))
    pandas_cond_time = time.time() - start
    
    print(f"Apply time (100k records): {apply_time:.6f}s")
    print(f"NumPy where time (1M records): {vectorized_cond_time:.6f}s")
    print(f"Pandas vectorized time: {pandas_cond_time:.6f}s")
    
    # Example 3: String operations
    print(f"\n3. String Operations:")
    
    # Create string data
    string_data = pd.Series(['Hello_World_' + str(i) for i in range(100000)])
    
    # ❌ Slow: Apply
    start = time.time()
    result_string_apply = string_data.apply(lambda x: x.split('_')[0])
    string_apply_time = time.time() - start
    
    # ✅ Fast: Vectorized string methods
    start = time.time()
    result_string_vectorized = string_data.str.split('_').str[0]
    string_vectorized_time = time.time() - start
    
    print(f"String apply time: {string_apply_time:.6f}s")
    print(f"String vectorized time: {string_vectorized_time:.6f}s")
    print(f"String speedup: {string_apply_time/string_vectorized_time:.1f}x")

vectorization_examples()
```

#### Optimized pandas methods

```python
def pandas_optimized_methods():
    """Demonstracja optimized pandas methods"""
    
    # Test data
    np.random.seed(42)
    n = 500000
    
    df = pd.DataFrame({
        'group': np.random.choice(['A', 'B', 'C', 'D'], n),
        'value1': np.random.randn(n),
        'value2': np.random.randn(n),
        'date': pd.date_range('2020-01-01', periods=n, freq='H')
    })
    
    print("Optimized Pandas Methods:")
    print("=" * 40)
    
    # 1. Groupby operations
    print("1. GroupBy Optimization:")
    
    # Standard groupby
    start = time.time()
    result_groupby = df.groupby('group').agg({
        'value1': ['mean', 'std'],
        'value2': ['sum', 'count']
    })
    groupby_time = time.time() - start
    
    # Using transform for broadcasted results
    start = time.time()
    df['group_mean'] = df.groupby('group')['value1'].transform('mean')
    transform_time = time.time() - start
    
    print(f"GroupBy agg time: {groupby_time:.6f}s")
    print(f"Transform time: {transform_time:.6f}s")
    
    # 2. Merge optimization
    print(f"\n2. Merge Optimization:")
    
    # Create lookup table
    lookup = pd.DataFrame({
        'group': ['A', 'B', 'C', 'D'],
        'group_info': ['Info A', 'Info B', 'Info C', 'Info D']
    })
    
    # Standard merge
    start = time.time()
    merged_standard = df.merge(lookup, on='group', how='left')
    merge_time = time.time() - start
    
    # Map method (often faster for simple lookups)
    lookup_dict = lookup.set_index('group')['group_info'].to_dict()
    start = time.time()
    df['group_info_mapped'] = df['group'].map(lookup_dict)
    map_time = time.time() - start
    
    print(f"Merge time: {merge_time:.6f}s")
    print(f"Map time: {map_time:.6f}s")
    print(f"Map speedup: {merge_time/map_time:.1f}x")
    
    # 3. Boolean operations optimization
    print(f"\n3. Boolean Operations:")
    
    # Multiple conditions
    start = time.time()
    mask_standard = (df['value1'] > 0) & (df['value2'] < 0) & (df['group'].isin(['A', 'B']))
    standard_bool_time = time.time() - start
    
    # Using query (can be faster for complex conditions)
    start = time.time()
    mask_query = df.eval('value1 > 0 & value2 < 0')
    query_bool_time = time.time() - start
    
    print(f"Standard boolean time: {standard_bool_time:.6f}s")
    print(f"Eval boolean time: {query_bool_time:.6f}s")
    
    # 4. Sorting optimization
    print(f"\n4. Sorting Optimization:")
    
    # Multiple column sort
    start = time.time()
    sorted_standard = df.sort_values(['group', 'value1'])
    sort_time = time.time() - start
    
    # Index-based operations after sorting
    df_sorted = df.sort_values(['group', 'value1'])
    start = time.time()
    # Operacja która korzysta z sortowania
    grouped_sorted = df_sorted.groupby('group').first()
    sorted_operation_time = time.time() - start
    
    print(f"Sort time: {sort_time:.6f}s")
    print(f"Operation on sorted data: {sorted_operation_time:.6f}s")

pandas_optimized_methods()
```

---

### 💾 Memory Management i Chunking

#### Memory-efficient data loading

```python
def memory_efficient_loading():
    """Memory-efficient strategies dla loading data"""
    
    # Symulacja dużego CSV file
    def create_large_csv_simulation():
        """Symulacja dużego CSV bez tworzenia fizycznego pliku"""
        import tempfile
        import os
        
        # Tworzenie tymczasowego pliku CSV
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        
        # Header
        temp_file.write('id,category,value,date,description\n')
        
        # Generate data
        for i in range(100000):
            category = np.random.choice(['A', 'B', 'C', 'D'])
            value = np.random.normal(100, 20)
            date = f"2023-01-{(i % 28) + 1:02d}"
            description = f"Description_{i % 1000}"
            temp_file.write(f"{i},{category},{value:.2f},{date},{description}\n")
        
        temp_file.close()
        return temp_file.name
    
    csv_file = create_large_csv_simulation()
    
    print("Memory-Efficient Loading Strategies:")
    print("=" * 50)
    
    # Strategy 1: Load everything (memory intensive)
    start = time.time()
    df_full = pd.read_csv(csv_file)
    full_time = time.time() - start
    full_memory = df_full.memory_usage(deep=True).sum() / 1024 / 1024
    
    print(f"1. Full Load:")
    print(f"   Time: {full_time:.4f}s")
    print(f"   Memory: {full_memory:.2f} MB")
    
    # Strategy 2: Chunked loading
    def process_chunks(filename, chunk_size=10000):
        """Process file w chunks"""
        results = []
        
        start = time.time()
        for chunk in pd.read_csv(filename, chunksize=chunk_size):
            # Process each chunk
            processed = chunk.groupby('category')['value'].mean()
            results.append(processed)
        
        # Combine results
        final_result = pd.concat(results).groupby(level=0).mean()
        chunk_time = time.time() - start
        
        return final_result, chunk_time
    
    chunk_result, chunk_time = process_chunks(csv_file)
    
    print(f"\n2. Chunked Processing:")
    print(f"   Time: {chunk_time:.4f}s")
    print(f"   Result shape: {chunk_result.shape}")
    print(f"   Peak memory: Much lower (only chunk in memory)")
    
    # Strategy 3: Selective column loading
    start = time.time()
    df_selective = pd.read_csv(csv_file, usecols=['category', 'value'])
    selective_time = time.time() - start
    selective_memory = df_selective.memory_usage(deep=True).sum() / 1024 / 1024
    
    print(f"\n3. Selective Columns:")
    print(f"   Time: {selective_time:.4f}s")
    print(f"   Memory: {selective_memory:.2f} MB")
    print(f"   Memory reduction: {(1-selective_memory/full_memory)*100:.1f}%")
    
    # Strategy 4: Optimized dtypes during loading
    start = time.time()
    df_optimized = pd.read_csv(
        csv_file,
        dtype={'category': 'category', 'value': 'float32'},
        parse_dates=['date']
    )
    optimized_time = time.time() - start
    optimized_memory = df_optimized.memory_usage(deep=True).sum() / 1024 / 1024
    
    print(f"\n4. Optimized Dtypes:")
    print(f"   Time: {optimized_time:.4f}s")
    print(f"   Memory: {optimized_memory:.2f} MB")
    print(f"   Memory reduction: {(1-optimized_memory/full_memory)*100:.1f}%")
    
    # Cleanup
    import os
    os.unlink(csv_file)

memory_efficient_loading()
```

#### Advanced chunking patterns

```python
class ChunkedProcessor:
    """Klasa do advanced chunked processing"""
    
    def __init__(self, chunk_size=10000):
        self.chunk_size = chunk_size
        self.results = []
        self.metadata = {}
    
    def process_file_aggregation(self, filename, agg_operations):
        """Process file z aggregation operations"""
        
        start_time = time.time()
        chunks_processed = 0
        
        # Initialize accumulators
        accumulators = {}
        
        for chunk in pd.read_csv(filename, chunksize=self.chunk_size):
            chunks_processed += 1
            
            # Apply operations to chunk
            for col, ops in agg_operations.items():
                if col not in accumulators:
                    accumulators[col] = {}
                
                for op in ops:
                    if op == 'sum':
                        accumulators[col][op] = accumulators[col].get(op, 0) + chunk[col].sum()
                    elif op == 'count':
                        accumulators[col][op] = accumulators[col].get(op, 0) + len(chunk)
                    elif op == 'min':
                        current_min = accumulators[col].get(op, float('inf'))
                        accumulators[col][op] = min(current_min, chunk[col].min())
                    elif op == 'max':
                        current_max = accumulators[col].get(op, float('-inf'))
                        accumulators[col][op] = max(current_max, chunk[col].max())
        
        # Calculate means from sum and count
        for col in accumulators:
            if 'sum' in accumulators[col] and 'count' in accumulators[col]:
                accumulators[col]['mean'] = accumulators[col]['sum'] / accumulators[col]['count']
        
        processing_time = time.time() - start_time
        
        self.metadata = {
            'chunks_processed': chunks_processed,
            'processing_time': processing_time,
            'total_records': sum(acc.get('count', 0) for acc in accumulators.values())
        }
        
        return accumulators
    
    def process_file_groupby(self, filename, groupby_col, agg_dict):
        """Chunked processing z groupby operations"""
        
        start_time = time.time()
        group_accumulators = {}
        
        for chunk in pd.read_csv(filename, chunksize=self.chunk_size):
            
            # GroupBy na chunk
            chunk_grouped = chunk.groupby(groupby_col).agg(agg_dict)
            
            # Accumulate results
            for group in chunk_grouped.index:
                if group not in group_accumulators:
                    group_accumulators[group] = {}
                
                for col in chunk_grouped.columns:
                    if col not in group_accumulators[group]:
                        group_accumulators[group][col] = []
                    group_accumulators[group][col].append(chunk_grouped.loc[group, col])
        
        # Final aggregation
        final_results = {}
        for group, data in group_accumulators.items():
            final_results[group] = {}
            for col, values in data.items():
                # Assume mean aggregation for simplicity
                final_results[group][col] = np.mean(values)
        
        processing_time = time.time() - start_time
        self.metadata['processing_time'] = processing_time
        
        return pd.DataFrame.from_dict(final_results, orient='index')
    
    def process_file_window(self, filename, window_size, operation):
        """Chunked processing z window operations"""
        
        previous_chunk_tail = None
        results = []
        
        for chunk in pd.read_csv(filename, chunksize=self.chunk_size):
            
            # Combine with previous chunk tail if exists
            if previous_chunk_tail is not None:
                combined_chunk = pd.concat([previous_chunk_tail, chunk])
            else:
                combined_chunk = chunk
            
            # Apply window operation
            if operation == 'rolling_mean':
                windowed = combined_chunk['value'].rolling(window_size).mean()
            elif operation == 'rolling_sum':
                windowed = combined_chunk['value'].rolling(window_size).sum()
            
            # Store valid results (skip NaN from window start)
            valid_results = windowed.dropna()
            results.append(valid_results)
            
            # Keep tail for next chunk
            if len(combined_chunk) >= window_size:
                previous_chunk_tail = combined_chunk.tail(window_size - 1)
        
        return pd.concat(results)

# Przykład użycia ChunkedProcessor
def demonstrate_chunked_processor():
    """Demonstracja ChunkedProcessor"""
    
    # Create test CSV file
    import tempfile
    import os
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write('id,category,value,date\n')
    
    for i in range(50000):
        category = np.random.choice(['A', 'B', 'C'])
        value = np.random.normal(100, 20)
        date = f"2023-{(i % 12) + 1:02d}-01"
        temp_file.write(f"{i},{category},{value:.2f},{date}\n")
    
    temp_file.close()
    
    processor = ChunkedProcessor(chunk_size=5000)
    
    print("Chunked Processor Demonstration:")
    print("=" * 40)
    
    # Test aggregation
    agg_ops = {
        'value': ['sum', 'count', 'min', 'max']
    }
    
    results = processor.process_file_aggregation(temp_file.name, agg_ops)
    print("1. Aggregation Results:")
    for col, ops in results.items():
        print(f"   {col}: {ops}")
    
    print(f"\nMetadata: {processor.metadata}")
    
    # Test groupby
    groupby_results = processor.process_file_groupby(
        temp_file.name, 
        'category', 
        {'value': 'mean'}
    )
    print(f"\n2. GroupBy Results:")
    print(groupby_results)
    
    # Cleanup
    os.unlink(temp_file.name)

demonstrate_chunked_processor()
```

---

### 🚀 Parallel Processing

#### Multiprocessing with pandas

```python
def parallel_processing_examples():
    """Przykłady parallel processing w Pandas"""
    
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
    import os
    
    # Test data
    np.random.seed(42)
    n = 100000
    
    df = pd.DataFrame({
        'group': np.random.choice(['A', 'B', 'C', 'D'], n),
        'value1': np.random.randn(n),
        'value2': np.random.randn(n),
        'value3': np.random.randn(n)
    })
    
    print("Parallel Processing Examples:")
    print("=" * 40)
    
    # 1. Parallel apply function
    def expensive_function(row):
        """Symulacja expensive operation"""
        return np.sum([row['value1']**2, row['value2']**2, row['value3']**2]) ** 0.5
    
    # Sequential processing
    start = time.time()
    result_sequential = df.head(1000).apply(expensive_function, axis=1)
    sequential_time = time.time() - start
    
    print(f"1. Apply Operation:")
    print(f"   Sequential time (1k rows): {sequential_time:.4f}s")
    
    # Parallel apply using multiprocessing
    def parallel_apply(df_chunk):
        """Function untuk parallel processing"""
        return df_chunk.apply(expensive_function, axis=1)
    
    def split_dataframe(df, num_chunks):
        """Split dataframe na chunks dla parallel processing"""
        chunk_size = len(df) // num_chunks
        chunks = []
        
        for i in range(num_chunks):
            start_idx = i * chunk_size
            if i == num_chunks - 1:
                end_idx = len(df)
            else:
                end_idx = (i + 1) * chunk_size
            chunks.append(df.iloc[start_idx:end_idx])
        
        return chunks
    
    # Parallel processing z ProcessPoolExecutor
    num_processes = min(4, mp.cpu_count())
    chunks = split_dataframe(df.head(1000), num_processes)
    
    start = time.time()
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(parallel_apply, chunks))
    
    result_parallel = pd.concat(results)
    parallel_time = time.time() - start
    
    print(f"   Parallel time ({num_processes} processes): {parallel_time:.4f}s")
    print(f"   Speedup: {sequential_time/parallel_time:.1f}x")
    print(f"   Results equal: {np.allclose(result_sequential, result_parallel)}")
    
    # 2. Parallel GroupBy operations
    print(f"\n2. Parallel GroupBy:")
    
    def group_operation(group_data):
        """Expensive group operation"""
        group_name, data = group_data
        return pd.Series({
            'mean_val1': data['value1'].mean(),
            'std_val1': data['value1'].std(),
            'corr_val1_val2': data['value1'].corr(data['value2']),
            'custom_metric': (data['value1'] * data['value2']).sum()
        })
    
    # Sequential groupby
    start = time.time()
    grouped = df.groupby('group')
    sequential_result = pd.DataFrame([group_operation((name, group)) for name, group in grouped])
    sequential_group_time = time.time() - start
    
    # Parallel groupby
    start = time.time()
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        group_data = [(name, group) for name, group in df.groupby('group')]
        parallel_results = list(executor.map(group_operation, group_data))
    
    parallel_result = pd.DataFrame(parallel_results)
    parallel_group_time = time.time() - start
    
    print(f"   Sequential GroupBy time: {sequential_group_time:.4f}s")
    print(f"   Parallel GroupBy time: {parallel_group_time:.4f}s")
    print(f"   GroupBy speedup: {sequential_group_time/parallel_group_time:.1f}x")

# parallel_processing_examples()  # Uncomment to run (może być intensywne)

# Alternative: Using Dask for parallel processing
def dask_processing_example():
    """Przykład using Dask dla parallel pandas operations"""
    
    try:
        import dask.dataframe as dd
        
        print("3. Dask Parallel Processing:")
        
        # Create test data
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(1000000),
            'y': np.random.randn(1000000),
            'group': np.random.choice(['A', 'B', 'C'], 1000000)
        })
        
        # Convert to Dask DataFrame
        ddf = dd.from_pandas(df, npartitions=4)
        
        # Dask operations (lazy evaluation)
        start = time.time()
        dask_result = ddf.groupby('group').x.mean().compute()
        dask_time = time.time() - start
        
        # Pandas equivalent
        start = time.time()
        pandas_result = df.groupby('group').x.mean()
        pandas_time = time.time() - start
        
        print(f"   Dask time: {dask_time:.4f}s")
        print(f"   Pandas time: {pandas_time:.4f}s")
        print(f"   Results equal: {np.allclose(dask_result.values, pandas_result.values)}")
        
    except ImportError:
        print("3. Dask not available - install with: pip install dask")

dask_processing_example()
```

---

### 🔧 Advanced Optimization Techniques

#### Query optimization

```python
def query_optimization_techniques():
    """Advanced query optimization techniques"""
    
    # Large test dataset
    np.random.seed(42)
    n = 500000
    
    df = pd.DataFrame({
        'id': range(n),
        'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], n),
        'subcategory': np.random.choice(['X', 'Y', 'Z'], n),
        'value': np.random.exponential(10, n),
        'flag': np.random.choice([True, False], n),
        'date': pd.date_range('2020-01-01', periods=n, freq='H')
    })
    
    print("Query Optimization Techniques:")
    print("=" * 40)
    
    # 1. Index optimization
    print("1. Index Optimization:")
    
    # Without index
    start = time.time()
    result_no_index = df[df['category'] == 'A']
    no_index_time = time.time() - start
    
    # With index
    df_indexed = df.set_index('category')
    start = time.time()
    result_indexed = df_indexed.loc['A']
    indexed_time = time.time() - start
    
    print(f"   No index: {no_index_time:.6f}s")
    print(f"   With index: {indexed_time:.6f}s")
    print(f"   Speedup: {no_index_time/indexed_time:.1f}x")
    
    # 2. Query vs Boolean indexing
    print(f"\n2. Query vs Boolean Indexing:")
    
    # Boolean indexing
    start = time.time()
    bool_result = df[(df['value'] > 10) & (df['flag'] == True) & (df['category'].isin(['A', 'B']))]
    bool_time = time.time() - start
    
    # Query method
    start = time.time()
    query_result = df.query("value > 10 & flag == True & category in ['A', 'B']")
    query_time = time.time() - start
    
    # Eval for complex expressions
    start = time.time()
    eval_result = df[df.eval("value > 10 & flag & category in ['A', 'B']")]
    eval_time = time.time() - start
    
    print(f"   Boolean indexing: {bool_time:.6f}s")
    print(f"   Query method: {query_time:.6f}s") 
    print(f"   Eval method: {eval_time:.6f}s")
    
    # 3. Categorical optimization
    print(f"\n3. Categorical Data Optimization:")
    
    # String categories
    df_strings = df.copy()
    
    # Categorical conversion
    df_categorical = df.copy()
    df_categorical['category'] = df_categorical['category'].astype('category')
    df_categorical['subcategory'] = df_categorical['subcategory'].astype('category')
    
    # Memory usage comparison
    strings_memory = df_strings.memory_usage(deep=True).sum() / 1024 / 1024
    categorical_memory = df_categorical.memory_usage(deep=True).sum() / 1024 / 1024
    
    print(f"   String categories memory: {strings_memory:.2f} MB")
    print(f"   Categorical memory: {categorical_memory:.2f} MB")
    print(f"   Memory reduction: {(1-categorical_memory/strings_memory)*100:.1f}%")
    
    # Performance comparison
    start = time.time()
    string_groupby = df_strings.groupby(['category', 'subcategory'])['value'].mean()
    string_groupby_time = time.time() - start
    
    start = time.time()
    categorical_groupby = df_categorical.groupby(['category', 'subcategory'])['value'].mean()
    categorical_groupby_time = time.time() - start
    
    print(f"   String groupby time: {string_groupby_time:.6f}s")
    print(f"   Categorical groupby time: {categorical_groupby_time:.6f}s")
    print(f"   Categorical speedup: {string_groupby_time/categorical_groupby_time:.1f}x")

query_optimization_techniques()
```

#### Memory profiling i monitoring

```python
class PandasProfiler:
    """Profiler dla Pandas operations"""
    
    def __init__(self):
        self.profile_data = []
        
    def profile_operation(self, operation_func, *args, **kwargs):
        """Profile single operation"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Before operation
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        time_before = time.time()
        
        # Execute operation
        result = operation_func(*args, **kwargs)
        
        # After operation
        time_after = time.time()
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        profile_info = {
            'operation': operation_func.__name__,
            'execution_time': time_after - time_before,
            'memory_before': memory_before,
            'memory_after': memory_after,
            'memory_delta': memory_after - memory_before,
            'result_type': type(result).__name__,
            'result_shape': getattr(result, 'shape', None)
        }
        
        self.profile_data.append(profile_info)
        return result
    
    def get_profile_summary(self):
        """Get profiling summary"""
        if not self.profile_data:
            return "No profiling data available"
        
        summary = pd.DataFrame(self.profile_data)
        
        return {
            'total_operations': len(summary),
            'total_time': summary['execution_time'].sum(),
            'total_memory_increase': summary['memory_delta'].sum(),
            'slowest_operation': summary.loc[summary['execution_time'].idxmax()],
            'most_memory_intensive': summary.loc[summary['memory_delta'].idxmax()],
            'detailed_summary': summary
        }

def demonstrate_profiling():
    """Demonstracja profiling"""
    
    profiler = PandasProfiler()
    
    # Test operations
    np.random.seed(42)
    df = pd.DataFrame({
        'A': np.random.randn(100000),
        'B': np.random.randn(100000),
        'C': np.random.choice(['X', 'Y', 'Z'], 100000)
    })
    
    # Profile różne operacje
    def operation_groupby():
        return df.groupby('C').agg({'A': 'mean', 'B': 'std'})
    
    def operation_merge():
        df2 = pd.DataFrame({'C': ['X', 'Y', 'Z'], 'info': [1, 2, 3]})
        return df.merge(df2, on='C')
    
    def operation_pivot():
        return df.groupby('C')['A'].mean().reset_index()
    
    def operation_sort():
        return df.sort_values(['C', 'A'])
    
    # Run profiled operations
    result1 = profiler.profile_operation(operation_groupby)
    result2 = profiler.profile_operation(operation_merge)
    result3 = profiler.profile_operation(operation_pivot)
    result4 = profiler.profile_operation(operation_sort)
    
    # Get summary
    summary = profiler.get_profile_summary()
    
    print("Profiling Results:")
    print("=" * 40)
    print(f"Total operations: {summary['total_operations']}")
    print(f"Total time: {summary['total_time']:.6f}s")
    print(f"Total memory increase: {summary['total_memory_increase']:.2f} MB")
    
    print(f"\nSlowest operation:")
    slow_op = summary['slowest_operation']
    print(f"   {slow_op['operation']}: {slow_op['execution_time']:.6f}s")
    
    print(f"\nMost memory intensive:")
    memory_op = summary['most_memory_intensive']
    print(f"   {memory_op['operation']}: {memory_op['memory_delta']:.2f} MB")
    
    print(f"\nDetailed breakdown:")
    detailed = summary['detailed_summary'][['operation', 'execution_time', 'memory_delta']]
    print(detailed)

demonstrate_profiling()
```

---

### 💡 Performance Best Practices

#### Comprehensive optimization checklist

```python
def pandas_optimization_checklist():
    """Kompleksowy checklist optymalizacji Pandas"""
    
    checklist = """
    ✅ DATA TYPES:
    - Użyj category dla powtarzających się stringów
    - Wybieraj najmniejsze possible numeric types (int8, float32)
    - Określ dtypes podczas read_csv()
    - Konwertuj boolean columns na bool dtype
    
    ✅ MEMORY MANAGEMENT:
    - Używaj chunksize dla dużych plików
    - Ładuj tylko potrzebne kolumny (usecols)
    - Usuń niepotrzebne kolumny wcześnie (.drop())
    - Monitruj memory usage (.memory_usage(deep=True))
    
    ✅ VECTORIZATION:
    - Unikaj .apply() z axis=1 gdy możliwe
    - Używaj vectorized string methods (.str)
    - Preferuj pandas methods nad custom functions
    - Wykorzystuj numpy functions dla matematycznych operacji
    
    ✅ INDEXING:
    - Set appropriate index dla częstych lookups
    - Używaj .loc/.iloc zamiast chained indexing
    - Sortuj dataframe dla range queries
    - Consider MultiIndex dla hierarchical data
    
    ✅ OPERATIONS:
    - Używaj .query() dla complex boolean conditions
    - Cache expensive computations
    - Batch similar operations together
    - Prefer merge over multiple operations
    
    ✅ PARALLEL PROCESSING:
    - Consider dask dla out-of-core computations
    - Użyj multiprocessing dla CPU-intensive tasks
    - Chunk data dla parallel processing
    - Profile before optimizing
    """
    
    print("Pandas Performance Optimization Checklist:")
    print("=" * 60)
    print(checklist)

pandas_optimization_checklist()

# Przykład optimized workflow
class OptimizedDataProcessor:
    """Przykład optimized data processing workflow"""
    
    def __init__(self, chunk_size=50000):
        self.chunk_size = chunk_size
        self.dtype_map = {}
        
    def auto_detect_dtypes(self, sample_df):
        """Auto-detect optimal dtypes z sample"""
        
        optimized_dtypes = {}
        
        for col in sample_df.columns:
            if sample_df[col].dtype == 'object':
                # Check if it should be category
                unique_ratio = sample_df[col].nunique() / len(sample_df)
                if unique_ratio < 0.5:
                    optimized_dtypes[col] = 'category'
            
            elif sample_df[col].dtype in ['int64']:
                # Optimize integer types
                col_min, col_max = sample_df[col].min(), sample_df[col].max()
                if col_min >= 0:  # Unsigned integers
                    if col_max < np.iinfo(np.uint8).max:
                        optimized_dtypes[col] = 'uint8'
                    elif col_max < np.iinfo(np.uint16).max:
                        optimized_dtypes[col] = 'uint16'
                    elif col_max < np.iinfo(np.uint32).max:
                        optimized_dtypes[col] = 'uint32'
                else:  # Signed integers
                    if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                        optimized_dtypes[col] = 'int8'
                    elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                        optimized_dtypes[col] = 'int16'
                    elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                        optimized_dtypes[col] = 'int32'
            
            elif sample_df[col].dtype in ['float64']:
                # Try float32
                optimized_dtypes[col] = 'float32'
        
        return optimized_dtypes
    
    def optimized_file_processing(self, filename, operations):
        """Optimized file processing workflow"""
        
        # 1. Sample file dla dtype detection
        sample_df = pd.read_csv(filename, nrows=1000)
        self.dtype_map = self.auto_detect_dtypes(sample_df)
        
        print(f"Detected optimal dtypes: {self.dtype_map}")
        
        # 2. Process in optimized chunks
        results = []
        memory_usage = []
        
        for chunk in pd.read_csv(filename, chunksize=self.chunk_size, dtype=self.dtype_map):
            
            # Apply operations
            processed_chunk = self.apply_operations(chunk, operations)
            results.append(processed_chunk)
            
            # Monitor memory
            memory_usage.append(chunk.memory_usage(deep=True).sum() / 1024 / 1024)
        
        # 3. Combine results efficiently
        final_result = pd.concat(results, ignore_index=True)
        
        print(f"Average chunk memory: {np.mean(memory_usage):.2f} MB")
        print(f"Final result shape: {final_result.shape}")
        
        return final_result
    
    def apply_operations(self, df, operations):
        """Apply operations efficiently"""
        
        result_df = df.copy()
        
        for operation in operations:
            if operation['type'] == 'filter':
                # Use query dla efficiency
                result_df = result_df.query(operation['condition'])
            
            elif operation['type'] == 'transform':
                # Vectorized transformation
                col = operation['column']
                if operation['function'] == 'normalize':
                    result_df[col] = (result_df[col] - result_df[col].mean()) / result_df[col].std()
            
            elif operation['type'] == 'aggregate':
                # GroupBy aggregation
                result_df = result_df.groupby(operation['group_by']).agg(operation['agg_dict'])
        
        return result_df

# Test optimized processor
def test_optimized_processor():
    """Test OptimizedDataProcessor"""
    
    # Create test file
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write('id,category,value,flag\n')
        for i in range(10000):
            f.write(f'{i},{np.random.choice(["A","B","C"])},{np.random.normal(100,20):.2f},{np.random.choice([True,False])}\n')
        filename = f.name
    
    processor = OptimizedDataProcessor(chunk_size=2000)
    
    operations = [
        {'type': 'filter', 'condition': 'value > 90'},
        {'type': 'transform', 'column': 'value', 'function': 'normalize'}
    ]
    
    result = processor.optimized_file_processing(filename, operations)
    print(f"Processing completed: {result.shape}")
    
    # Cleanup
    import os
    os.unlink(filename)

test_optimized_processor()
```

---

### 🔗 Powiązane tematy

- [[Pandas - Advanced Indexing i MultiIndex]] - Zaawansowane indeksowanie
- [[Pandas - Wprowadzenie do DataFrame]] - Podstawy Pandas
- [[NumPy - Performance Optimization]] - Optymalizacja NumPy
- [[Data Cleaning - Missing Values]] - Czyszczenie danych