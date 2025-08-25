## 🧮 NumPy - Memory Management i Broadcasting

_Zaawansowane zarządzanie pamięcią i mechanizmy broadcasting w NumPy_

---

### 📝 Wprowadzenie do memory management

**Memory management w NumPy** obejmuje:

1. **Views vs Copies** - różnica między referencjami a kopiami danych
2. **Memory layout** - organizacja danych w pamięci (C vs Fortran order)
3. **Broadcasting** - efektywne operacje na tablicach różnych rozmiarów
4. **Memory mapping** - praca z danymi większymi niż RAM
5. **Garbage collection** - zarządzanie cyklem życia obiektów

---

### 🔍 Views vs Copies - Fundamenty

#### Czym są views i copies

```python
import numpy as np

# Oryginalna tablica
original = np.arange(12).reshape(3, 4)
print("Original array:")
print(original)
print(f"Original id: {id(original)}")
print(f"Data pointer: {original.data}")

# View - ta sama pamięć, inna "perspektywa"
view = original[1:, 1:]  # Slice tworzy view
print(f"\nView id: {id(view)}")
print(f"View data pointer: {view.data}")
print(f"Shares memory: {np.shares_memory(original, view)}")

# Copy - nowa pamięć, niezależne dane
copy = original.copy()
print(f"\nCopy id: {id(copy)}")  
print(f"Copy data pointer: {copy.data}")
print(f"Shares memory: {np.shares_memory(original, copy)}")

# Modyfikacja view wpływa na oryginał
view[0, 0] = 999
print("\nAfter modifying view:")
print("Original array:")
print(original)  # Zmieniony!

# Modyfikacja copy nie wpływa na oryginał
copy[0, 0] = 777
print("\nAfter modifying copy:")
print("Original array:")
print(original)  # Bez zmian
```

#### Kiedy powstają views vs copies

```python
def check_view_or_copy(operation_name, result, original):
    """Helper do sprawdzania czy operacja tworzy view czy copy"""
    is_view = np.shares_memory(original, result)
    print(f"{operation_name:30}: {'VIEW' if is_view else 'COPY'}")
    return is_view

# Test różnych operacji
arr = np.arange(24).reshape(4, 6)

print("View vs Copy operations:")
print("=" * 50)

# Slicing - zawsze view (jeśli możliwy)
slice_result = arr[1:3, 2:5]
check_view_or_copy("Basic slicing", slice_result, arr)

# Reshaping - view gdy możliwy
reshape_result = arr.reshape(6, 4)
check_view_or_copy("Reshape (compatible)", reshape_result, arr)

# Transpose - zawsze view
transpose_result = arr.T
check_view_or_copy("Transpose", transpose_result, arr)

# Fancy indexing - zawsze copy
fancy_result = arr[[0, 2], :]
check_view_or_copy("Fancy indexing", fancy_result, arr)

# Boolean indexing - zawsze copy
bool_result = arr[arr > 10]
check_view_or_copy("Boolean indexing", bool_result, arr)

# Mathematical operations - zawsze copy
math_result = arr + 1
check_view_or_copy("Mathematical operation", math_result, arr)

# Flatten vs ravel
flatten_result = arr.flatten()  # Zawsze copy
ravel_result = arr.ravel()      # View gdy możliwy
check_view_or_copy("Flatten", flatten_result, arr)
check_view_or_copy("Ravel", ravel_result, arr)
```

#### Memory layout i contiguity

