# Binary Search

> Efficient search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half.

## 📖 Definition

Binary search is a search algorithm that works on sorted arrays by comparing the target value to the middle element and eliminating half of the remaining elements with each comparison.

## 🎯 Key Requirements

- **Sorted Array**: Data must be in sorted order
- **Random Access**: Must be able to access elements by index
- **Comparison**: Elements must be comparable

## ⚡ Time Complexity

- **Best Case**: O(1) - target is at middle
- **Average Case**: O(log n)
- **Worst Case**: O(log n) - target not found or at boundary
- **Space Complexity**: O(1) iterative, O(log n) recursive

## 🐍 Python Implementation

```python
def binary_search_iterative(arr, target):
    """
    Iterative binary search implementation
    Returns index if found, -1 if not found
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Prevents overflow
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Target not found

def binary_search_recursive(arr, target, left=0, right=None):
    """
    Recursive binary search implementation
    """
    if right is None:
        right = len(arr) - 1
    
    # Base case: element not found
    if left > right:
        return -1
    
    mid = left + (right - left) // 2
    
    # Element found
    if arr[mid] == target:
        return mid
    # Target is in left half
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, left, mid - 1)
    # Target is in right half
    else:
        return binary_search_recursive(arr, target, mid + 1, right)

def binary_search_leftmost(arr, target):
    """
    Find leftmost occurrence of target (first occurrence)
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left if left < len(arr) and arr[left] == target else -1

def binary_search_rightmost(arr, target):
    """
    Find rightmost occurrence of target (last occurrence)
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left - 1 if left > 0 and arr[left - 1] == target else -1

def search_range(arr, target):
    """
    Find first and last position of target in sorted array
    Returns [-1, -1] if not found
    """
    left_idx = binary_search_leftmost(arr, target)
    if left_idx == -1:
        return [-1, -1]
    
    right_idx = binary_search_rightmost(arr, target)
    return [left_idx, right_idx]

# Binary search on answer pattern
def sqrt_binary_search(x):
    """
    Find square root using binary search
    """
    if x < 2:
        return x
    
    left, right = 2, x // 2
    
    while left <= right:
        mid = left + (right - left) // 2
        square = mid * mid
        
        if square == x:
            return mid
        elif square < x:
            left = mid + 1
        else:
            right = mid - 1
    
    return right  # Return floor of square root

# Search in rotated sorted array
def search_rotated_array(arr, target):
    """
    Search in rotated sorted array
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        
        # Left half is sorted
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1

# Example usage and testing
def test_binary_search():
    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 7
    
    print(f"Array: {arr}")
    print(f"Target: {target}")
    print(f"Iterative result: {binary_search_iterative(arr, target)}")
    print(f"Recursive result: {binary_search_recursive(arr, target)}")
    
    # Test with duplicates
    arr_dup = [1, 2, 2, 2, 3, 4, 4, 5]
    target = 2
    print(f"\\nArray with duplicates: {arr_dup}")
    print(f"Leftmost {target}: {binary_search_leftmost(arr_dup, target)}")
    print(f"Rightmost {target}: {binary_search_rightmost(arr_dup, target)}")
    print(f"Range of {target}: {search_range(arr_dup, target)}")
```

## ☕ Java Implementation

