# Quick Sort

> Fast, in-place, divide-and-conquer sorting algorithm that works by selecting a 'pivot' element and partitioning the array around it.

## 📖 Definition

Quick Sort is a highly efficient sorting algorithm that uses the divide-and-conquer strategy. It picks a pivot element and rearranges the array so that elements smaller than the pivot come before it, and elements greater come after it.

## 🎯 Algorithm Steps

1. **Choose Pivot**: Select an element as pivot (first, last, middle, or random)
2. **Partition**: Rearrange array so smaller elements are left of pivot, larger on right
3. **Recursively Sort**: Apply quicksort to left and right subarrays
4. **Combine**: No explicit combine step needed (sorted in-place)

## ⚡ Time Complexity

- **Best Case**: O(n log n) - balanced partitions
- **Average Case**: O(n log n) - random pivots
- **Worst Case**: O(n²) - already sorted with first/last pivot
- **Space Complexity**: O(log n) average, O(n) worst case (recursion stack)

## 🐍 Python Implementation

```python
def quicksort_basic(arr):
    """
    Simple quicksort implementation (not in-place)
    Easy to understand but uses extra space
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort_basic(left) + middle + quicksort_basic(right)

def quicksort_inplace(arr, low=0, high=None):
    """
    In-place quicksort implementation
    More memory efficient
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition and get pivot index
        pivot_index = partition(arr, low, high)
        
        # Recursively sort elements before and after partition
        quicksort_inplace(arr, low, pivot_index - 1)
        quicksort_inplace(arr, pivot_index + 1, high)

def partition(arr, low, high):
    """
    Lomuto partition scheme
    Takes last element as pivot
    """
    pivot = arr[high]
    i = low - 1  # Index of smaller element
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def partition_hoare(arr, low, high):
    """
    Hoare partition scheme (original)
    More efficient than Lomuto
    """
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        # Find element >= pivot from left
        i += 1
        while arr[i] < pivot:
            i += 1
        
        # Find element <= pivot from right
        j -= 1
        while arr[j] > pivot:
            j -= 1
        
        # If pointers crossed, partitioning is done
        if i >= j:
            return j
        
        # Swap elements
        arr[i], arr[j] = arr[j], arr[i]

def quicksort_hoare(arr, low=0, high=None):
    """Quicksort using Hoare partition"""
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_index = partition_hoare(arr, low, high)
        quicksort_hoare(arr, low, pivot_index)
        quicksort_hoare(arr, pivot_index + 1, high)

def quicksort_random_pivot(arr, low=0, high=None):
    """
    Quicksort with random pivot selection
    Helps avoid worst-case performance
    """
    import random
    
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Choose random pivot and swap with last element
        random_index = random.randint(low, high)
        arr[random_index], arr[high] = arr[high], arr[random_index]
        
        pivot_index = partition(arr, low, high)
        
        quicksort_random_pivot(arr, low, pivot_index - 1)
        quicksort_random_pivot(arr, pivot_index + 1, high)

def quicksort_iterative(arr):
    """
    Iterative quicksort using stack
    Avoids recursion depth issues
    """
    if len(arr) <= 1:
        return
    
    stack = [(0, len(arr) - 1)]
    
    while stack:
        low, high = stack.pop()
        
        if low < high:
            pivot_index = partition(arr, low, high)
            
            # Push left and right subarrays onto stack
            stack.append((low, pivot_index - 1))
            stack.append((pivot_index + 1, high))

def quickselect(arr, k, low=0, high=None):
    """
    Find k-th smallest element using quickselect algorithm
    Average O(n) time complexity
    """
    if high is None:
        high = len(arr) - 1
    
    if low == high:
        return arr[low]
    
    pivot_index = partition(arr, low, high)
    
    if k == pivot_index:
        return arr[k]
    elif k < pivot_index:
        return quickselect(arr, k, low, pivot_index - 1)
    else:
        return quickselect(arr, k, pivot_index + 1, high)

# Example usage and testing
def test_quicksort():
    import random
    
    # Test cases
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 8, 6, 1, 9, 4],
        [1],  # Single element
        [],   # Empty array
        [3, 3, 3, 3],  # All same elements
        [5, 4, 3, 2, 1],  # Reverse sorted
        [1, 2, 3, 4, 5]   # Already sorted
    ]
    
    for i, arr in enumerate(test_arrays):
        if arr:  # Skip empty array for some tests
            original = arr.copy()
            
            # Test basic quicksort
            result1 = quicksort_basic(arr.copy())
            
            # Test in-place quicksort
            arr_copy = arr.copy()
            quicksort_inplace(arr_copy)
            
            # Test random pivot
            arr_copy2 = arr.copy()
            quicksort_random_pivot(arr_copy2)
            
            print(f"Test {i+1}:")
            print(f"Original: {original}")
            print(f"Sorted:   {result1}")
            print(f"In-place: {arr_copy}")
            print(f"Random:   {arr_copy2}")
            print(f"Built-in: {sorted(original)}")
            print()
```

