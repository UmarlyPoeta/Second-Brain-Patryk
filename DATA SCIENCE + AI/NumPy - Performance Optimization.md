## ⚡ NumPy - Performance Optimization

_Optymalizacja wydajności obliczeń numerycznych w NumPy_

---

### 📝 Wprowadzenie do optymalizacji NumPy

**Wydajność NumPy** zależy od kilku kluczowych czynników:

1. **Vectorization** - wykorzystanie operacji na całych tablicach
2. **Memory layout** - organizacja danych w pamięci  
3. **Data types** - wybór odpowiednich typów danych
4. **Broadcasting** - efektywne operacje na różnych rozmiarach
5. **Compiled libraries** - BLAS, LAPACK, MKL

---

### 🚀 Vectorization - unikanie pętli Python

#### Problem z pętlami Python

```python
import numpy as np
import time

# Porównanie wydajności: pętla Python vs vectorization
def python_sum_of_squares(arr):
    """Suma kwadratów - wersja Python z pętlą"""
    total = 0
    for i in range(len(arr)):
        total += arr[i] ** 2
    return total

def numpy_sum_of_squares(arr):
    """Suma kwadratów - wersja vectorized NumPy"""
    return np.sum(arr ** 2)

# Test wydajności
arr = np.random.rand(1000000)

# Python loop
start_time = time.time()
result_python = python_sum_of_squares(arr)
python_time = time.time() - start_time

# NumPy vectorized
start_time = time.time()
result_numpy = numpy_sum_of_squares(arr)
numpy_time = time.time() - start_time

print(f"Python loop: {python_time:.6f}s")
print(f"NumPy vectorized: {numpy_time:.6f}s")
print(f"Speedup: {python_time/numpy_time:.1f}x")
print(f"Results equal: {np.isclose(result_python, result_numpy)}")
```

#### Zamiana pętli na operacje vectorized

```python
# ❌ Nieefektywne - pętle Python
def distance_matrix_slow(points):
    """Macierz odległości - wersja z pętlami"""
    n = len(points)
    distances = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            distances[i, j] = np.sqrt(np.sum((points[i] - points[j]) ** 2))
    
    return distances

# ✅ Efektywne - broadcasting i vectorization
def distance_matrix_fast(points):
    """Macierz odległości - wersja vectorized"""
    points = np.array(points)
    # Broadcasting: (n, 1, d) - (1, n, d) = (n, n, d)
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    # Sum along last axis and sqrt
    distances = np.sqrt(np.sum(diff ** 2, axis=2))
    return distances

# Test na przykładowych punktach
points = np.random.rand(500, 3)  # 500 punktów w 3D

start_time = time.time()
dist_slow = distance_matrix_slow(points)
slow_time = time.time() - start_time

start_time = time.time()
dist_fast = distance_matrix_fast(points)
fast_time = time.time() - start_time

print(f"Slow version: {slow_time:.4f}s")
print(f"Fast version: {fast_time:.4f}s") 
print(f"Speedup: {slow_time/fast_time:.1f}x")
print(f"Results equal: {np.allclose(dist_slow, dist_fast)}")
```

---

### 🧠 Memory Layout i Cache Efficiency

#### Row-major vs Column-major

```python
# NumPy domyślnie używa row-major (C order)
arr_c = np.random.rand(1000, 1000)  # C order (row-major)
arr_f = np.random.rand(1000, 1000)  # Fortran order (column-major)
arr_f = np.asfortranarray(arr_f)

print(f"C-contiguous: {arr_c.flags.c_contiguous}")
print(f"F-contiguous: {arr_f.flags.f_contiguous}")

# Test wydajności dostępu do elementów
def sum_rows(arr):
    """Sumowanie wierszami (cache-friendly dla C order)"""
    total = 0
    for i in range(arr.shape[0]):
        total += np.sum(arr[i, :])
    return total

def sum_cols(arr):
    """Sumowanie kolumnami (cache-friendly dla F order)"""
    total = 0
    for j in range(arr.shape[1]):
        total += np.sum(arr[:, j])
    return total

# Test dla C order
start_time = time.time()
sum_c_rows = sum_rows(arr_c)
c_rows_time = time.time() - start_time

start_time = time.time()
sum_c_cols = sum_cols(arr_c)
c_cols_time = time.time() - start_time

print(f"\nC order array:")
print(f"Summing by rows: {c_rows_time:.4f}s")
print(f"Summing by cols: {c_cols_time:.4f}s")
print(f"Row/Col ratio: {c_cols_time/c_rows_time:.2f}")

# Test dla F order  
start_time = time.time()
sum_f_rows = sum_rows(arr_f)
f_rows_time = time.time() - start_time

start_time = time.time()
sum_f_cols = sum_cols(arr_f)
f_cols_time = time.time() - start_time

print(f"\nF order array:")
print(f"Summing by rows: {f_rows_time:.4f}s")
print(f"Summing by cols: {f_cols_time:.4f}s")
print(f"Row/Col ratio: {f_rows_time/f_cols_time:.2f}")
```

