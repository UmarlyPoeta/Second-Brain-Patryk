# Merge Sort

> Stable, divide-and-conquer sorting algorithm that consistently performs in O(n log n) time by recursively dividing arrays and merging sorted subarrays.

## 📖 Definition

Merge Sort divides the array into two halves, recursively sorts each half, then merges the sorted halves back together. It guarantees O(n log n) time complexity in all cases.

## 🎯 Algorithm Steps

1. **Divide**: Split array into two halves
2. **Conquer**: Recursively sort each half
3. **Combine**: Merge the two sorted halves

## ⚡ Time Complexity

- **Best Case**: O(n log n)
- **Average Case**: O(n log n)
- **Worst Case**: O(n log n)
- **Space Complexity**: O(n) - requires additional space for merging

## 🐍 Python Implementation

```python
def merge_sort(arr):
    """
    Merge sort implementation
    Returns new sorted array
    """
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    # Combine
    return merge(left_half, right_half)

def merge(left, right):
    """Merge two sorted arrays"""
    result = []
    i = j = 0
    
    # Compare elements and merge in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def merge_sort_inplace(arr, left=0, right=None):
    """In-place merge sort (still uses O(n) auxiliary space for merging)"""
    if right is None:
        right = len(arr) - 1
    
    if left < right:
        mid = left + (right - left) // 2
        
        # Recursively sort halves
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        
        # Merge sorted halves
        merge_inplace(arr, left, mid, right)

def merge_inplace(arr, left, mid, right):
    """Merge two sorted subarrays in-place"""
    # Create temporary arrays for left and right subarrays
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    # Merge back into original array
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    # Copy remaining elements
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

def merge_sort_iterative(arr):
    """Iterative merge sort (bottom-up approach)"""
    if len(arr) <= 1:
        return arr
    
    arr = arr.copy()
    size = 1
    
    while size < len(arr):
        # Merge subarrays of current size
        for start in range(0, len(arr), 2 * size):
            mid = min(start + size, len(arr))
            end = min(start + 2 * size, len(arr))
            
            if mid < end:
                merge_iterative(arr, start, mid - 1, end - 1)
        
        size *= 2
    
    return arr

def merge_iterative(arr, left, mid, right):
    """Helper function for iterative merge"""
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

# Example usage and testing
def test_merge_sort():
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 6, 1, 9, 4],
        [1],  # Single element
        [],   # Empty array
        [3, 3, 3, 3],  # All same elements
        [5, 4, 3, 2, 1],  # Reverse sorted
        [1, 2, 3, 4, 5]   # Already sorted
    ]
    
    for i, arr in enumerate(test_cases):
        original = arr.copy()
        
        # Test different implementations
        result1 = merge_sort(arr.copy())
        
        arr_copy = arr.copy()
        merge_sort_inplace(arr_copy)
        
        result3 = merge_sort_iterative(arr.copy())
        
        print(f"Test {i+1}:")
        print(f"Original: {original}")
        print(f"Merge Sort: {result1}")
        print(f"In-place: {arr_copy}")
        print(f"Iterative: {result3}")
        print(f"Built-in: {sorted(original)}")
        print()

if __name__ == "__main__":
    test_merge_sort()
```

## ☕ Java Implementation