## ☕ Java Implementation

```java
import java.util.*;

public class QuickSort {
    
    // Basic quicksort implementation
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    // Lomuto partition scheme
    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        
        swap(arr, i + 1, high);
        return i + 1;
    }
    
    // Hoare partition scheme
    private static int hoarePartition(int[] arr, int low, int high) {
        int pivot = arr[low];
        int i = low - 1;
        int j = high + 1;
        
        while (true) {
            do {
                i++;
            } while (arr[i] < pivot);
            
            do {
                j--;
            } while (arr[j] > pivot);
            
            if (i >= j) {
                return j;
            }
            
            swap(arr, i, j);
        }
    }
    
    // Quicksort with random pivot
    public static void quickSortRandomPivot(int[] arr, int low, int high) {
        if (low < high) {
            // Random pivot selection
            Random rand = new Random();
            int randomIndex = low + rand.nextInt(high - low + 1);
            swap(arr, randomIndex, high);
            
            int pivotIndex = partition(arr, low, high);
            
            quickSortRandomPivot(arr, low, pivotIndex - 1);
            quickSortRandomPivot(arr, pivotIndex + 1, high);
        }
    }
    
    // 3-way quicksort (handles duplicates efficiently)
    public static void quickSort3Way(int[] arr, int low, int high) {
        if (low >= high) return;
        
        int pivot = arr[low];
        int lt = low;      // arr[low..lt-1] < pivot
        int gt = high;     // arr[gt+1..high] > pivot
        int i = low + 1;   // arr[lt..i-1] == pivot
        
        while (i <= gt) {
            if (arr[i] < pivot) {
                swap(arr, lt++, i++);
            } else if (arr[i] > pivot) {
                swap(arr, i, gt--);
            } else {
                i++;
            }
        }
        
        quickSort3Way(arr, low, lt - 1);
        quickSort3Way(arr, gt + 1, high);
    }
    
    // Iterative quicksort
    public static void quickSortIterative(int[] arr) {
        if (arr.length <= 1) return;
        
        Stack<int[]> stack = new Stack<>();
        stack.push(new int[]{0, arr.length - 1});
        
        while (!stack.isEmpty()) {
            int[] bounds = stack.pop();
            int low = bounds[0];
            int high = bounds[1];
            
            if (low < high) {
                int pivotIndex = partition(arr, low, high);
                
                stack.push(new int[]{low, pivotIndex - 1});
                stack.push(new int[]{pivotIndex + 1, high});
            }
        }
    }
    
    // Quickselect - find k-th smallest element
    public static int quickSelect(int[] arr, int k) {
        return quickSelect(arr, 0, arr.length - 1, k - 1);
    }
    
    private static int quickSelect(int[] arr, int low, int high, int k) {
        if (low == high) {
            return arr[low];
        }
        
        int pivotIndex = partition(arr, low, high);
        
        if (k == pivotIndex) {
            return arr[k];
        } else if (k < pivotIndex) {
            return quickSelect(arr, low, pivotIndex - 1, k);
        } else {
            return quickSelect(arr, pivotIndex + 1, high, k);
        }
    }
    
    // Utility method to swap elements
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    // Public interface methods
    public static void sort(int[] arr) {
        if (arr.length > 1) {
            quickSort(arr, 0, arr.length - 1);
        }
    }
    
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        System.out.println("Original: " + Arrays.toString(arr));
        
        int[] copy1 = arr.clone();
        quickSort(copy1, 0, copy1.length - 1);
        System.out.println("Quick Sort: " + Arrays.toString(copy1));
        
        int[] copy2 = arr.clone();
        quickSortRandomPivot(copy2, 0, copy2.length - 1);
        System.out.println("Random Pivot: " + Arrays.toString(copy2));
        
        int[] copy3 = arr.clone();
        quickSort3Way(copy3, 0, copy3.length - 1);
        System.out.println("3-Way: " + Arrays.toString(copy3));
        
        // Test quickselect
        int[] copy4 = arr.clone();
        int kthSmallest = quickSelect(copy4, 3);
        System.out.println("3rd smallest element: " + kthSmallest);
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <stack>
#include <random>
#include <algorithm>

class QuickSort {
public:
    // Basic quicksort
    static void quickSort(std::vector<int>& arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    // Lomuto partition
    static int partition(std::vector<int>& arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                std::swap(arr[i], arr[j]);
            }
        }
        
        std::swap(arr[i + 1], arr[high]);
        return i + 1;
    }
    
    // Hoare partition
    static int hoarePartition(std::vector<int>& arr, int low, int high) {
        int pivot = arr[low];
        int i = low - 1;
        int j = high + 1;
        
        while (true) {
            do {
                i++;
            } while (arr[i] < pivot);
            
            do {
                j--;
            } while (arr[j] > pivot);
            
            if (i >= j) {
                return j;
            }
            
            std::swap(arr[i], arr[j]);
        }
    }
    
    // Random pivot quicksort
    static void quickSortRandomPivot(std::vector<int>& arr, int low, int high) {
        if (low < high) {
            // Generate random pivot
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> dis(low, high);
            int randomIndex = dis(gen);
            
            std::swap(arr[randomIndex], arr[high]);
            
            int pivotIndex = partition(arr, low, high);
            
            quickSortRandomPivot(arr, low, pivotIndex - 1);
            quickSortRandomPivot(arr, pivotIndex + 1, high);
        }
    }
    
    // 3-way quicksort for handling duplicates
    static void quickSort3Way(std::vector<int>& arr, int low, int high) {
        if (low >= high) return;
        
        int pivot = arr[low];
        int lt = low;      // arr[low..lt-1] < pivot
        int gt = high;     // arr[gt+1..high] > pivot
        int i = low + 1;   // arr[lt..i-1] == pivot
        
        while (i <= gt) {
            if (arr[i] < pivot) {
                std::swap(arr[lt++], arr[i++]);
            } else if (arr[i] > pivot) {
                std::swap(arr[i], arr[gt--]);
            } else {
                i++;
            }
        }
        
        quickSort3Way(arr, low, lt - 1);
        quickSort3Way(arr, gt + 1, high);
    }
    
    // Iterative quicksort
    static void quickSortIterative(std::vector<int>& arr) {
        if (arr.size() <= 1) return;
        
        std::stack<std::pair<int, int>> stack;
        stack.push({0, static_cast<int>(arr.size()) - 1});
        
        while (!stack.empty()) {
            auto [low, high] = stack.top();
            stack.pop();
            
            if (low < high) {
                int pivotIndex = partition(arr, low, high);
                
                stack.push({low, pivotIndex - 1});
                stack.push({pivotIndex + 1, high});
            }
        }
    }
    
    // Quickselect algorithm
    static int quickSelect(std::vector<int>& arr, int k) {
        return quickSelectHelper(arr, 0, arr.size() - 1, k - 1);
    }
    
private:
    static int quickSelectHelper(std::vector<int>& arr, int low, int high, int k) {
        if (low == high) {
            return arr[low];
        }
        
        int pivotIndex = partition(arr, low, high);
        
        if (k == pivotIndex) {
            return arr[k];
        } else if (k < pivotIndex) {
            return quickSelectHelper(arr, low, pivotIndex - 1, k);
        } else {
            return quickSelectHelper(arr, pivotIndex + 1, high, k);
        }
    }
    
public:
    // Public interface
    static void sort(std::vector<int>& arr) {
        if (arr.size() > 1) {
            quickSort(arr, 0, arr.size() - 1);
        }
    }
};

// Example usage
int main() {
    std::vector<int> arr = {64, 34, 25, 12, 22, 11, 90};
    
    std::cout << "Original: ";
    for (int x : arr) std::cout << x << " ";
    std::cout << std::endl;
    
    // Test regular quicksort
    auto copy1 = arr;
    QuickSort::sort(copy1);
    std::cout << "Quick Sort: ";
    for (int x : copy1) std::cout << x << " ";
    std::cout << std::endl;
    
    // Test random pivot
    auto copy2 = arr;
    QuickSort::quickSortRandomPivot(copy2, 0, copy2.size() - 1);
    std::cout << "Random Pivot: ";
    for (int x : copy2) std::cout << x << " ";
    std::cout << std::endl;
    
    // Test STL sort (typically uses introsort - hybrid of quicksort, heapsort, insertion sort)
    auto copy3 = arr;
    std::sort(copy3.begin(), copy3.end());
    std::cout << "STL Sort: ";
    for (int x : copy3) std::cout << x << " ";
    std::cout << std::endl;
    
    // Test quickselect
    auto copy4 = arr;
    int kthSmallest = QuickSort::quickSelect(copy4, 3);
    std::cout << "3rd smallest element: " << kthSmallest << std::endl;
    
    return 0;
}
```

