# Time Complexity

> Computational complexity that describes the amount of time an algorithm takes to run as a function of the length of the input, focusing on growth rate for large inputs.

## 📖 Definition

Time complexity measures how the runtime of an algorithm grows with input size. It helps us:
- Compare algorithm efficiency
- Predict performance on large datasets
- Choose appropriate algorithms for constraints

## 🎯 Asymptotic Notation

### Big O (O) - Upper Bound
Describes the worst-case or upper bound of growth rate.
```
f(n) = O(g(n)) means f(n) ≤ c × g(n) for large n
```

### Big Omega (Ω) - Lower Bound  
Describes the best-case or lower bound of growth rate.
```
f(n) = Ω(g(n)) means f(n) ≥ c × g(n) for large n
```

### Big Theta (Θ) - Tight Bound
When upper and lower bounds are the same.
```
f(n) = Θ(g(n)) means f(n) = O(g(n)) and f(n) = Ω(g(n))
```

## ⏱️ Common Time Complexities

### O(1) - Constant Time
```python
def get_first(arr):
    """Always takes same time regardless of input size"""
    if arr:
        return arr[0]
    return None

def hash_lookup(dictionary, key):
    """Hash table lookup - O(1) average case"""
    return dictionary.get(key)

# Array access by index
arr[5]  # O(1)

# Basic arithmetic operations  
x + y   # O(1)
```

### O(log n) - Logarithmic Time
```python
def binary_search(arr, target):
    """Each iteration eliminates half the remaining elements"""
    left, right = 0, len(arr) - 1
    
    while left <= right:  # At most log₂(n) iterations
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def tree_height(node):
    """Height of balanced binary tree"""
    if not node:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))
```

### O(n) - Linear Time  
```python
def linear_search(arr, target):
    """Might need to check every element once"""
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1

def sum_array(arr):
    """Must visit every element exactly once"""
    total = 0
    for num in arr:
        total += num
    return total

def find_max(arr):
    """Single pass through array"""
    if not arr:
        return None
    
    max_val = arr[0]
    for element in arr[1:]:  # n-1 comparisons
        if element > max_val:
            max_val = element
    return max_val
```

### O(n log n) - Linearithmic Time
```python
def merge_sort(arr):
    """Divide and conquer: log n levels, O(n) work per level"""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])    # T(n/2)
    right = merge_sort(arr[mid:])   # T(n/2)
    
    return merge(left, right)       # O(n)
    # Total: T(n) = 2T(n/2) + O(n) = O(n log n)

def heap_sort(arr):
    """Build heap O(n) + n extract operations O(log n) each"""
    import heapq
    heapq.heapify(arr)  # O(n)
    
    result = []
    while arr:
        result.append(heapq.heappop(arr))  # O(log n) × n times
    
    return result  # Total: O(n log n)
```

### O(n²) - Quadratic Time
```python
def bubble_sort(arr):
    """Nested loops: outer runs n times, inner runs up to n times"""
    n = len(arr)
    for i in range(n):              # n iterations
        for j in range(0, n - i - 1):   # up to n iterations
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def selection_sort(arr):
    """For each position, find minimum in remaining array"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):   # Nested loop
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def has_duplicate_pair(arr):
    """Check all pairs for duplicates"""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):   # O(n²) comparisons
            if arr[i] == arr[j]:
                return True
    return False
```

### O(2ⁿ) - Exponential Time
```python
def fibonacci_naive(n):
    """Each call branches into 2 recursive calls"""
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)
    # Creates binary tree of calls with ~2ⁿ nodes

def generate_subsets(arr):
    """Generate all possible subsets (power set)"""
    if not arr:
        return [[]]
    
    first = arr[0]
    rest_subsets = generate_subsets(arr[1:])
    
    # Each subset can either include or exclude first element
    return rest_subsets + [[first] + subset for subset in rest_subsets]
    # 2ⁿ subsets total
```

### O(n!) - Factorial Time
```python
def generate_permutations(arr):
    """Generate all possible arrangements"""
    if len(arr) <= 1:
        return [arr]
    
    result = []
    for i in range(len(arr)):
        first = arr[i]
        rest = arr[:i] + arr[i+1:]
        for perm in generate_permutations(rest):
            result.append([first] + perm)
    
    return result  # n! permutations

def traveling_salesman_brute_force(cities):
    """Try all possible routes"""
    import itertools
    min_distance = float('inf')
    
    for route in itertools.permutations(cities[1:]):  # (n-1)! permutations
        distance = calculate_total_distance([cities[0]] + list(route) + [cities[0]])
        min_distance = min(min_distance, distance)
    
    return min_distance
```

## 📊 Analysis Techniques

### 1. Counting Primitive Operations
```python
def example_analysis(arr):
    """Count each operation's contribution to time complexity"""
    n = len(arr)                    # O(1)
    total = 0                       # O(1)
    
    for i in range(n):              # Loop runs n times
        for j in range(i, n):       # Inner loop: (n + (n-1) + ... + 1) = n(n+1)/2
            total += arr[j]         # O(1) operation
    
    return total                    # O(1)
    
    # Total: O(1) + O(n²) + O(1) = O(n²)
```