#### Memory views vs copies

```python
# Views vs copies - wpływ na wydajność
large_array = np.random.rand(10000, 10000)

# View (no copying) - szybkie
start_time = time.time()
subarray_view = large_array[100:200, 100:200]  # View
view_time = time.time() - start_time

# Copy - wolniejsze
start_time = time.time()
subarray_copy = large_array[100:200, 100:200].copy()  # Explicit copy
copy_time = time.time() - start_time

print(f"View creation: {view_time:.6f}s")
print(f"Copy creation: {copy_time:.6f}s")

# Sprawdzenie czy to view czy copy
print(f"Is view: {np.shares_memory(large_array, subarray_view)}")
print(f"Is copy: {np.shares_memory(large_array, subarray_copy)}")

# Uwaga: niektóre operacje mogą zmuszać do kopii
non_contiguous = large_array[::2, ::2]  # Co drugi element
print(f"Non-contiguous is contiguous: {non_contiguous.flags.c_contiguous}")
```

---

### 🔢 Optymalizacja typów danych

#### Wybór właściwego dtype

```python
# Porównanie różnych typów danych
sizes = [100, 1000, 10000]
dtypes = [np.int8, np.int32, np.int64, np.float32, np.float64]

for size in sizes:
    print(f"\nArray size: {size} x {size}")
    print("=" * 40)
    
    for dtype in dtypes:
        # Tworzenie tablicy
        arr = np.random.randint(0, 100, size=(size, size)).astype(dtype)
        
        # Pamięć
        memory_mb = arr.nbytes / (1024 * 1024)
        
        # Test operacji matematycznej
        start_time = time.time()
        result = np.sum(arr ** 2)
        operation_time = time.time() - start_time
        
        print(f"{dtype.__name__:>8}: {memory_mb:6.2f} MB, {operation_time:.6f}s")

# Przykład: kiedy użyć mniejszego typu
def process_image_data():
    """Przetwarzanie danych obrazu - uint8 vs float64"""
    
    # Symulacja danych obrazu (0-255)
    image_uint8 = np.random.randint(0, 256, size=(1000, 1000, 3), dtype=np.uint8)
    image_float64 = image_uint8.astype(np.float64) / 255.0
    
    print(f"uint8 size: {image_uint8.nbytes / 1024 / 1024:.2f} MB")
    print(f"float64 size: {image_float64.nbytes / 1024 / 1024:.2f} MB")
    print(f"Memory ratio: {image_float64.nbytes / image_uint8.nbytes:.1f}x")
    
    # Operacja na każdym typie
    start_time = time.time()
    mean_uint8 = np.mean(image_uint8, axis=2)
    uint8_time = time.time() - start_time
    
    start_time = time.time()
    mean_float64 = np.mean(image_float64, axis=2)
    float64_time = time.time() - start_time
    
    print(f"uint8 operation: {uint8_time:.6f}s")
    print(f"float64 operation: {float64_time:.6f}s")

process_image_data()
```

---

### 📡 Broadcasting i Memory-Efficient Operations

#### Zrozumienie broadcasting rules