```python
# Różne layout patterns
def analyze_memory_layout(arr, name):
    """Analizuj layout pamięci tablicy"""
    print(f"\n{name}:")
    print(f"  Shape: {arr.shape}")
    print(f"  Strides: {arr.strides}")
    print(f"  C-contiguous: {arr.flags.c_contiguous}")
    print(f"  F-contiguous: {arr.flags.f_contiguous}")
    print(f"  Memory usage: {arr.nbytes} bytes")

# Oryginalna tablica (C-contiguous)
arr = np.arange(12).reshape(3, 4)
analyze_memory_layout(arr, "Original C-order")

# Transpose (nie-contiguous)
arr_t = arr.T
analyze_memory_layout(arr_t, "Transposed")

# Fortran order
arr_f = np.asfortranarray(arr)
analyze_memory_layout(arr_f, "Fortran order")

# Slice (może być nie-contiguous)
arr_slice = arr[:, ::2]  # Co drugi element w kolumnach
analyze_memory_layout(arr_slice, "Strided slice")

# Demonstracja wpływu na wydajność
def performance_test_layout():
    """Test wydajności różnych layout"""
    size = 2000
    
    # C-order array
    arr_c = np.random.rand(size, size)
    
    # F-order array  
    arr_f = np.asfortranarray(arr_c)
    
    import time
    
    # Row-wise access (lepszy dla C-order)
    start = time.time()
    sum_c_rows = np.sum(np.sum(arr_c, axis=1))
    c_row_time = time.time() - start
    
    start = time.time()
    sum_f_rows = np.sum(np.sum(arr_f, axis=1))
    f_row_time = time.time() - start
    
    # Column-wise access (lepszy dla F-order)
    start = time.time()
    sum_c_cols = np.sum(np.sum(arr_c, axis=0))
    c_col_time = time.time() - start
    
    start = time.time()
    sum_f_cols = np.sum(np.sum(arr_f, axis=0))
    f_col_time = time.time() - start
    
    print(f"\nPerformance comparison ({size}x{size}):")
    print(f"C-order row access: {c_row_time:.6f}s")
    print(f"F-order row access: {f_row_time:.6f}s")
    print(f"C-order col access: {c_col_time:.6f}s")
    print(f"F-order col access: {f_col_time:.6f}s")
    
    print(f"\nRatio C/F for rows: {c_row_time/f_row_time:.2f}")
    print(f"Ratio C/F for cols: {c_col_time/f_col_time:.2f}")

performance_test_layout()
```

---

### 📡 Broadcasting - Zaawansowane techniki

#### Broadcasting rules i mechanizm

```python
def explain_broadcasting(a, b, operation_name="operation"):
    """Wyjaśnia jak działa broadcasting dla dwóch tablic"""
    print(f"\n{operation_name}:")
    print(f"Array A shape: {a.shape}")
    print(f"Array B shape: {b.shape}")
    
    # Sprawdzenie kompatybilności broadcasting
    try:
        # Dummy operation to check compatibility
        result_shape = np.broadcast(a, b).shape
        print(f"Broadcast result shape: {result_shape}")
        print("✅ Broadcasting compatible")
        
        # Pokazanie pamięci
        a_size = a.nbytes
        b_size = b.nbytes
        print(f"Memory A: {a_size} bytes")
        print(f"Memory B: {b_size} bytes")
        print(f"No additional memory needed for broadcasting")
        
    except ValueError as e:
        print(f"❌ Broadcasting error: {e}")

# Przykłady broadcasting
print("Broadcasting Examples:")
print("=" * 50)

# 1. Scalar with array
scalar = 5
array_1d = np.array([1, 2, 3, 4])
explain_broadcasting(scalar, array_1d, "Scalar + 1D Array")

# 2. 1D with 2D
array_2d = np.random.rand(3, 4)
array_1d_compatible = np.random.rand(4)
explain_broadcasting(array_2d, array_1d_compatible, "2D + 1D Array")

# 3. Compatible shapes
array_a = np.random.rand(5, 1)
array_b = np.random.rand(1, 4)  
explain_broadcasting(array_a, array_b, "Broadcasting to (5,4)")

# 4. Incompatible shapes
array_incompatible = np.random.rand(3)
explain_broadcasting(array_2d, array_incompatible, "Incompatible shapes")
```

#### Memory-efficient broadcasting tricks