### 2. Recurrence Relations
```python
def merge_sort_analysis(n):
    """
    Merge sort recurrence:
    T(n) = 2T(n/2) + O(n)
    
    Using Master Theorem:
    a = 2, b = 2, f(n) = O(n)
    log_b(a) = log₂(2) = 1
    Since f(n) = O(n¹), we have Case 2
    Therefore T(n) = O(n log n)
    """
    
def binary_search_analysis(n):
    """
    Binary search recurrence:
    T(n) = T(n/2) + O(1)
    
    Using Master Theorem:
    a = 1, b = 2, f(n) = O(1)
    log_b(a) = log₂(1) = 0
    Since f(n) = O(1) = O(n⁰), we have Case 2
    Therefore T(n) = O(log n)
    """
```

### 3. Loop Analysis Patterns
```python
# Single loop - O(n)
for i in range(n):
    do_something()  # O(1)

# Nested loops - O(n²)
for i in range(n):
    for j in range(n):
        do_something()  # O(1)

# Dependent nested loops - O(n²)
for i in range(n):
    for j in range(i, n):  # j depends on i
        do_something()  # Still O(n²) total iterations

# Loop with halving - O(log n)
i = n
while i > 1:
    do_something()  # O(1)
    i //= 2         # Divide by 2 each iteration

# Loop with multiplication - O(log n)
i = 1
while i < n:
    do_something()  # O(1)
    i *= 2          # Double each iteration
```

## 🎯 Best, Average, and Worst Cases

```python
def quicksort_analysis():
    """
    Quick Sort time complexity varies by case:
    
    Best Case: O(n log n)
    - Pivot always divides array evenly
    - Recurrence: T(n) = 2T(n/2) + O(n)
    
    Average Case: O(n log n)  
    - Random pivot selection
    - Expected depth is log n
    
    Worst Case: O(n²)
    - Pivot is always smallest or largest
    - Recurrence: T(n) = T(n-1) + O(n)
    - Happens with sorted input and bad pivot choice
    """

def linear_search_analysis():
    """
    Linear search cases:
    
    Best Case: O(1)
    - Target is first element
    
    Average Case: O(n)
    - On average, find target in middle
    - Expected comparisons: n/2
    
    Worst Case: O(n)
    - Target is last element or not present
    - Must check all n elements
    """
```

## 🔍 Hidden Complexities

### Library Function Complexities
```python
# Python list operations
arr.append(x)           # O(1) amortized
arr.insert(0, x)        # O(n) - shift all elements
arr.pop()               # O(1)
arr.pop(0)              # O(n) - shift all elements
arr.remove(x)           # O(n) - search + remove
arr.index(x)            # O(n) - linear search
x in arr                # O(n) - linear search

# String operations  
s1 + s2                 # O(len(s1) + len(s2))
s.replace(old, new)     # O(n × len(old))
s.split()               # O(n)

# Dictionary operations
dict[key]               # O(1) average, O(n) worst
dict.keys()             # O(n)
dict.values()           # O(n)

# Sorting
arr.sort()              # O(n log n)
sorted(arr)             # O(n log n)
```

### Nested Function Calls
```python
def complex_operation(arr):
    """Hidden complexity in nested calls"""
    result = []
    
    for element in arr:                    # O(n)
        sorted_sub = sorted(element)       # O(k log k) where k is len(element)
        result.extend(sorted_sub)          # O(k)
    
    return sorted(result)                  # O(m log m) where m is len(result)
    
    # If each element has length k, total complexity could be O(n × k log k + m log m)
```

## 💡 Optimization Strategies

### 1. Choose Better Algorithms
```python
# Bad: O(n²) search for duplicates
def has_duplicates_slow(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False

# Good: O(n) using set
def has_duplicates_fast(arr):
    seen = set()
    for element in arr:
        if element in seen:
            return True
        seen.add(element)
    return False
```

### 2. Memoization for Overlapping Subproblems
```python
# Bad: O(2ⁿ) naive Fibonacci
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

# Good: O(n) with memoization
def fib_fast(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fib_fast(n - 1, memo) + fib_fast(n - 2, memo)
    return memo[n]
```

### 3. Early Termination
```python
def search_with_early_exit(arr, target):
    """Stop as soon as target is found"""
    for i, element in enumerate(arr):
        if element == target:
            return i  # Early termination
    return -1

def all_positive(arr):
    """Stop as soon as negative found"""
    for num in arr:
        if num <= 0:
            return False  # Early termination
    return True
```

## 🔗 Related Topics

- [[Big O Notation]] - Asymptotic notation for complexity
- [[Space Complexity]] - Memory usage analysis
- [[Amortized Analysis]] - Average-case over sequence of operations

## 📝 Practice Problems

1. **Analyze Given Code**: Determine time complexity of algorithms
2. **Two Sum**: Improve from O(n²) to O(n) using hash map
3. **Three Sum**: Optimize from O(n³) to O(n²)
4. **Subarray Sum**: Use prefix sums for O(1) range queries
5. **Longest Substring**: Sliding window technique for O(n)

---

*See also: [[Big O Notation]], [[Space Complexity]], [[algorithms_and_ds]]*