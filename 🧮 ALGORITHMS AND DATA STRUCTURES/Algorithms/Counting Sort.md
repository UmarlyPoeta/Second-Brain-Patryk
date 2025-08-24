# Counting Sort

> Non-comparison based sorting algorithm that works by counting occurrences of each distinct element, suitable for sorting integers within a known range.

## 📖 Definition

Counting sort works by counting the number of objects having distinct key values, then calculating the position of each object in the output sequence. It's efficient when the range of potential items is not significantly greater than the number of items.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(n + k) where n = number of elements, k = range of input
- **Space Complexity**: O(k) for counting array
- **Stable**: Maintains relative order of equal elements

## 🔑 Key Requirements

- **Integer Keys**: Works with integers or objects with integer keys
- **Known Range**: Range of possible values should be known
- **Small Range**: k should not be significantly larger than n

## 🐍 Python Implementation

```python
def counting_sort(arr):
    """Basic counting sort for non-negative integers"""
    if not arr:
        return arr
    
    # Find range
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    # Count occurrences
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    # Reconstruct sorted array
    result = []
    for i in range(range_size):
        result.extend([i + min_val] * count[i])
    
    return result

def counting_sort_stable(arr):
    """Stable counting sort implementation"""
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    # Count occurrences
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    # Calculate cumulative counts
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    # Build result array
    result = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        result[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return result

def counting_sort_objects(arr, key_func):
    """Counting sort for objects with integer keys"""
    if not arr:
        return arr
    
    # Extract keys and find range
    keys = [key_func(obj) for obj in arr]
    max_key = max(keys)
    min_key = min(keys)
    range_size = max_key - min_key + 1
    
    # Count occurrences
    count = [0] * range_size
    for key in keys:
        count[key - min_key] += 1
    
    # Calculate cumulative counts
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    # Build result array
    result = [None] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        key = key_func(arr[i])
        result[count[key - min_key] - 1] = arr[i]
        count[key - min_key] -= 1
    
    return result

# Example usage
if __name__ == "__main__":
    test_array = [4, 2, 2, 8, 3, 3, 1]
    print("Original array:", test_array)
    
    sorted_array = counting_sort(test_array)
    print("Sorted array:", sorted_array)
```

## ☕ Java Implementation

```java
import java.util.Arrays;

public class CountingSort {
    
    public static int[] countingSort(int[] arr) {
        if (arr.length == 0) return arr;
        
        // Find range
        int max = Arrays.stream(arr).max().getAsInt();
        int min = Arrays.stream(arr).min().getAsInt();
        int range = max - min + 1;
        
        // Count occurrences
        int[] count = new int[range];
        for (int num : arr) {
            count[num - min]++;
        }
        
        // Calculate cumulative counts
        for (int i = 1; i < range; i++) {
            count[i] += count[i - 1];
        }
        
        // Build result array
        int[] result = new int[arr.length];
        for (int i = arr.length - 1; i >= 0; i--) {
            result[count[arr[i] - min] - 1] = arr[i];
            count[arr[i] - min]--;
        }
        
        return result;
    }
    
    public static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        int[] arr = {4, 2, 2, 8, 3, 3, 1};
        
        System.out.println("Original array:");
        printArray(arr);
        
        int[] sorted = countingSort(arr);
        
        System.out.println("Sorted array:");
        printArray(sorted);
    }
}
```

## 🎯 When to Use Counting Sort

✅ **Use Counting Sort when:**
- Range of possible values is small (k ≈ n)
- Dealing with integers or discrete values
- Stable sorting is required
- Linear time sorting is needed

❌ **Don't use when:**
- Range is very large (k >> n)
- Floating-point numbers
- Memory is limited
- Keys are complex objects

## 🆚 Counting Sort vs Comparison Sorts

| Aspect | Counting Sort | Comparison Sorts |
|--------|---------------|------------------|
| **Time Complexity** | O(n + k) | O(n log n) |
| **Space Complexity** | O(k) | O(1) to O(n) |
| **Stability** | Yes | Varies |
| **Input Restriction** | Integer range | Any comparable |
| **Adaptivity** | No | Some are adaptive |

## 💡 Optimizations

1. **Range Reduction**: Use offset to reduce counting array size
2. **Sparse Arrays**: Use hash maps for large sparse ranges
3. **Hybrid Approach**: Combine with comparison sorts

## 🎯 Applications

1. **Radix Sort**: Used as subroutine in radix sort
2. **Suffix Arrays**: Construction algorithms
3. **Histogram Generation**: Frequency counting
4. **Bucket Sort**: As stable sort within buckets

## 🔗 Related Topics

- [[Radix Sort]] - Uses counting sort as subroutine
- [[Bucket Sort]] - Another non-comparison sort
- [[Hash Tables]] - For sparse counting arrays
- [[Heaps]] - Alternative for priority-based sorting

---

*See also: [[Radix Sort]], [[Bucket Sort]], [[algorithms_and_ds]]*