```python
def demonstrate_memory_efficient_operations():
    """Demonstracja memory-efficient operations z broadcasting"""
    
    # Duże tablice do demonstracji
    large_matrix = np.random.rand(1000, 2000)
    row_vector = np.random.rand(1, 2000)
    col_vector = np.random.rand(1000, 1)
    
    print(f"Large matrix: {large_matrix.shape} ({large_matrix.nbytes/1024/1024:.2f} MB)")
    print(f"Row vector: {row_vector.shape} ({row_vector.nbytes/1024:.2f} KB)")
    print(f"Col vector: {col_vector.shape} ({col_vector.nbytes/1024:.2f} KB)")
    
    import time
    
    # ✅ Efficient: Broadcasting (no memory expansion)
    start = time.time()
    result_broadcast = large_matrix + row_vector + col_vector
    broadcast_time = time.time() - start
    
    # ❌ Inefficient: Manual tiling (creates large copies)
    start = time.time()
    row_tiled = np.tile(row_vector, (1000, 1))  # Creates 16MB copy!
    col_tiled = np.tile(col_vector, (1, 2000))  # Creates 16MB copy!
    result_tiled = large_matrix + row_tiled + col_tiled
    tiling_time = time.time() - start
    
    print(f"\nBroadcasting time: {broadcast_time:.6f}s")
    print(f"Tiling time: {tiling_time:.6f}s")
    print(f"Memory efficiency ratio: {tiling_time/broadcast_time:.1f}x")
    print(f"Results are equal: {np.allclose(result_broadcast, result_tiled)}")
    
    # Advanced broadcasting example - outer operations
    def efficient_pairwise_operations(arr1, arr2):
        """Efektywne operacje parami używając broadcasting"""
        
        # arr1: (N, features), arr2: (M, features)
        # Result: (N, M) pairwise operations
        
        # Expand dimensions for broadcasting
        arr1_expanded = arr1[:, np.newaxis, :]  # (N, 1, features)
        arr2_expanded = arr2[np.newaxis, :, :]  # (1, M, features)
        
        # Pairwise differences
        differences = arr1_expanded - arr2_expanded  # (N, M, features)
        
        # Pairwise distances
        distances = np.sqrt(np.sum(differences**2, axis=2))  # (N, M)
        
        return distances
    
    # Test efficient pairwise operations
    points1 = np.random.rand(500, 3)
    points2 = np.random.rand(300, 3)
    
    start = time.time()
    distances = efficient_pairwise_operations(points1, points2)
    pairwise_time = time.time() - start
    
    print(f"\nPairwise distances: {distances.shape}")
    print(f"Computation time: {pairwise_time:.6f}s")

demonstrate_memory_efficient_operations()
```

#### Advanced broadcasting patterns

```python
def advanced_broadcasting_patterns():
    """Zaawansowane wzorce broadcasting"""
    
    print("Advanced Broadcasting Patterns:")
    print("=" * 40)
    
    # 1. Multi-dimensional broadcasting
    A = np.random.rand(2, 3, 1, 5)  # (2, 3, 1, 5)
    B = np.random.rand(1, 4, 1)     # (1, 4, 1)
    C = np.random.rand(2, 1, 4, 1)  # (2, 1, 4, 1)
    
    result = A + B + C  # Broadcasts to (2, 3, 4, 5)
    print(f"Multi-dim broadcasting result: {result.shape}")
    
    # 2. Broadcasting with newaxis for specific patterns
    data = np.random.rand(100, 50)  # 100 samples, 50 features
    
    # Center each feature (subtract mean)
    feature_means = np.mean(data, axis=0, keepdims=True)  # (1, 50)
    centered_data = data - feature_means
    print(f"Centered data shape: {centered_data.shape}")
    
    # Normalize each sample (divide by sample norm)
    sample_norms = np.linalg.norm(data, axis=1, keepdims=True)  # (100, 1)
    normalized_data = data / sample_norms
    print(f"Normalized data shape: {normalized_data.shape}")
    
    # 3. Broadcasting for complex transformations
    def apply_per_class_transformation(data, class_labels, transformations):
        """Apply different transformations per class using broadcasting"""
        
        unique_classes = np.unique(class_labels)
        result = np.zeros_like(data)
        
        for i, cls in enumerate(unique_classes):
            mask = class_labels == cls
            # Use broadcasting to apply transformation
            result[mask] = data[mask] * transformations[i][:, np.newaxis]
        
        return result
    
    # Example usage
    sample_data = np.random.rand(20, 10)
    labels = np.random.choice([0, 1, 2], size=20)
    transforms = np.random.rand(3, 10)  # Different transform for each class
    
    transformed = apply_per_class_transformation(sample_data, labels, transforms)
    print(f"Per-class transformation result: {transformed.shape}")

advanced_broadcasting_patterns()
```

