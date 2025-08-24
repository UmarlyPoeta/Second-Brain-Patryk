# Selection Sort

> In-place comparison-based sorting algorithm that divides the input list into sorted and unsorted regions, repeatedly selecting the smallest element from the unsorted region.

## 📖 Definition

Selection sort works by finding the minimum element from the unsorted portion of the array and placing it at the beginning. This process is repeated for the remaining unsorted portion until the entire array is sorted.

## ⚡ Time & Space Complexity

- **Best Case**: O(n²) - even if array is sorted, all comparisons are made
- **Average Case**: O(n²) - random order
- **Worst Case**: O(n²) - reverse sorted array
- **Space Complexity**: O(1) - in-place sorting

## 🐍 Python Implementation

```python
def selection_sort(arr):
    """Basic selection sort implementation"""
    n = len(arr)
    
    for i in range(n):
        # Find minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap found minimum with first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr

def selection_sort_with_steps(arr):
    """Selection sort with step-by-step visualization"""
    n = len(arr)
    
    print(f"Original array: {arr}")
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap if needed
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            print(f"Step {i + 1}: {arr} (swapped {arr[i]} to position {i})")
    
    return arr

# Example usage
if __name__ == "__main__":
    test_array = [64, 25, 12, 22, 11]
    print("Original array:", test_array)
    
    sorted_array = selection_sort(test_array.copy())
    print("Sorted array:", sorted_array)
```

## ☕ Java Implementation

```java
public class SelectionSort {
    
    public static void selectionSort(int[] arr) {
        int n = arr.length;
        
        for (int i = 0; i < n - 1; i++) {
            // Find minimum element in remaining array
            int minIndex = i;
            
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            
            // Swap minimum element with first element
            if (minIndex != i) {
                int temp = arr[minIndex];
                arr[minIndex] = arr[i];
                arr[i] = temp;
            }
        }
    }
    
    public static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        int[] arr = {64, 25, 12, 22, 11};
        
        System.out.println("Original array:");
        printArray(arr);
        
        selectionSort(arr);
        
        System.out.println("Sorted array:");
        printArray(arr);
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

class SelectionSort {
public:
    static void selectionSort(std::vector<int>& arr) {
        int n = arr.size();
        
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;
            
            // Find minimum element in remaining array
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            
            // Swap if needed
            if (minIndex != i) {
                std::swap(arr[i], arr[minIndex]);
            }
        }
    }
    
    static void printArray(const std::vector<int>& arr) {
        for (int val : arr) {
            std::cout << val << " ";
        }
        std::cout << std::endl;
    }
};

int main() {
    std::vector<int> arr = {64, 25, 12, 22, 11};
    
    std::cout << "Original array: ";
    SelectionSort::printArray(arr);
    
    SelectionSort::selectionSort(arr);
    
    std::cout << "Sorted array: ";
    SelectionSort::printArray(arr);
    
    return 0;
}
```

## 🎯 When to Use Selection Sort

✅ **Use Selection Sort when:**
- Small datasets (n < 50)
- Memory writes are expensive (fewer swaps than bubble sort)
- Simple implementation needed
- Educational purposes

❌ **Don't use when:**
- Large datasets
- Stable sorting is required
- Performance is critical

## 🆚 Selection vs Other Simple Sorts

| Aspect | Selection Sort | Bubble Sort | Insertion Sort |
|--------|----------------|-------------|----------------|
| **Comparisons** | O(n²) | O(n²) | O(n²) |
| **Swaps** | O(n) | O(n²) | O(n²) |
| **Stability** | No | Yes | Yes |
| **Best Case** | O(n²) | O(n) | O(n) |
| **Memory Writes** | Minimal | Many | Many |

## 💡 Key Insights

1. **Fewer Swaps**: Only n-1 swaps maximum (one per position)
2. **Not Adaptive**: Doesn't improve on partially sorted arrays
3. **Not Stable**: Relative order of equal elements may change
4. **Predictable**: Always makes same number of comparisons

## 🔗 Related Topics

- [[Bubble Sort]] - Similar simple sorting algorithm
- [[Insertion Sort]] - Another O(n²) sorting method
- [[Heap Sort]] - Selection sort with heap optimization
- [[Sorting Algorithms]] - Overview of all sorting methods

---

*See also: [[Bubble Sort]], [[Insertion Sort]], [[algorithms_and_ds]]*