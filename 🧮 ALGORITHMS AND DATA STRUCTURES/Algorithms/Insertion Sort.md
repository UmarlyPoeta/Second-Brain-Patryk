# Insertion Sort

> Efficient algorithm for sorting small datasets that builds the sorted array one element at a time by inserting each element into its correct position.

## 📖 Definition

Insertion sort works by iterating through the array and for each element, finding the correct position in the already-sorted portion and inserting it there. It's similar to how people sort playing cards in their hands.

## ⚡ Time & Space Complexity

- **Best Case**: O(n) - when array is already sorted
- **Average Case**: O(n²) - random order
- **Worst Case**: O(n²) - reverse sorted array
- **Space Complexity**: O(1) - in-place sorting

## 🐍 Python Implementation

```python
def insertion_sort(arr):
    """Basic insertion sort implementation"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insert key at correct position
        arr[j + 1] = key
    
    return arr

def insertion_sort_recursive(arr, n=None):
    """Recursive insertion sort"""
    if n is None:
        n = len(arr)
    
    # Base case
    if n <= 1:
        return
    
    # Sort first n-1 elements
    insertion_sort_recursive(arr, n - 1)
    
    # Insert last element at correct position
    last = arr[n - 1]
    j = n - 2
    
    while j >= 0 and arr[j] > last:
        arr[j + 1] = arr[j]
        j -= 1
    
    arr[j + 1] = last

def binary_insertion_sort(arr):
    """Insertion sort with binary search for position"""
    import bisect
    
    for i in range(1, len(arr)):
        key = arr[i]
        # Find position using binary search
        pos = bisect.bisect_left(arr, key, 0, i)
        # Shift elements and insert
        arr[pos + 1:i + 1] = arr[pos:i]
        arr[pos] = key
    
    return arr

# Example usage
if __name__ == "__main__":
    test_array = [12, 11, 13, 5, 6]
    print("Original array:", test_array)
    
    sorted_array = insertion_sort(test_array.copy())
    print("Sorted array:", sorted_array)
```

## ☕ Java Implementation

```java
public class InsertionSort {
    
    public static void insertionSort(int[] arr) {
        int n = arr.length;
        
        for (int i = 1; i < n; i++) {
            int key = arr[i];
            int j = i - 1;
            
            // Move elements greater than key one position ahead
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j = j - 1;
            }
            
            arr[j + 1] = key;
        }
    }
    
    public static void insertionSortRecursive(int[] arr, int n) {
        // Base case
        if (n <= 1) return;
        
        // Sort first n-1 elements
        insertionSortRecursive(arr, n - 1);
        
        // Insert last element at correct position
        int last = arr[n - 1];
        int j = n - 2;
        
        while (j >= 0 && arr[j] > last) {
            arr[j + 1] = arr[j];
            j--;
        }
        
        arr[j + 1] = last;
    }
    
    public static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        int[] arr = {12, 11, 13, 5, 6};
        
        System.out.println("Original array:");
        printArray(arr);
        
        insertionSort(arr);
        
        System.out.println("Sorted array:");
        printArray(arr);
    }
}
```

## 🎯 When to Use Insertion Sort

✅ **Use Insertion Sort when:**
- Small datasets (n < 50)
- Array is nearly sorted
- Online algorithm needed (sorts as data arrives)
- Stable sorting required
- Simple implementation needed

❌ **Don't use when:**
- Large datasets
- Random data (poor performance)
- Memory access is expensive

## 🆚 Insertion Sort Advantages

1. **Adaptive**: Efficient for data sets that are already substantially sorted
2. **Stable**: Maintains relative order of equal elements
3. **In-place**: Only requires O(1) additional memory
4. **Online**: Can sort a list as it receives it
5. **Simple**: Easy to implement and understand

## 🔧 Variants

1. **Binary Insertion Sort**: Use binary search to find insertion position
2. **Shell Sort**: Generalization with gap sequences
3. **Library Sort**: With gaps for better performance

## 🔗 Related Topics

- [[Bubble Sort]] - Another simple O(n²) algorithm
- [[Selection Sort]] - Similar complexity, different approach
- [[Shell Sort]] - Improved version of insertion sort
- [[Binary Search]] - Used in binary insertion sort variant

---

*See also: [[Bubble Sort]], [[Selection Sort]], [[algorithms_and_ds]]*