---

### 💾 Memory Mapping i Duże Dane

#### Memory mapping basics

```python
def demonstrate_memory_mapping():
    """Demonstracja memory mapping dla dużych plików"""
    
    # Tworzenie dużego pliku danych
    filename = '/tmp/large_data.dat'
    shape = (10000, 1000)
    
    # Tworzenie memory-mapped array
    print(f"Creating memory-mapped array: {shape}")
    mmap_array = np.memmap(filename, dtype='float32', mode='w+', shape=shape)
    
    # Wypełnianie danych w chunks (nie ładuje wszystkich do RAM)
    chunk_size = 1000
    for i in range(0, shape[0], chunk_size):
        end_i = min(i + chunk_size, shape[0])
        mmap_array[i:end_i] = np.random.rand(end_i - i, shape[1]).astype('float32')
    
    print(f"File size: {mmap_array.nbytes / 1024 / 1024:.2f} MB")
    print(f"Memory map created successfully")
    
    # Praca z memory-mapped data
    # Operacje działają bezpośrednio na pliku
    import time
    
    start = time.time()
    # Obliczenie statystyk bez ładowania do RAM
    column_means = np.mean(mmap_array, axis=0)
    stats_time = time.time() - start
    
    print(f"Statistics computation time: {stats_time:.4f}s")
    print(f"Means shape: {column_means.shape}")
    
    # Dostęp do części danych
    subset = mmap_array[:100, :50]  # Tylko ta część zostanie załadowana
    print(f"Subset shape: {subset.shape}")
    
    # Cleanup
    del mmap_array  # Zamyka plik
    import os
    os.remove(filename)
    
    print("Memory mapping demonstration completed")

# demonstrate_memory_mapping()  # Uncomment to run

def chunked_processing_example():
    """Przykład przetwarzania dużych danych w chunks"""
    
    def process_large_dataset_chunked(data_source, chunk_size=1000):
        """Process data in chunks to manage memory"""
        
        total_samples = data_source.shape[0]
        results = []
        
        print(f"Processing {total_samples} samples in chunks of {chunk_size}")
        
        for start_idx in range(0, total_samples, chunk_size):
            end_idx = min(start_idx + chunk_size, total_samples)
            
            # Load only current chunk
            chunk = data_source[start_idx:end_idx]
            
            # Process chunk
            chunk_result = {
                'mean': np.mean(chunk, axis=1),
                'std': np.std(chunk, axis=1),
                'min': np.min(chunk, axis=1),
                'max': np.max(chunk, axis=1)
            }
            
            results.append(chunk_result)
            
            print(f"Processed chunk {start_idx//chunk_size + 1}/{(total_samples-1)//chunk_size + 1}")
        
        # Combine results
        combined_results = {}
        for key in results[0].keys():
            combined_results[key] = np.concatenate([r[key] for r in results])
        
        return combined_results
    
    # Simulate large dataset
    large_data = np.random.rand(50000, 100)
    
    start_time = time.time()
    results = process_large_dataset_chunked(large_data, chunk_size=5000)
    processing_time = time.time() - start_time
    
    print(f"\nChunked processing completed in {processing_time:.4f}s")
    print(f"Results shape: {results['mean'].shape}")

chunked_processing_example()
```

#### Memory-efficient algorithms

