# Divide and Conquer

> Problem-solving paradigm that breaks down complex problems into smaller, more manageable subproblems, solves them independently, and combines the results.

## 📖 Definition

Divide and conquer is an algorithmic paradigm that recursively breaks down a problem into sub-problems of similar type until they become simple enough to be solved directly. The solutions are then combined to give a solution to the original problem.

## 🔑 Three Steps

1. **Divide**: Break the problem into smaller subproblems
2. **Conquer**: Solve subproblems recursively
3. **Combine**: Merge solutions to get final result

## ⚡ Time Complexity Analysis

Most divide and conquer algorithms follow the recurrence:
**T(n) = aT(n/b) + f(n)**

Using Master Theorem:
- If f(n) = O(n^(log_b(a) - ε)): T(n) = Θ(n^log_b(a))
- If f(n) = Θ(n^log_b(a)): T(n) = Θ(n^log_b(a) × log n)
- If f(n) = Ω(n^(log_b(a) + ε)): T(n) = Θ(f(n))

## 🐍 Python Implementation Examples

```python
# Classic Example 1: Merge Sort
def merge_sort(arr):
    """Divide and conquer sorting"""
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer & Combine
    return merge(left, right)

def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Example 2: Maximum Subarray (Kadane's Algorithm D&C version)
def max_subarray_dc(arr):
    """Maximum subarray using divide and conquer"""
    def max_crossing_sum(arr, low, mid, high):
        """Find max sum crossing the midpoint"""
        left_sum = float('-inf')
        sum_val = 0
        for i in range(mid, low - 1, -1):
            sum_val += arr[i]
            left_sum = max(left_sum, sum_val)
        
        right_sum = float('-inf')
        sum_val = 0
        for i in range(mid + 1, high + 1):
            sum_val += arr[i]
            right_sum = max(right_sum, sum_val)
        
        return left_sum + right_sum
    
    def max_subarray_helper(arr, low, high):
        if low == high:
            return arr[low]
        
        mid = (low + high) // 2
        
        left_sum = max_subarray_helper(arr, low, mid)
        right_sum = max_subarray_helper(arr, mid + 1, high)
        cross_sum = max_crossing_sum(arr, low, mid, high)
        
        return max(left_sum, right_sum, cross_sum)
    
    return max_subarray_helper(arr, 0, len(arr) - 1)

# Example 3: Quick Sort
def quick_sort(arr):
    """Quick sort using divide and conquer"""
    if len(arr) <= 1:
        return arr
    
    # Divide
    pivot = partition(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    # Conquer and Combine
    return quick_sort(left) + middle + quick_sort(right)

def partition(arr):
    """Simple pivot selection"""
    return arr[len(arr) // 2]

# Example 4: Binary Search
def binary_search_dc(arr, target):
    """Binary search using divide and conquer"""
    def search_helper(left, right):
        if left > right:
            return -1
        
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] > target:
            return search_helper(left, mid - 1)
        else:
            return search_helper(mid + 1, right)
    
    return search_helper(0, len(arr) - 1)

# Example 5: Closest Pair of Points
def closest_pair(points):
    """Find closest pair using divide and conquer"""
    import math
    
    def distance(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def brute_force(points):
        min_dist = float('inf')
        n = len(points)
        closest = None
        
        for i in range(n):
            for j in range(i + 1, n):
                dist = distance(points[i], points[j])
                if dist < min_dist:
                    min_dist = dist
                    closest = (points[i], points[j])
        
        return min_dist, closest
    
    def closest_pair_rec(px, py):
        n = len(px)
        
        # Base case for small arrays
        if n <= 3:
            return brute_force(px)
        
        # Divide
        mid = n // 2
        midpoint = px[mid]
        
        pyl = [point for point in py if point[0] < midpoint[0] or 
               (point[0] == midpoint[0] and point[1] < midpoint[1])]
        pyr = [point for point in py if point not in pyl]
        
        # Conquer
        dl, pair_l = closest_pair_rec(px[:mid], pyl)
        dr, pair_r = closest_pair_rec(px[mid:], pyr)
        
        # Find minimum of the two halves
        if dl < dr:
            min_dist, closest = dl, pair_l
        else:
            min_dist, closest = dr, pair_r
        
        # Check points across the divide
        strip = [point for point in py if abs(point[0] - midpoint[0]) < min_dist]
        
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[j][1] - strip[i][1] >= min_dist:
                    break
                dist = distance(strip[i], strip[j])
                if dist < min_dist:
                    min_dist = dist
                    closest = (strip[i], strip[j])
        
        return min_dist, closest
    
    # Sort points by x and y coordinates
    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    
    return closest_pair_rec(px, py)

# Example usage
if __name__ == "__main__":
    # Merge sort
    arr = [12, 11, 13, 5, 6, 7]
    print("Original array:", arr)
    sorted_arr = merge_sort(arr)
    print("Merge sorted:", sorted_arr)
    
    # N-Queens
    print("\n4-Queens solutions:")
    solutions = solve_n_queens(4)
    for i, solution in enumerate(solutions):
        print(f"Solution {i + 1}:")
        print_queens_solution(solution)
    
    # Maximum subarray
    arr = [-2, -3, 4, -1, -2, 1, 5, -3]
    max_sum = max_subarray_dc(arr)
    print(f"Maximum subarray sum: {max_sum}")
    
    # Closest pair
    points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    min_dist, pair = closest_pair(points)
    print(f"Closest pair: {pair} with distance {min_dist:.2f}")
```

## 🎯 Common Divide and Conquer Algorithms

### Sorting Algorithms
- [[Merge Sort]] - O(n log n) stable sorting
- [[Quick Sort]] - O(n log n) average case

### Searching Algorithms
- [[Binary Search]] - O(log n) search in sorted array
- **Ternary Search** - Divide into three parts

### Mathematical Algorithms
- **Fast Multiplication** - Karatsuba algorithm
- **Fast Exponentiation** - Matrix exponentiation
- **FFT** - Fast Fourier Transform

### Geometric Algorithms
- **Closest Pair** - Find nearest points
- **Convex Hull** - Find convex boundary

## 💡 Design Guidelines

1. **Subproblem Size**: Ideally divide into equal or nearly equal parts
2. **Base Case**: Define clear stopping condition
3. **Combine Step**: Efficiently merge subproblem solutions
4. **Overlap**: Minimize redundant computation

## 🔧 When to Use Divide and Conquer

✅ **Use when:**
- Problem can be divided into similar subproblems
- Subproblems are independent
- Combination step is efficient
- Recursive structure is natural

❌ **Avoid when:**
- Subproblems heavily overlap (use DP instead)
- Division overhead is too high
- Problem is already simple enough

## 🆚 vs Other Paradigms

| Paradigm | Subproblems | Overlap | Strategy |
|----------|-------------|---------|----------|
| **Divide & Conquer** | Independent | No | Divide into parts |
| **Dynamic Programming** | Dependent | Yes | Store results |
| **Greedy** | None | No | Local optimal choice |
| **Backtracking** | Constraint-based | No | Explore with pruning |

## 🔗 Related Topics

- [[Merge Sort]] - Classic divide and conquer example
- [[Quick Sort]] - Another divide and conquer sort
- [[Binary Search]] - Search using divide and conquer
- [[Dynamic Programming]] - Alternative for overlapping subproblems

---

*See also: [[Merge Sort]], [[Quick Sort]], [[algorithms_and_ds]]*