# Big O Notation

> Mathematical notation used to describe the limiting behavior of algorithms as input size approaches infinity, focusing on the most significant factors that affect performance.

## 📖 Definition

Big O notation describes the upper bound of the time complexity of an algorithm. It gives us an asymptotic upper bound for the growth rate of algorithm runtime or space requirements as input size grows.

## 🎯 Key Concepts

### Formal Definition
f(n) = O(g(n)) if there exist positive constants c and n₀ such that:
**0 ≤ f(n) ≤ c × g(n)** for all n ≥ n₀

This means f(n) grows no faster than g(n) for large values of n.

### Focus on Growth Rate
- **Ignore constants**: 5n² + 3n + 10 → O(n²)
- **Ignore lower-order terms**: n² + n → O(n²)
- **Consider worst case**: Usually analyze the worst-case scenario

## 📊 Common Time Complexities

### O(1) - Constant Time
Algorithm takes same time regardless of input size.

```python
def get_first_element(arr):
    """Always takes same time - O(1)"""
    if arr:
        return arr[0]
    return None

def hash_table_lookup(hash_table, key):
    """Hash table lookup - O(1) average"""
    return hash_table.get(key)
```

### O(log n) - Logarithmic Time
Runtime increases logarithmically with input size.

```python
def binary_search(arr, target):
    """Binary search - O(log n)"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def tree_height(node):
    """Height of balanced binary tree - O(log n)"""
    if not node:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))
```

### O(n) - Linear Time
Runtime increases linearly with input size.

```python
def linear_search(arr, target):
    """Linear search - O(n)"""
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1

def find_maximum(arr):
    """Find maximum element - O(n)"""
    if not arr:
        return None
    
    max_val = arr[0]
    for element in arr[1:]:
        if element > max_val:
            max_val = element
    return max_val
```

### O(n log n) - Linearithmic Time
Common in efficient sorting algorithms.

```python
def merge_sort(arr):
    """Merge sort - O(n log n)"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def heap_sort(arr):
    """Heap sort - O(n log n)"""
    import heapq
    heapq.heapify(arr)  # O(n)
    
    result = []
    while arr:
        result.append(heapq.heappop(arr))  # O(log n) × n times
    
    return result
```

### O(n²) - Quadratic Time
Common in nested loops over input.

```python
def bubble_sort(arr):
    """Bubble sort - O(n²)"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def has_duplicate_pair(arr):
    """Check for duplicate pairs - O(n²)"""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                return True
    return False
```

### O(2ⁿ) - Exponential Time
Often seen in brute force recursive solutions.

```python
def fibonacci_recursive(n):
    """Naive recursive fibonacci - O(2ⁿ)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def power_set(arr):
    """Generate all subsets - O(2ⁿ)"""
    if not arr:
        return [[]]
    
    rest = power_set(arr[1:])
    return rest + [[arr[0]] + subset for subset in rest]
```

### O(n!) - Factorial Time
Extremely slow, often in brute force permutation algorithms.

```python
def generate_permutations(arr):
    """Generate all permutations - O(n!)"""
    if len(arr) <= 1:
        return [arr]
    
    result = []
    for i in range(len(arr)):
        rest = arr[:i] + arr[i+1:]
        for perm in generate_permutations(rest):
            result.append([arr[i]] + perm)
    
    return result

def traveling_salesman_brute_force(cities):
    """TSP brute force - O(n!)"""
    import itertools
    min_distance = float('inf')
    best_path = None
    
    for path in itertools.permutations(cities[1:]):
        full_path = [cities[0]] + list(path) + [cities[0]]
        distance = calculate_path_distance(full_path)
        if distance < min_distance:
            min_distance = distance
            best_path = full_path
    
    return best_path, min_distance
```

## 📈 Growth Rate Visualization

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_complexity_growth():
    n = np.array([1, 2, 4, 8, 16, 32, 64, 128])
    
    # Different complexity classes
    constant = np.ones_like(n)
    logarithmic = np.log2(n)
    linear = n
    linearithmic = n * np.log2(n)
    quadratic = n ** 2
    exponential = 2 ** n
    
    plt.figure(figsize=(12, 8))
    plt.plot(n, constant, 'g-', label='O(1) - Constant')
    plt.plot(n, logarithmic, 'b-', label='O(log n) - Logarithmic')
    plt.plot(n, linear, 'orange', label='O(n) - Linear')
    plt.plot(n, linearithmic, 'r-', label='O(n log n) - Linearithmic')
    plt.plot(n, quadratic, 'purple', label='O(n²) - Quadratic')
    plt.plot(n[:6], exponential[:6], 'm-', label='O(2ⁿ) - Exponential')
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Operations')
    plt.title('Algorithm Complexity Growth Rates')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.show()
```

## 🔍 Analysis Examples

### Example 1: Nested Loops
```python
def analyze_nested_loops(arr):
    """
    What's the time complexity?
    
    Outer loop: n iterations
    Inner loop: n iterations for each outer
    Total: n × n = n² operations
    
    Answer: O(n²)
    """
    n = len(arr)
    count = 0
    
    for i in range(n):          # O(n)
        for j in range(n):      # O(n) for each i
            count += 1          # O(1)
    
    return count  # Total: O(n²)