```python
class MemoryEfficientProcessor:
    """Klasa do memory-efficient przetwarzania danych"""
    
    def __init__(self, max_memory_mb=100):
        self.max_memory_mb = max_memory_mb
        self.temp_arrays = {}
    
    def get_optimal_chunk_size(self, data_shape, dtype=np.float64):
        """Oblicz optymalny rozmiar chunk based na dostępnej pamięci"""
        bytes_per_element = np.dtype(dtype).itemsize
        bytes_per_row = data_shape[1] * bytes_per_element
        
        max_bytes = self.max_memory_mb * 1024 * 1024
        optimal_rows = max_bytes // bytes_per_row
        
        return max(1, min(optimal_rows, data_shape[0]))
    
    def correlation_matrix_chunked(self, data):
        """Oblicz macierz korelacji w chunks"""
        n_features = data.shape[1]
        correlation_matrix = np.zeros((n_features, n_features))
        
        # Oblicz średnie
        means = np.mean(data, axis=0)
        
        chunk_size = self.get_optimal_chunk_size(data.shape)
        
        # Covariance calculation in chunks
        n_samples = data.shape[0]
        
        for i in range(0, n_samples, chunk_size):
            end_i = min(i + chunk_size, n_samples)
            chunk = data[i:end_i]
            
            # Center the chunk
            centered_chunk = chunk - means
            
            # Add to correlation matrix
            correlation_matrix += centered_chunk.T @ centered_chunk
        
        # Normalize to get correlation
        correlation_matrix /= (n_samples - 1)
        
        # Convert covariance to correlation
        stds = np.sqrt(np.diag(correlation_matrix))
        correlation_matrix = correlation_matrix / stds[:, np.newaxis]
        correlation_matrix = correlation_matrix / stds[np.newaxis, :]
        
        return correlation_matrix
    
    def pca_chunked(self, data, n_components=2):
        """PCA implementation dla dużych danych"""
        n_features = data.shape[1]
        
        # Center the data
        means = np.mean(data, axis=0)
        
        # Compute covariance matrix in chunks
        cov_matrix = np.zeros((n_features, n_features))
        n_samples = data.shape[0]
        
        chunk_size = self.get_optimal_chunk_size(data.shape)
        
        for i in range(0, n_samples, chunk_size):
            end_i = min(i + chunk_size, n_samples)
            chunk = data[i:end_i] - means
            
            cov_matrix += chunk.T @ chunk
        
        cov_matrix /= (n_samples - 1)
        
        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        # Sort by eigenvalue (descending)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Return top components
        return eigenvectors[:, :n_components], eigenvalues[:n_components]

# Test memory-efficient processor
processor = MemoryEfficientProcessor(max_memory_mb=50)

# Create test data
test_data = np.random.rand(10000, 20)

import time

start_time = time.time()
components, eigenvalues = processor.pca_chunked(test_data, n_components=5)
pca_time = time.time() - start_time

print(f"Memory-efficient PCA completed in {pca_time:.4f}s")
print(f"Components shape: {components.shape}")
print(f"Explained variance ratio: {eigenvalues[:5] / np.sum(eigenvalues)}")
```

---

### 🔧 Memory Debugging i Monitoring

#### Memory leaks detection

