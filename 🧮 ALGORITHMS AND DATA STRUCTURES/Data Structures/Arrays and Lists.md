# Arrays and Lists

> Fundamental linear data structures that store elements in contiguous memory locations with direct index access.

## 📖 Definition

Arrays are collections of elements stored in contiguous memory locations, accessible via indices. Lists are dynamic arrays that can grow and shrink during runtime.

## 🔑 Key Properties

- **Direct Access**: O(1) access time by index
- **Fixed Size** (Static Arrays): Size determined at declaration
- **Dynamic Size** (Lists/Dynamic Arrays): Can resize during runtime
- **Homogeneous**: All elements of the same type (in most languages)

## 🐍 Python Implementation

```python
# Static-like array (using list)
arr = [1, 2, 3, 4, 5]

# Dynamic list operations
numbers = []
numbers.append(10)      # Add element - O(1) amortized
numbers.insert(0, 5)    # Insert at index - O(n)
numbers.remove(10)      # Remove by value - O(n)
numbers.pop()           # Remove last - O(1)
numbers.pop(0)          # Remove by index - O(n)

# Access and modification
print(numbers[0])       # Access - O(1)
numbers[0] = 100        # Modify - O(1)

# Useful operations
length = len(numbers)   # Get size - O(1)
numbers.reverse()       # Reverse in place - O(n)
numbers.sort()          # Sort in place - O(n log n)

# List comprehension
squares = [x**2 for x in range(10)]
```

## ☕ Java Implementation

```java
import java.util.*;

public class ArraysAndLists {
    public static void main(String[] args) {
        // Static array
        int[] staticArray = new int[5];
        staticArray[0] = 10;
        
        // Or initialize with values
        int[] numbers = {1, 2, 3, 4, 5};
        
        // Dynamic list (ArrayList)
        ArrayList<Integer> list = new ArrayList<>();
        list.add(10);           // Add element - O(1) amortized
        list.add(0, 5);         // Insert at index - O(n)
        list.remove(0);         // Remove by index - O(n)
        list.remove(Integer.valueOf(10)); // Remove by value - O(n)
        
        // Access and modification
        int value = list.get(0);    // Access - O(1)
        list.set(0, 100);          // Modify - O(1)
        
        // Useful operations
        int size = list.size();     // Get size - O(1)
        Collections.reverse(list);  // Reverse - O(n)
        Collections.sort(list);     // Sort - O(n log n)
        
        // Convert to array
        Integer[] array = list.toArray(new Integer[0]);
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // Static array
    int staticArray[5] = {1, 2, 3, 4, 5};
    
    // Dynamic vector
    std::vector<int> vec;
    vec.push_back(10);          // Add element - O(1) amortized
    vec.insert(vec.begin(), 5); // Insert at beginning - O(n)
    vec.pop_back();             // Remove last - O(1)
    vec.erase(vec.begin());     // Remove by iterator - O(n)
    
    // Access and modification
    int value = vec[0];         // Access - O(1)
    vec[0] = 100;              // Modify - O(1)
    
    // Safer access with bounds checking
    int safeValue = vec.at(0);
    
    // Useful operations
    int size = vec.size();      // Get size - O(1)
    std::reverse(vec.begin(), vec.end());  // Reverse - O(n)
    std::sort(vec.begin(), vec.end());     // Sort - O(n log n)
    
    return 0;
}
```

## 🔄 Common Operations Complexity

| Operation | Python List | Java ArrayList | C++ Vector |
|-----------|-------------|----------------|------------|
| Access by index | O(1) | O(1) | O(1) |
| Insert at end | O(1)* | O(1)* | O(1)* |
| Insert at beginning | O(n) | O(n) | O(n) |
| Remove from end | O(1) | O(1) | O(1) |
| Remove from beginning | O(n) | O(n) | O(n) |
| Search by value | O(n) | O(n) | O(n) |

*Amortized time complexity

## 🎯 Use Cases

### When to Use Arrays/Lists:
- Need random access to elements
- Frequent access by index
- Cache-friendly sequential access
- When memory efficiency is important

### When NOT to Use:
- Frequent insertions/deletions at beginning
- Unknown maximum size (for static arrays)
- Need constant-time insertions in middle

## 🔗 Related Topics

- [[Linked Lists]] - Alternative dynamic data structure
- [[Dynamic Programming]] - Often uses arrays for memoization
- [[Binary Search]] - Requires sorted arrays
- [[Sorting Algorithms]] - Operate on arrays

## 💡 Tips and Tricks

1. **Python**: Use `collections.deque` for frequent insertions at both ends
2. **Java**: Consider `LinkedList` for frequent insertions/deletions
3. **C++**: Use `std::array` for compile-time fixed size, `std::vector` for dynamic
4. Always consider bounds checking to avoid runtime errors
5. Pre-allocate size if known to avoid frequent resizing

## 📝 Practice Problems

1. **Two Sum**: Find two numbers that add up to target
2. **Maximum Subarray**: Find contiguous subarray with maximum sum
3. **Merge Sorted Arrays**: Merge two sorted arrays
4. **Remove Duplicates**: Remove duplicates from sorted array
5. **Rotate Array**: Rotate array to the right by k steps

---

*See also: [[Time Complexity]], [[Space Complexity]], [[algorithms_and_ds]]*