```

### Example 2: Logarithmic Pattern
```python
def analyze_logarithmic(n):
    """
    What's the time complexity?
    
    Loop runs while i < n
    i doubles each iteration: 1, 2, 4, 8, 16, ...
    Number of iterations: log₂(n)
    
    Answer: O(log n)
    """
    i = 1
    count = 0
    
    while i < n:
        count += 1
        i *= 2      # Key: i doubles each time
    
    return count  # Total: O(log n)
```

### Example 3: Divide and Conquer
```python
def analyze_divide_conquer(arr):
    """
    Merge sort analysis:
    
    T(n) = 2T(n/2) + O(n)
    
    Using Master Theorem:
    a = 2, b = 2, f(n) = O(n)
    log_b(a) = log₂(2) = 1
    
    Since f(n) = O(n¹), we have Case 2
    Answer: O(n log n)
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = analyze_divide_conquer(arr[:mid])   # T(n/2)
    right = analyze_divide_conquer(arr[mid:])  # T(n/2)
    
    return merge(left, right)  # O(n)
```

## 🎯 Best, Average, and Worst Case

Different cases can have different complexities:

```python
def quick_sort_analysis(arr):
    """
    Quick Sort Complexity Analysis:
    
    Best Case: O(n log n)
    - Pivot always divides array in half
    
    Average Case: O(n log n)
    - Random pivot selection
    
    Worst Case: O(n²)
    - Pivot is always smallest/largest
    - Happens with sorted input and bad pivot choice
    """
    pass

def binary_search_analysis(arr, target):
    """
    Binary Search Complexity Analysis:
    
    Best Case: O(1)
    - Target is at middle position
    
    Average Case: O(log n)
    - Target found after log₂(n) comparisons
    
    Worst Case: O(log n)
    - Target not in array or at boundary
    """
    pass
```

## 🚀 Space Complexity

Big O also applies to memory usage:

```python
def space_complexity_examples():
    """Examples of different space complexities"""
    
    def constant_space(arr):
        """O(1) space - only uses few variables"""
        max_val = arr[0]
        for element in arr[1:]:
            if element > max_val:
                max_val = element
        return max_val
    
    def linear_space(n):
        """O(n) space - creates array of size n"""
        return [i for i in range(n)]
    
    def quadratic_space(n):
        """O(n²) space - creates 2D array"""
        return [[0 for _ in range(n)] for _ in range(n)]
    
    def recursive_space(n):
        """O(n) space - recursion uses call stack"""
        if n <= 0:
            return 1
        return recursive_space(n - 1)
```

## 💡 Practical Tips

### 1. Common Patterns
```python
# O(n) - Single loop
for i in range(n):
    do_something()

# O(n²) - Nested loops
for i in range(n):
    for j in range(n):
        do_something()

# O(log n) - Divide by half each time
while n > 1:
    n //= 2
    do_something()

# O(n log n) - Divide and conquer
def divide_conquer(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = divide_conquer(arr[:mid])    # T(n/2)
    right = divide_conquer(arr[mid:])   # T(n/2)
    
    return combine(left, right)  # O(n)
```

### 2. Drop Constants and Lower Terms
```python
# 5n² + 3n + 10 → O(n²)
# 2n log n + n → O(n log n)  
# 100 → O(1)
# n/2 → O(n)
```

### 3. Consider Input Characteristics
```python
def search_in_array(arr, target):
    """
    Time complexity depends on array properties:
    - Unsorted: O(n) linear search
    - Sorted: O(log n) binary search
    - Hash table: O(1) average lookup
    """
    pass
```

## 📊 Complexity Hierarchy

**From fastest to slowest:**
1. O(1) - Constant
2. O(log n) - Logarithmic  
3. O(n) - Linear
4. O(n log n) - Linearithmic
5. O(n²) - Quadratic
6. O(n³) - Cubic
7. O(2ⁿ) - Exponential
8. O(n!) - Factorial

## 🔗 Related Topics

- [[Time Complexity]] - Detailed time analysis
- [[Space Complexity]] - Memory usage analysis
- [[Amortized Analysis]] - Average cost over sequence
- [[Sorting Algorithms]] - Complexity comparisons

## 📝 Practice Problems

1. **Analyze Code Complexity**: Determine Big O of given algorithms
2. **Optimize Algorithms**: Improve time complexity of solutions
3. **Trade-offs**: Choose between time vs space complexity
4. **Real-world Applications**: Apply Big O to system design

## 💡 Common Mistakes

1. **Ignoring hidden operations**: `arr.insert(0, x)` is O(n), not O(1)
2. **Confusing average and worst case**: Hash tables are O(1) average, O(n) worst
3. **Not considering input size**: Small inputs may favor different algorithms
4. **Premature optimization**: Focus on correctness first, then optimize

---

*See also: [[Time Complexity]], [[Space Complexity]], [[algorithms_and_ds]]*