```python
import psutil
import os

class MemoryMonitor:
    """Monitor memory usage podczas operacji NumPy"""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.baseline_memory = self.get_memory_usage()
    
    def get_memory_usage(self):
        """Pobierz aktualne użycie pamięci w MB"""
        return self.process.memory_info().rss / 1024 / 1024
    
    def memory_diff(self):
        """Różnica w użyciu pamięci od baseline"""
        return self.get_memory_usage() - self.baseline_memory
    
    def reset_baseline(self):
        """Reset baseline do aktualnego stanu"""
        self.baseline_memory = self.get_memory_usage()
    
    def monitor_operation(self, operation_func, *args, **kwargs):
        """Monitoruj operację i zwróć statystyki pamięci"""
        
        start_memory = self.get_memory_usage()
        
        import time
        start_time = time.time()
        result = operation_func(*args, **kwargs)
        operation_time = time.time() - start_time
        
        peak_memory = self.get_memory_usage()
        
        # Force garbage collection to see actual usage
        import gc
        gc.collect()
        
        end_memory = self.get_memory_usage()
        
        stats = {
            'operation_time': operation_time,
            'start_memory': start_memory,
            'peak_memory': peak_memory,
            'end_memory': end_memory,
            'memory_increase': end_memory - start_memory,
            'peak_increase': peak_memory - start_memory
        }
        
        return result, stats

# Przykład użycia memory monitor
monitor = MemoryMonitor()

def memory_intensive_operation():
    """Operacja intensywnie używająca pamięci"""
    # Tworzenie dużej tablicy
    large_array = np.random.rand(5000, 2000)
    
    # Kilka operacji
    result1 = large_array @ large_array.T
    result2 = np.linalg.svd(result1)
    
    # Zwróć tylko małą część żeby zobaczyć memory cleanup
    return result2[1][:10]  # Tylko singular values

# Monitorowanie operacji
result, stats = monitor.monitor_operation(memory_intensive_operation)

print("Memory Usage Statistics:")
print("=" * 40)
for key, value in stats.items():
    if 'memory' in key:
        print(f"{key:20}: {value:8.2f} MB")
    elif 'time' in key:
        print(f"{key:20}: {value:8.6f} s")

# Test memory leaks
def test_for_memory_leaks():
    """Test na memory leaks w pętli"""
    
    monitor.reset_baseline()
    
    for i in range(10):
        # Operacje które mogą powodować memory leaks
        arr = np.random.rand(1000, 1000)
        result = np.fft.fft2(arr)  # Complex operation
        del arr, result  # Explicit deletion
        
        if i % 3 == 0:
            memory_used = monitor.memory_diff()
            print(f"Iteration {i:2}: Memory diff: {memory_used:6.2f} MB")
    
    # Final memory check
    import gc
    gc.collect()
    final_memory = monitor.memory_diff()
    print(f"Final memory diff: {final_memory:.2f} MB")
    
    if abs(final_memory) < 10:  # Less than 10MB difference
        print("✅ No significant memory leaks detected")
    else:
        print("⚠️  Potential memory leak detected")

test_for_memory_leaks()
```

#### Memory profiling tools integration

```python
def memory_profiling_example():
    """Przykład profilowania pamięci z różnymi narzędziami"""
    
    # 1. Podstawowe profilowanie z tracemalloc
    import tracemalloc
    
    tracemalloc.start()
    
    # Memory-intensive operations
    arrays = []
    for i in range(5):
        arr = np.random.rand(1000, 1000)
        processed = np.fft.fft2(arr)
        arrays.append(processed)
    
    # Get memory statistics
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print("Tracemalloc Statistics:")
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
    
    # 2. Line-by-line memory profiling (manual implementation)
    def line_memory_profile(func):
        """Decorator do line-by-line memory profiling"""
        def wrapper(*args, **kwargs):
            monitor = MemoryMonitor()
            
            print(f"\nProfiling function: {func.__name__}")
            print("-" * 50)
            
            result = func(*args, **kwargs)
            
            print(f"Total memory used: {monitor.memory_diff():.2f} MB")
            return result
        return wrapper
    
    @line_memory_profile
    def example_function():
        # Line 1
        arr1 = np.random.rand(2000, 1000)
        print(f"After arr1 creation: {MemoryMonitor().memory_diff():.2f} MB")
        
        # Line 2
        arr2 = arr1.T @ arr1
        print(f"After matrix multiplication: {MemoryMonitor().memory_diff():.2f} MB")
        
        # Line 3
        result = np.linalg.eig(arr2)
        print(f"After eigendecomposition: {MemoryMonitor().memory_diff():.2f} MB")
        
        return result[0][:5]  # Return only first 5 eigenvalues
    
    result = example_function()
    
    # Cleanup arrays
    del arrays
    import gc
    gc.collect()

memory_profiling_example()
```

---

### 🎯 Best Practices Summary