```python
# Broadcasting rules i wydajność
def demonstrate_broadcasting():
    """Demonstracja efektywnego broadcasting"""
    
    # Duże tablice
    large_matrix = np.random.rand(1000, 2000)
    row_vector = np.random.rand(1, 2000)
    col_vector = np.random.rand(1000, 1)
    scalar = 5.0
    
    print("Memory usage:")
    print(f"Large matrix: {large_matrix.nbytes / 1024 / 1024:.2f} MB")
    print(f"Row vector: {row_vector.nbytes / 1024:.2f} KB")
    print(f"Col vector: {col_vector.nbytes / 1024:.2f} KB")
    
    # ✅ Efektywne broadcasting - nie tworzy kopii
    start_time = time.time()
    result1 = large_matrix + row_vector  # Broadcasting
    broadcast_time = time.time() - start_time
    
    # ❌ Nieefektywne - explicit tiling tworzy kopie
    start_time = time.time()
    row_tiled = np.tile(row_vector, (1000, 1))  # Tworzy dużą kopię!
    result2 = large_matrix + row_tiled
    tiling_time = time.time() - start_time
    
    print(f"\nBroadcasting time: {broadcast_time:.6f}s")
    print(f"Tiling time: {tiling_time:.6f}s")
    print(f"Results equal: {np.allclose(result1, result2)}")
    
    # Complex broadcasting example
    start_time = time.time()
    # (1000, 2000) + (1, 2000) + (1000, 1) + scalar
    complex_result = large_matrix + row_vector + col_vector + scalar
    complex_time = time.time() - start_time
    
    print(f"Complex broadcasting: {complex_time:.6f}s")

demonstrate_broadcasting()
```

#### Operacje in-place dla oszczędności pamięci

```python
# In-place operations - modyfikacja bez kopii
def compare_inplace_operations():
    """Porównanie operacji in-place vs tworzenie nowych tablic"""
    
    # Duża tablica
    size = 5000
    arr = np.random.rand(size, size)
    original_id = id(arr)
    
    print(f"Original array memory: {arr.nbytes / 1024 / 1024:.2f} MB")
    
    # ❌ Nieefektywne - tworzy nową tablicę
    start_time = time.time()
    arr_new = arr * 2 + 1
    new_array_time = time.time() - start_time
    
    # ✅ Efektywne - in-place modification
    start_time = time.time()
    arr *= 2
    arr += 1
    inplace_time = time.time() - start_time
    
    print(f"\nNew array creation: {new_array_time:.6f}s")
    print(f"In-place operations: {inplace_time:.6f}s")
    print(f"Speedup: {new_array_time/inplace_time:.1f}x")
    print(f"Same memory location: {id(arr) == original_id}")
    
    # Universal functions z out parameter
    arr1 = np.random.rand(1000, 1000)
    arr2 = np.random.rand(1000, 1000)
    result = np.empty_like(arr1)  # Pre-allocate
    
    start_time = time.time()
    np.add(arr1, arr2, out=result)  # In-place w result
    out_param_time = time.time() - start_time
    
    start_time = time.time()
    normal_result = arr1 + arr2  # Tworzy nową tablicę
    normal_time = time.time() - start_time
    
    print(f"\nWith out parameter: {out_param_time:.6f}s")
    print(f"Normal addition: {normal_time:.6f}s")

compare_inplace_operations()
```

---

### 🔧 Compiled Libraries Integration

#### Wykorzystanie MKL i BLAS

```python
# Sprawdzanie konfiguracji bibliotek
def check_numpy_config():
    """Sprawdzenie konfiguracji NumPy i dostępnych bibliotek"""
    
    print("NumPy configuration:")
    print("=" * 50)
    
    # Podstawowe informacje
    print(f"NumPy version: {np.__version__}")
    
    # Sprawdzenie BLAS/LAPACK
    try:
        config = np.__config__.show()
        print("\nBLAS/LAPACK configuration available")
    except:
        print("\nBLAS/LAPACK configuration not available")
    
    # Test wydajności dużych operacji macierzowych
    sizes = [500, 1000, 2000]
    
    for size in sizes:
        print(f"\nMatrix multiplication {size}x{size}:")
        A = np.random.rand(size, size)
        B = np.random.rand(size, size)
        
        start_time = time.time()
        C = A @ B
        elapsed = time.time() - start_time
        
        # FLOPS estimation (2*n^3 operations)
        flops = 2 * size**3
        gflops = flops / elapsed / 1e9
        
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Performance: {gflops:.2f} GFLOPS")

check_numpy_config()

# Wykorzystanie numexpr dla złożonych wyrażeń
try:
    import numexpr as ne
    
    def compare_numexpr():
        """Porównanie NumPy vs numexpr"""
        size = 1000000
        a = np.random.rand(size)
        b = np.random.rand(size)
        c = np.random.rand(size)
        
        # NumPy
        start_time = time.time()
        result_numpy = 2*a + 3*b + 4*c
        numpy_time = time.time() - start_time
        
        # numexpr
        start_time = time.time()
        result_numexpr = ne.evaluate("2*a + 3*b + 4*c")
        numexpr_time = time.time() - start_time
        
        print(f"\nNumExpr comparison:")
        print(f"NumPy: {numpy_time:.6f}s")
        print(f"NumExpr: {numexpr_time:.6f}s")
        print(f"Speedup: {numpy_time/numexpr_time:.1f}x")
        print(f"Results equal: {np.allclose(result_numpy, result_numexpr)}")
    
    compare_numexpr()
    
except ImportError:
    print("NumExpr not available - install with: pip install numexpr")
```

