# Bubble Sort

> Simple comparison-based sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.

## 📖 Definition

Bubble sort works by repeatedly passing through the list, comparing adjacent elements and swapping them if they're in the wrong order. The pass through the list is repeated until the list is sorted. The algorithm gets its name because smaller elements "bubble" to the beginning of the list.

## ⚡ Time & Space Complexity

- **Best Case**: O(n) - when array is already sorted (with optimization)
- **Average Case**: O(n²) - random order
- **Worst Case**: O(n²) - reverse sorted array
- **Space Complexity**: O(1) - in-place sorting

## 🐍 Python Implementation

```python
def bubble_sort(arr):
    """Basic bubble sort implementation"""
    n = len(arr)
    
    for i in range(n):
        # Track if any swaps occurred
        swapped = False
        
        # Last i elements are already sorted
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps occurred, array is sorted
        if not swapped:
            break
    
    return arr

def bubble_sort_optimized(arr):
    """Optimized version with early termination"""
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        if not swapped:
            break
    
    return arr

# Example usage
if __name__ == "__main__":
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", test_array)
    
    sorted_array = bubble_sort(test_array.copy())
    print("Sorted array:", sorted_array)
```

## ☕ Java Implementation

```java
public class BubbleSort {
    
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            
            // Last i elements are already sorted
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap elements
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }
            
            // If no swapping occurred, array is sorted
            if (!swapped) break;
        }
    }
    
    public static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        
        System.out.println("Original array:");
        printArray(arr);
        
        bubbleSort(arr);
        
        System.out.println("Sorted array:");
        printArray(arr);
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>

class BubbleSort {
public:
    static void bubbleSort(std::vector<int>& arr) {
        int n = arr.size();
        
        for (int i = 0; i < n - 1; i++) {
            bool swapped = false;
            
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    std::swap(arr[j], arr[j + 1]);
                    swapped = true;
                }
            }
            
            if (!swapped) break;
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
    std::vector<int> arr = {64, 34, 25, 12, 22, 11, 90};
    
    std::cout << "Original array: ";
    BubbleSort::printArray(arr);
    
    BubbleSort::bubbleSort(arr);
    
    std::cout << "Sorted array: ";
    BubbleSort::printArray(arr);
    
    return 0;
}
```

## 🎯 When to Use Bubble Sort

✅ **Use Bubble Sort when:**
- Educational purposes (easy to understand)
- Small datasets (n < 50)
- Detecting if list is already sorted
- Memory is extremely limited

❌ **Don't use when:**
- Large datasets (very inefficient)
- Performance is critical
- Production systems

## 🆚 Comparison with Other Sorts

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| **Bubble Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes |
| **Selection Sort** | O(n²) | O(n²) | O(n²) | O(1) | No |
| **Insertion Sort** | O(n) | O(n²) | O(n²) | O(1) | Yes |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |

## 💡 Optimizations

1. **Early Termination**: Stop if no swaps occur in a pass
2. **Cocktail Sort**: Bubble in both directions
3. **Odd-Even Sort**: Parallel version of bubble sort

## 🔗 Related Topics

- [[Selection Sort]] - Another simple O(n²) sorting algorithm
- [[Insertion Sort]] - Similar simplicity, better performance
- [[Merge Sort]] - Efficient divide-and-conquer alternative
- [[Sorting Algorithms]] - Overview of all sorting methods

---

*See also: [[Selection Sort]], [[Insertion Sort]], [[algorithms_and_ds]]*