```java
public class BinarySearch {
    
    public static int binarySearchIterative(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1; // Not found
    }
    
    public static int binarySearchRecursive(int[] arr, int target) {
        return binarySearchRecursive(arr, target, 0, arr.length - 1);
    }
    
    private static int binarySearchRecursive(int[] arr, int target, int left, int right) {
        if (left > right) {
            return -1; // Base case: not found
        }
        
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            return binarySearchRecursive(arr, target, mid + 1, right);
        } else {
            return binarySearchRecursive(arr, target, left, mid - 1);
        }
    }
    
    public static int findLeftmostOccurrence(int[] arr, int target) {
        int left = 0, right = arr.length;
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return (left < arr.length && arr[left] == target) ? left : -1;
    }
    
    public static int findRightmostOccurrence(int[] arr, int target) {
        int left = 0, right = arr.length;
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] <= target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return (left > 0 && arr[left - 1] == target) ? left - 1 : -1;
    }
    
    public static int[] searchRange(int[] arr, int target) {
        int left = findLeftmostOccurrence(arr, target);
        if (left == -1) {
            return new int[]{-1, -1};
        }
        
        int right = findRightmostOccurrence(arr, target);
        return new int[]{left, right};
    }
    
    // Binary search for insertion point
    public static int searchInsertPosition(int[] arr, int target) {
        int left = 0, right = arr.length;
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return left;
    }
    
    // Search in rotated sorted array
    public static int searchRotatedArray(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            }
            
            // Left half is sorted
            if (arr[left] <= arr[mid]) {
                if (arr[left] <= target && target < arr[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } 
            // Right half is sorted
            else {
                if (arr[mid] < target && target <= arr[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }
        
        return -1;
    }
    
    public static void main(String[] args) {
        int[] arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
        int target = 7;
        
        System.out.println("Iterative: " + binarySearchIterative(arr, target));
        System.out.println("Recursive: " + binarySearchRecursive(arr, target));
        
        int[] duplicates = {1, 2, 2, 2, 3, 4, 4, 5};
        System.out.println("Range of 2: " + Arrays.toString(searchRange(duplicates, 2)));
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

class BinarySearch {
public:
    // Iterative implementation
    static int binarySearchIterative(const std::vector<int>& arr, int target) {
        int left = 0, right = arr.size() - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
    
    // Recursive implementation
    static int binarySearchRecursive(const std::vector<int>& arr, int target, 
                                   int left = -1, int right = -1) {
        if (left == -1) left = 0;
        if (right == -1) right = arr.size() - 1;
        
        if (left > right) {
            return -1;
        }
        
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            return binarySearchRecursive(arr, target, mid + 1, right);
        } else {
            return binarySearchRecursive(arr, target, left, mid - 1);
        }
    }
    
    // Find leftmost occurrence
    static int findLeftmost(const std::vector<int>& arr, int target) {
        int left = 0, right = arr.size();
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return (left < arr.size() && arr[left] == target) ? left : -1;
    }
    
    // Find rightmost occurrence
    static int findRightmost(const std::vector<int>& arr, int target) {
        int left = 0, right = arr.size();
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] <= target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return (left > 0 && arr[left - 1] == target) ? left - 1 : -1;
    }
    
    // Using STL binary search functions
    static void stlBinarySearch(const std::vector<int>& arr, int target) {
        // Check if element exists
        bool found = std::binary_search(arr.begin(), arr.end(), target);
        std::cout << "STL binary_search found " << target << ": " << found << std::endl;
        
        // Find lower bound (first position where target could be inserted)
        auto lower = std::lower_bound(arr.begin(), arr.end(), target);
        if (lower != arr.end() && *lower == target) {
            std::cout << "Lower bound index: " << (lower - arr.begin()) << std::endl;
        }
        
        // Find upper bound (first position after target)
        auto upper = std::upper_bound(arr.begin(), arr.end(), target);
        std::cout << "Upper bound index: " << (upper - arr.begin()) << std::endl;
        
        // Equal range (returns pair of lower and upper bounds)
        auto range = std::equal_range(arr.begin(), arr.end(), target);
        std::cout << "Equal range: [" << (range.first - arr.begin()) 
                 << ", " << (range.second - arr.begin()) << ")" << std::endl;
    }
};

// Template version for generic types
template<typename T>
int binarySearchTemplate(const std::vector<T>& arr, const T& target) {
    int left = 0, right = arr.size() - 1;
    
    while (left <= right) {
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return -1;
}

int main() {
    std::vector<int> arr = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
    int target = 7;
    
    std::cout << "Array: ";
    for (int x : arr) std::cout << x << " ";
    std::cout << std::endl;
    
    std::cout << "Target: " << target << std::endl;
    std::cout << "Iterative result: " << BinarySearch::binarySearchIterative(arr, target) << std::endl;
    std::cout << "Recursive result: " << BinarySearch::binarySearchRecursive(arr, target) << std::endl;
    
    // Test with duplicates
    std::vector<int> duplicates = {1, 2, 2, 2, 3, 4, 4, 5};
    target = 2;
    std::cout << "\\nWith duplicates, target " << target << ":" << std::endl;
    std::cout << "Leftmost: " << BinarySearch::findLeftmost(duplicates, target) << std::endl;
    std::cout << "Rightmost: " << BinarySearch::findRightmost(duplicates, target) << std::endl;
    
    BinarySearch::stlBinarySearch(duplicates, target);
    
    return 0;
}
```

## 🎯 Binary Search Variants

### 1. Search Insert Position
```python
def search_insert_position(arr, target):
    \"\"\"Find position where target should be inserted\"\"\"
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left
```

### 2. Peak Element
```python
def find_peak_element(arr):
    \"\"\"Find any peak element in array\"\"\"
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] > arr[mid + 1]:
            right = mid
        else:
            left = mid + 1
    
    return left
```

### 3. Find Minimum in Rotated Array
```python
def find_min_rotated(arr):
    \"\"\"Find minimum in rotated sorted array\"\"\"
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] > arr[right]:
            left = mid + 1
        else:
            right = mid
    
    return left
```

## 🔍 Applications

### 1. Database Indexing
- B-tree indexes use binary search principles
- Fast lookup in sorted database tables

### 2. Library Functions
- `std::binary_search`, `std::lower_bound` in C++
- `bisect` module in Python
- `Arrays.binarySearch()` in Java

### 3. Game Development
- Collision detection optimization
- Level-of-detail selection

### 4. Numerical Computing
- Finding roots of equations
- Optimization algorithms

## 💡 Tips and Best Practices

1. **Overflow prevention**: Use `mid = left + (right - left) // 2`
2. **Boundary conditions**: Careful with `<=` vs `<` in while loop
3. **Integer division**: Be aware of floor division behavior
4. **Sorted requirement**: Always ensure array is sorted
5. **Edge cases**: Handle empty arrays and single elements

## 🐛 Common Pitfalls

1. **Infinite loops**: Wrong boundary updates
2. **Off-by-one errors**: Incorrect mid calculation or boundary handling
3. **Integer overflow**: Using `(left + right) / 2`
4. **Unsorted data**: Binary search only works on sorted data

## 📝 Practice Problems

1. **Find First and Last Position**: Search for range in sorted array
2. **Search Insert Position**: Find insertion point for target
3. **Search in Rotated Array**: Handle rotated sorted arrays
4. **Find Peak Element**: Locate local maximum
5. **Sqrt(x)**: Implement square root using binary search
6. **Search 2D Matrix**: Binary search in sorted matrix
7. **Find Minimum in Rotated Array**: Locate minimum element
8. **Valid Perfect Square**: Check if number is perfect square

## 🔗 Related Topics

- [[Arrays and Lists]] - Binary search operates on arrays
- [[Binary Search Trees]] - Tree equivalent of binary search
- [[Divide and Conquer]] - Binary search is divide and conquer algorithm
- [[Sorting Algorithms]] - Binary search requires sorted data

---

*See also: [[Linear Search]], [[Binary Search Trees]], [[Sorting Algorithms]], [[algorithms_and_ds]]*