---

### ⚡ Specific Optimization Techniques

#### Optimizing array creation

```python
def optimize_array_creation():
    """Optymalizacja tworzenia tablic"""
    
    size = 1000000
    
    # Pre-allocation vs dynamic growth
    print("Array creation comparison:")
    
    # ❌ Bardzo wolne - dynamiczne rozszerzanie
    start_time = time.time()
    slow_array = np.array([])
    for i in range(1000):  # Mniejszy rozmiar dla demonstracji
        slow_array = np.append(slow_array, i)
    slow_time = time.time() - start_time
    
    # ✅ Szybkie - pre-allocation
    start_time = time.time()
    fast_array = np.zeros(1000)
    for i in range(1000):
        fast_array[i] = i
    fast_time = time.time() - start_time
    
    # ✅ Najszybsze - vectorized
    start_time = time.time()
    fastest_array = np.arange(1000)
    fastest_time = time.time() - start_time
    
    print(f"Dynamic append: {slow_time:.6f}s")
    print(f"Pre-allocated: {fast_time:.6f}s")
    print(f"Vectorized: {fastest_time:.6f}s")
    
    # Specialized creation functions
    print(f"\nSpecialized creation functions:")
    
    # zeros vs empty
    start_time = time.time()
    zeros_array = np.zeros((size,))
    zeros_time = time.time() - start_time
    
    start_time = time.time()
    empty_array = np.empty((size,))
    empty_array.fill(0)  # Manual fill
    empty_time = time.time() - start_time
    
    print(f"np.zeros: {zeros_time:.6f}s")
    print(f"np.empty + fill: {empty_time:.6f}s")

optimize_array_creation()
```

#### Memory pool and object reuse

```python
class ArrayPool:
    """Prosty pool tablic do wielokrotnego użytku"""
    
    def __init__(self):
        self.pool = {}
    
    def get_array(self, shape, dtype=np.float64):
        """Pobierz tablicę z pool lub utwórz nową"""
        key = (shape, dtype)
        if key in self.pool and len(self.pool[key]) > 0:
            return self.pool[key].pop()
        else:
            return np.empty(shape, dtype=dtype)
    
    def return_array(self, arr):
        """Zwróć tablicę do pool"""
        key = (arr.shape, arr.dtype)
        if key not in self.pool:
            self.pool[key] = []
        self.pool[key].append(arr)
    
    def clear(self):
        """Wyczyść pool"""
        self.pool.clear()

def test_array_pool():
    """Test wydajności array pool"""
    pool = ArrayPool()
    shape = (1000, 1000)
    n_iterations = 100
    
    # Bez pool - każda iteracja tworzy nową tablicę
    start_time = time.time()
    for _ in range(n_iterations):
        arr = np.empty(shape)
        # Symulacja obróbki
        arr.fill(1.0)
        result = np.sum(arr)
    no_pool_time = time.time() - start_time
    
    # Z pool - reuse tablic
    start_time = time.time()
    for _ in range(n_iterations):
        arr = pool.get_array(shape)
        # Symulacja obróbki
        arr.fill(1.0)
        result = np.sum(arr)
        pool.return_array(arr)
    with_pool_time = time.time() - start_time
    
    print(f"Without pool: {no_pool_time:.6f}s")
    print(f"With pool: {with_pool_time:.6f}s")
    print(f"Improvement: {no_pool_time/with_pool_time:.1f}x")

test_array_pool()
```

---

### 🔍 Profiling i Diagnostyka

#### Memory profiling

