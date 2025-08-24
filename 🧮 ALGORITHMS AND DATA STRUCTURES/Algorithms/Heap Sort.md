# Heap Sort

> Comparison-based sorting algorithm that uses a binary heap data structure to sort elements efficiently with guaranteed O(n log n) performance.

## 📖 Definition

Heap sort divides its input into a sorted and an unsorted region, and iteratively shrinks the unsorted region by extracting the largest element from it and inserting it into the sorted region. It uses a heap data structure rather than a linear-time search to find the maximum.

## ⚡ Time & Space Complexity

- **Best Case**: O(n log n) - consistent performance
- **Average Case**: O(n log n) - reliable complexity
- **Worst Case**: O(n log n) - guaranteed performance
- **Space Complexity**: O(1) - in-place sorting

## 🔑 Key Steps

1. **Build Max Heap**: Convert array into max heap
2. **Extract Maximum**: Repeatedly extract max and place at end
3. **Heapify**: Maintain heap property after each extraction

## 🐍 Python Implementation

```python
def heap_sort(arr):
    """Main heap sort function"""
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]
        
        # Call heapify on reduced heap
        heapify(arr, i, 0)
    
    return arr

def heapify(arr, n, i):
    """Heapify subtree rooted at index i"""
    largest = i  # Initialize largest as root
    left = 2 * i + 1  # Left child
    right = 2 * i + 2  # Right child
    
    # If left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # If right child exists and is greater than largest so far
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # If largest is not root
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # Recursively heapify affected subtree
        heapify(arr, n, largest)

def heap_sort_iterative(arr):
    """Iterative version of heapify"""
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify_iterative(arr, n, i)
    
    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify_iterative(arr, i, 0)
    
    return arr

def heapify_iterative(arr, n, i):
    """Iterative heapify to avoid recursion"""
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest == i:
            break
        
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest

# Example usage
if __name__ == "__main__":
    test_array = [12, 11, 13, 5, 6, 7]
    print("Original array:", test_array)
    
    sorted_array = heap_sort(test_array.copy())
    print("Sorted array:", sorted_array)
```

## ☕ Java Implementation

```java
public class HeapSort {
    
    public static void heapSort(int[] arr) {
        int n = arr.length;
        
        // Build max heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }
        
        // Extract elements from heap one by one
        for (int i = n - 1; i > 0; i--) {
            // Move current root to end
            int temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;
            
            // Call heapify on reduced heap
            heapify(arr, i, 0);
        }
    }
    
    static void heapify(int[] arr, int n, int i) {
        int largest = i; // Initialize largest as root
        int left = 2 * i + 1; // Left child
        int right = 2 * i + 2; // Right child
        
        // If left child is larger than root
        if (left < n && arr[left] > arr[largest])
            largest = left;
        
        // If right child is larger than largest so far
        if (right < n && arr[right] > arr[largest])
            largest = right;
        
        // If largest is not root
        if (largest != i) {
            int swap = arr[i];
            arr[i] = arr[largest];
            arr[largest] = swap;
            
            // Recursively heapify affected subtree
            heapify(arr, n, largest);
        }
    }
    
    public static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        int[] arr = {12, 11, 13, 5, 6, 7};
        
        System.out.println("Original array:");
        printArray(arr);
        
        heapSort(arr);
        
        System.out.println("Sorted array:");
        printArray(arr);
    }
}
```

## 🎯 Applications

1. **Priority Queues**: Natural heap-based implementation
2. **k-th largest/smallest**: Find k-th element efficiently
3. **Memory-constrained environments**: O(1) space complexity
4. **Real-time systems**: Predictable O(n log n) performance

## 🆚 Heap Sort vs Other Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |

## 💡 Key Advantages

1. **Guaranteed Performance**: Always O(n log n)
2. **In-place**: Constant space complexity
3. **Not Recursive**: Can be implemented iteratively
4. **Heap Structure**: Useful for priority queue operations

## 🔗 Related Topics

- [[Heaps]] - Underlying data structure
- [[Binary Trees]] - Heap is a complete binary tree
- [[Quick Sort]] - Another O(n log n) algorithm
- [[Merge Sort]] - Stable alternative with O(n) space

---

*See also: [[Heaps]], [[Quick Sort]], [[algorithms_and_ds]]*