## 🔄 Partition Schemes Comparison

| Scheme | Complexity | Pros | Cons |
|--------|------------|------|------|
| **Lomuto** | Same | Easier to understand | More swaps |
| **Hoare** | Same | Fewer swaps, faster | More complex |
| **3-Way** | Better for duplicates | Handles duplicates well | More complex |

## 🎯 Optimizations

### 1. Pivot Selection
```python
# Median-of-three pivot
def median_of_three_pivot(arr, low, high):
    mid = (low + high) // 2
    if arr[mid] < arr[low]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[high] < arr[low]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[high] < arr[mid]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    # Move median to end
    arr[mid], arr[high] = arr[high], arr[mid]
```

### 2. Hybrid with Insertion Sort
```python
def quicksort_hybrid(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    THRESHOLD = 10
    
    if high - low + 1 < THRESHOLD:
        insertion_sort(arr, low, high)
    elif low < high:
        pivot_index = partition(arr, low, high)
        quicksort_hybrid(arr, low, pivot_index - 1)
        quicksort_hybrid(arr, pivot_index + 1, high)
```

## 🆚 Comparison with Other Sorts

| Algorithm | Time (Avg) | Time (Worst) | Space | Stable |
|-----------|------------|---------------|-------|---------|
| **Quick Sort** | O(n log n) | O(n²) | O(log n) | No |
| **Merge Sort** | O(n log n) | O(n log n) | O(n) | Yes |
| **Heap Sort** | O(n log n) | O(n log n) | O(1) | No |
| **Bubble Sort** | O(n²) | O(n²) | O(1) | Yes |