```python
import psutil
import os

def memory_usage():
    """Sprawdzenie użycia pamięci przez proces"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def profile_memory_usage():
    """Profilowanie użycia pamięci"""
    
    print("Memory profiling:")
    print(f"Initial memory: {memory_usage():.2f} MB")
    
    # Tworzenie dużej tablicy
    large_array = np.random.rand(10000, 1000)
    print(f"After large array creation: {memory_usage():.2f} MB")
    
    # Operacja tworząca kopię
    copied_array = large_array * 2
    print(f"After copy creation: {memory_usage():.2f} MB")
    
    # Usunięcie kopii
    del copied_array
    print(f"After copy deletion: {memory_usage():.2f} MB")
    
    # In-place operation
    large_array *= 3
    print(f"After in-place operation: {memory_usage():.2f} MB")
    
    # Final cleanup
    del large_array
    print(f"After cleanup: {memory_usage():.2f} MB")

profile_memory_usage()

# Timing utilities
def time_function(func, *args, n_runs=5, **kwargs):
    """Zmierz czas wykonania funkcji z wieloma uruchomieniami"""
    times = []
    
    for _ in range(n_runs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    times = np.array(times)
    print(f"Function: {func.__name__}")
    print(f"Mean time: {np.mean(times):.6f}s ± {np.std(times):.6f}s")
    print(f"Min time: {np.min(times):.6f}s")
    print(f"Max time: {np.max(times):.6f}s")
    
    return result, times

# Przykład użycia
def test_function(size):
    arr = np.random.rand(size, size)
    return np.linalg.eigvals(arr)

result, times = time_function(test_function, 500, n_runs=3)
```

---

### 📊 Konkretne przypadki optymalizacji

#### Optymalizacja operacji na dużych danych

```python
def optimize_large_data_processing():
    """Optymalizacja przetwarzania dużych zbiorów danych"""
    
    # Symulacja dużego datasetu
    n_samples = 1000000
    n_features = 100
    
    # ❌ Nieefektywne podejście
    def slow_processing(data):
        result = []
        for i in range(data.shape[0]):
            row_sum = np.sum(data[i, :])
            row_mean = np.mean(data[i, :])
            row_std = np.std(data[i, :])
            result.append([row_sum, row_mean, row_std])
        return np.array(result)
    
    # ✅ Efektywne podejście vectorized
    def fast_processing(data):
        row_sums = np.sum(data, axis=1)
        row_means = np.mean(data, axis=1) 
        row_stds = np.std(data, axis=1)
        return np.column_stack([row_sums, row_means, row_stds])
    
    # ✅ Jeszcze bardziej efektywne - chunk processing
    def chunked_processing(data, chunk_size=10000):
        n_samples = data.shape[0]
        results = []
        
        for start_idx in range(0, n_samples, chunk_size):
            end_idx = min(start_idx + chunk_size, n_samples)
            chunk = data[start_idx:end_idx]
            
            chunk_result = fast_processing(chunk)
            results.append(chunk_result)
        
        return np.vstack(results)
    
    # Generowanie danych testowych (mniejszych dla demonstracji)
    test_data = np.random.rand(10000, n_features)
    
    # Porównanie czasów
    print("Large data processing comparison:")
    
    start_time = time.time()
    result_slow = slow_processing(test_data[:1000])  # Mniejszy sample
    slow_time = time.time() - start_time
    
    start_time = time.time()
    result_fast = fast_processing(test_data)
    fast_time = time.time() - start_time
    
    start_time = time.time()
    result_chunked = chunked_processing(test_data, chunk_size=2000)
    chunked_time = time.time() - start_time
    
    print(f"Slow (loop): {slow_time:.6f}s")
    print(f"Fast (vectorized): {fast_time:.6f}s")
    print(f"Chunked: {chunked_time:.6f}s")

optimize_large_data_processing()
```

---

### 💡 Best Practices Summary

#### Checklist optymalizacji NumPy