```java
import java.util.Arrays;

public class MergeSort {
    
    public static void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        mergeSort(arr, 0, arr.length - 1);
    }
    
    private static void mergeSort(int[] arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            
            // Recursively sort halves
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);
            
            // Merge sorted halves
            merge(arr, left, mid, right);
        }
    }
    
    private static void merge(int[] arr, int left, int mid, int right) {
        // Create temporary arrays
        int[] leftArr = new int[mid - left + 1];
        int[] rightArr = new int[right - mid];
        
        // Copy data to temporary arrays
        System.arraycopy(arr, left, leftArr, 0, leftArr.length);
        System.arraycopy(arr, mid + 1, rightArr, 0, rightArr.length);
        
        // Merge the temporary arrays back
        int i = 0, j = 0, k = left;
        
        while (i < leftArr.length && j < rightArr.length) {
            if (leftArr[i] <= rightArr[j]) {
                arr[k++] = leftArr[i++];
            } else {
                arr[k++] = rightArr[j++];
            }
        }
        
        // Copy remaining elements
        while (i < leftArr.length) {
            arr[k++] = leftArr[i++];
        }
        
        while (j < rightArr.length) {
            arr[k++] = rightArr[j++];
        }
    }
    
    // Iterative merge sort
    public static void mergeSortIterative(int[] arr) {
        int n = arr.length;
        
        for (int size = 1; size < n; size *= 2) {
            for (int start = 0; start < n - 1; start += 2 * size) {
                int mid = Math.min(start + size - 1, n - 1);
                int end = Math.min(start + 2 * size - 1, n - 1);
                
                if (mid < end) {
                    merge(arr, start, mid, end);
                }
            }
        }
    }
    
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Original: " + Arrays.toString(arr));
        
        int[] copy1 = arr.clone();
        mergeSort(copy1);
        System.out.println("Merge Sort: " + Arrays.toString(copy1));
        
        int[] copy2 = arr.clone();
        mergeSortIterative(copy2);
        System.out.println("Iterative: " + Arrays.toString(copy2));
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

class MergeSort {
public:
    static void mergeSort(std::vector<int>& arr) {
        if (arr.size() <= 1) return;
        mergeSort(arr, 0, arr.size() - 1);
    }
    
private:
    static void mergeSort(std::vector<int>& arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);
            
            merge(arr, left, mid, right);
        }
    }
    
    static void merge(std::vector<int>& arr, int left, int mid, int right) {
        // Create temporary vectors
        std::vector<int> leftArr(arr.begin() + left, arr.begin() + mid + 1);
        std::vector<int> rightArr(arr.begin() + mid + 1, arr.begin() + right + 1);
        
        int i = 0, j = 0, k = left;
        
        // Merge the temporary vectors back
        while (i < leftArr.size() && j < rightArr.size()) {
            if (leftArr[i] <= rightArr[j]) {
                arr[k++] = leftArr[i++];
            } else {
                arr[k++] = rightArr[j++];
            }
        }
        
        // Copy remaining elements
        while (i < leftArr.size()) {
            arr[k++] = leftArr[i++];
        }
        
        while (j < rightArr.size()) {
            arr[k++] = rightArr[j++];
        }
    }
    
public:
    // Iterative merge sort
    static void mergeSortIterative(std::vector<int>& arr) {
        int n = arr.size();
        
        for (int size = 1; size < n; size *= 2) {
            for (int start = 0; start < n - 1; start += 2 * size) {
                int mid = std::min(start + size - 1, n - 1);
                int end = std::min(start + 2 * size - 1, n - 1);
                
                if (mid < end) {
                    merge(arr, start, mid, end);
                }
            }
        }
    }
};

int main() {
    std::vector<int> arr = {64, 34, 25, 12, 22, 11, 90};
    
    std::cout << "Original: ";
    for (int x : arr) std::cout << x << " ";
    std::cout << std::endl;
    
    auto copy1 = arr;
    MergeSort::mergeSort(copy1);
    std::cout << "Merge Sort: ";
    for (int x : copy1) std::cout << x << " ";
    std::cout << std::endl;
    
    auto copy2 = arr;
    MergeSort::mergeSortIterative(copy2);
    std::cout << "Iterative: ";
    for (int x : copy2) std::cout << x << " ";
    std::cout << std::endl;
    
    // Using STL sort (typically introsort - hybrid algorithm)
    auto copy3 = arr;
    std::sort(copy3.begin(), copy3.end());
    std::cout << "STL Sort: ";
    for (int x : copy3) std::cout << x << " ";
    std::cout << std::endl;
    
    return 0;
}
```

## 🎯 Applications

### 1. External Sorting
When data doesn't fit in memory, merge sort is ideal for sorting large files.

### 2. Stable Sorting
Maintains relative order of equal elements - important for complex objects.

### 3. Parallel Processing
Easy to parallelize - sort halves on different processors.

### 4. Inversion Count
Count inversions (pairs where arr[i] > arr[j] and i < j):

```python
def merge_and_count(left, right):
    """Merge and count inversions"""
    result = []
    i = j = inv_count = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            inv_count += len(left) - i  # All remaining in left are > right[j]
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result, inv_count

def count_inversions(arr):
    """Count inversions using merge sort"""
    if len(arr) <= 1:
        return arr, 0
    
    mid = len(arr) // 2
    left, left_inv = count_inversions(arr[:mid])
    right, right_inv = count_inversions(arr[mid:])
    
    merged, merge_inv = merge_and_count(left, right)
    
    return merged, left_inv + right_inv + merge_inv
```

## 🆚 Comparison with Other Sorts

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|--------|---------|
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes |

## 💡 Advantages and Disadvantages

### ✅ Advantages
- **Consistent O(n log n)**: No worst-case degradation
- **Stable**: Preserves relative order of equal elements
- **Predictable**: Performance doesn't depend on input distribution
- **Parallelizable**: Easy to implement in parallel
- **External sorting**: Works well for large datasets

### ❌ Disadvantages  
- **Space complexity**: Requires O(n) additional space
- **Not in-place**: Unlike heap sort or quick sort
- **Overhead**: Constant factors higher than quick sort
- **Not adaptive**: Doesn't take advantage of existing order

## 🔗 Related Topics

- [[Quick Sort]] - Faster average case but unstable
- [[Heap Sort]] - In-place O(n log n) alternative  
- [[Divide and Conquer]] - Merge sort exemplifies this paradigm
- [[Sorting Algorithms]] - Overview of all sorting methods

## 📝 Practice Problems

1. **Sort Linked List**: Merge sort on linked list (O(1) space)
2. **Merge K Sorted Arrays**: Extend merge to k arrays
3. **Count Smaller Numbers**: Count elements smaller than current
4. **Reverse Pairs**: Count pairs where arr[i] > 2*arr[j] and i < j
5. **Sort Colors**: Dutch national flag (different approach)

---

*See also: [[Quick Sort]], [[Heap Sort]], [[Divide and Conquer]], [[algorithms_and_ds]]*