#### Memory Management Checklist

```python
def memory_best_practices_summary():
    """Podsumowanie best practices dla memory management"""
    
    best_practices = """
    ✅ VIEWS VS COPIES:
    - Używaj slicing dla views (arr[1:5])
    - Unikaj fancy indexing gdy niepotrzebny (tworzy copies)
    - Sprawdzaj np.shares_memory() gdy wątpisz
    - Używaj .copy() świadomie gdy potrzebujesz niezależnych danych
    
    ✅ BROADCASTING:
    - Preferuj broadcasting nad jawnym tilowaniem
    - Używaj keepdims=True dla zachowania wymiarów
    - Planuj shape manipulations dla efektywnego broadcasting
    - Testuj memory usage dla złożonych operacji
    
    ✅ MEMORY LAYOUT:
    - Respektuj C vs Fortran order
    - Używaj .ascontiguousarray() dla cache efficiency
    - Monitoruj strides dla performance
    - Rozważ memory mapping dla dużych danych
    
    ✅ LARGE DATA:
    - Implementuj chunked processing
    - Używaj memory mapping gdy dane > RAM
    - Pre-alokuj tablice gdy znasz rozmiary
    - Implementuj memory monitoring
    
    ✅ DEBUGGING:
    - Używaj tracemalloc dla profiling
    - Monitoruj peak memory usage
    - Testuj na memory leaks w pętlach
    - Explicit cleanup gdy potrzebny (del, gc.collect())
    """
    
    print(best_practices)

memory_best_practices_summary()

# Przykład kompleksowego memory-aware kodu
class MemoryAwareDataProcessor:
    """Przykład klasy z optimized memory management"""
    
    def __init__(self, max_memory_mb=500):
        self.max_memory_mb = max_memory_mb
        self.monitor = MemoryMonitor()
    
    def process_correlation_analysis(self, data):
        """Memory-aware correlation analysis"""
        
        print(f"Starting correlation analysis for shape {data.shape}")
        self.monitor.reset_baseline()
        
        # Chunk size based on available memory
        chunk_size = min(1000, data.shape[0])
        
        # Pre-allocate result arrays
        n_features = data.shape[1]
        correlation_matrix = np.zeros((n_features, n_features), dtype=np.float32)
        
        # Compute in chunks
        means = np.mean(data, axis=0, keepdims=True)  # Broadcasting-friendly shape
        
        for i in range(0, data.shape[0], chunk_size):
            end_i = min(i + chunk_size, data.shape[0])
            
            # Get chunk as view when possible
            chunk = data[i:end_i] - means  # Broadcasting subtraction
            
            # Update correlation matrix
            correlation_matrix += chunk.T @ chunk
            
            # Memory check
            if i % (chunk_size * 5) == 0:
                memory_used = self.monitor.memory_diff()
                print(f"Processed {i:6d} samples, Memory: {memory_used:6.2f} MB")
        
        # Finalize correlation matrix
        correlation_matrix /= (data.shape[0] - 1)
        
        # Convert to correlation from covariance
        stds = np.sqrt(np.diag(correlation_matrix))
        correlation_matrix /= stds[:, np.newaxis]  # Broadcasting division
        correlation_matrix /= stds[np.newaxis, :]
        
        final_memory = self.monitor.memory_diff()
        print(f"Analysis completed, Final memory usage: {final_memory:.2f} MB")
        
        return correlation_matrix

# Test the memory-aware processor
processor = MemoryAwareDataProcessor(max_memory_mb=200)
test_data = np.random.rand(5000, 50)

correlation_result = processor.process_correlation_analysis(test_data)
print(f"Correlation matrix shape: {correlation_result.shape}")
```

---

### 🔗 Powiązane tematy

- [[NumPy - Performance Optimization]] - Optymalizacja wydajności
- [[NumPy - Podstawy]] - Podstawy NumPy
- [[Pandas - Performance Optimization]] - Optymalizacja Pandas
- [[Machine Learning Pipeline - Preprocessing]] - Preprocessing w ML