```python
def numpy_optimization_checklist():
    """
    Lista kontrolna do optymalizacji kodu NumPy:
    """
    
    checklist = """
    ✅ VECTORIZATION:
    - Zastąp pętle Python operacjami na tablicach
    - Użyj broadcasting zamiast jawnego kopiowania
    - Wykorzystaj universal functions (ufuncs)
    
    ✅ MEMORY MANAGEMENT:
    - Pre-alokuj tablice gdy znasz rozmiar
    - Używaj in-place operations gdzie możliwe
    - Wybieraj odpowiedni dtype (nie zawsze float64)
    - Unikaj niepotrzebnych kopii (sprawdzaj views vs copies)
    
    ✅ CACHE EFFICIENCY:
    - Respektuj memory layout (C vs Fortran order)
    - Przetwarzaj dane w sposób sekwencyjny
    - Używaj contiguous arrays
    
    ✅ ALGORITHM SELECTION:
    - Wybierz specialized functions dla konkretnych zadań
    - Wykorzystuj optimized linear algebra (BLAS/LAPACK)
    - Rozważ chunk processing dla bardzo dużych danych
    
    ✅ PROFILING:
    - Mierz wydajność przed optymalizacją
    - Identyfikuj bottlenecks
    - Sprawdzaj użycie pamięci
    """
    
    print(checklist)

numpy_optimization_checklist()
```

#### Przykład kompleksowej optymalizacji

```python
class OptimizedDataProcessor:
    """Przykład klasy z zoptymalizowanym przetwarzaniem danych"""
    
    def __init__(self, chunk_size=50000):
        self.chunk_size = chunk_size
        self.array_pool = {}
    
    def _get_temp_array(self, shape, dtype):
        """Pobierz tablicę tymczasową z pool"""
        key = (shape, dtype)
        if key in self.array_pool:
            return self.array_pool[key]
        else:
            arr = np.empty(shape, dtype=dtype)
            self.array_pool[key] = arr
            return arr
    
    def normalize_features(self, data):
        """Znormalizuj cechy - zoptymalizowana wersja"""
        # Pre-compute statistics
        means = np.mean(data, axis=0, keepdims=True)
        stds = np.std(data, axis=0, keepdims=True)
        
        # Avoid division by zero
        stds[stds == 0] = 1
        
        # In-place normalization
        data -= means
        data /= stds
        
        return data
    
    def compute_distances_chunked(self, points1, points2):
        """Oblicz macierz odległości w chunks"""
        n1, n2 = len(points1), len(points2)
        distances = np.empty((n1, n2), dtype=np.float32)  # Use float32 for memory
        
        # Process in chunks to manage memory
        for i in range(0, n1, self.chunk_size):
            end_i = min(i + self.chunk_size, n1)
            chunk1 = points1[i:end_i]
            
            for j in range(0, n2, self.chunk_size):
                end_j = min(j + self.chunk_size, n2)
                chunk2 = points2[j:end_j]
                
                # Compute distances for this chunk
                diff = chunk1[:, np.newaxis, :] - chunk2[np.newaxis, :, :]
                chunk_distances = np.sqrt(np.sum(diff**2, axis=2))
                
                distances[i:end_i, j:end_j] = chunk_distances
        
        return distances
    
    def process_dataset(self, data):
        """Kompleksowe przetwarzanie datasetu"""
        print(f"Processing dataset shape: {data.shape}")
        print(f"Memory usage: {data.nbytes / 1024 / 1024:.2f} MB")
        
        start_time = time.time()
        
        # 1. Normalizacja
        normalized_data = self.normalize_features(data.copy())
        
        # 2. Compute some statistics efficiently
        feature_stats = {
            'means': np.mean(normalized_data, axis=0),
            'stds': np.std(normalized_data, axis=0),
            'correlations': np.corrcoef(normalized_data.T)
        }
        
        total_time = time.time() - start_time
        print(f"Processing completed in {total_time:.4f}s")
        
        return normalized_data, feature_stats

# Test zoptymalizowanego processora
processor = OptimizedDataProcessor(chunk_size=10000)
test_data = np.random.rand(50000, 20)

processed_data, stats = processor.process_dataset(test_data)
print(f"Processed data shape: {processed_data.shape}")
print(f"Feature means range: [{np.min(stats['means']):.6f}, {np.max(stats['means']):.6f}]")
```

---

### 🔗 Powiązane tematy

- [[NumPy - Podstawy]] - Podstawowe operacje NumPy
- [[NumPy - Memory Management i Broadcasting]] - Zarządzanie pamięcią
- [[Machine Learning Pipeline - Preprocessing]] - Zastosowanie w ML
- [[Pandas - Performance Optimization]] - Optymalizacja Pandas