## 🎯 Applications

1. **General-purpose sorting**: Most library implementations
2. **Quickselect**: Finding k-th order statistics
3. **In-place sorting**: When memory is limited
4. **Large datasets**: Good cache performance

## 💡 Tips and Best Practices

1. **Avoid worst case**: Use random or median-of-three pivot
2. **Handle duplicates**: Consider 3-way partitioning
3. **Small arrays**: Switch to insertion sort for small subarrays
4. **Stack overflow**: Use iterative version for large inputs
5. **Stable sorting**: Use merge sort if stability is required

## 📝 Practice Problems

1. **Kth Largest Element**: Find k-th largest using quickselect
2. **Sort Colors**: Dutch national flag problem (3-way partitioning)
3. **Nuts and Bolts**: Match nuts and bolts using quicksort idea
4. **Quick Sort on Linked List**: Adapt quicksort for linked lists
5. **Find Median**: Use quickselect to find median efficiently

## 🔗 Related Topics

- [[Merge Sort]] - Stable O(n log n) alternative
- [[Heap Sort]] - Another O(n log n) comparison sort
- [[Binary Search]] - Both use divide-and-conquer
- [[Sorting Algorithms]] - Overview of all sorting methods

---

*See also: [[Merge Sort]], [[Heap Sort]], [[Sorting Algorithms]], [[algorithms_and_ds]]*