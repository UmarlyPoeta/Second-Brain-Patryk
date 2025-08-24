# Radix Sort

> Non-comparison based sorting algorithm that sorts integers by processing individual digits, using counting sort as a subroutine for each digit position.

## 📖 Definition

Radix sort works by sorting the elements digit by digit, starting from the least significant digit to the most significant digit. It uses counting sort as a subroutine to sort the array according to the current digit being considered.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(d × (n + k)) where d = digits, n = elements, k = range of digits
- **Space Complexity**: O(n + k) for counting sort arrays
- **Stable**: Maintains relative order of equal elements

## 🔑 Key Variants

### LSD (Least Significant Digit)
- Starts from rightmost digit
- Works for fixed-length integers
- Most common implementation

### MSD (Most Significant Digit)
- Starts from leftmost digit
- Can work with variable-length strings
- More complex implementation

## 🐍 Python Implementation

```python
def radix_sort(arr):
    """LSD radix sort for non-negative integers"""
    if not arr:
        return arr
    
    # Find maximum number to know number of digits
    max_num = max(arr)
    
    # Do counting sort for every digit
    exp = 1
    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_by_digit(arr, exp):
    """Counting sort according to digit represented by exp"""
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # For digits 0-9
    
    # Count occurrences of each digit
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1
    
    # Calculate cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    # Copy output array to arr
    for i in range(n):
        arr[i] = output[i]

def radix_sort_with_negatives(arr):
    """Radix sort that handles negative numbers"""
    if not arr:
        return arr
    
    # Separate positive and negative numbers
    positive = [x for x in arr if x >= 0]
    negative = [-x for x in arr if x < 0]
    
    # Sort positive numbers
    if positive:
        radix_sort(positive)
    
    # Sort negative numbers (as positive) and reverse
    if negative:
        radix_sort(negative)
        negative = [-x for x in reversed(negative)]
    
    return negative + positive

def radix_sort_strings(arr):
    """Radix sort for strings of equal length"""
    if not arr or len(arr) == 0:
        return arr
    
    # Assume all strings have same length
    max_len = len(arr[0])
    
    # Sort by each character position from right to left
    for pos in range(max_len - 1, -1, -1):
        # Use counting sort for current character position
        counting_sort_strings(arr, pos)
    
    return arr

def counting_sort_strings(arr, pos):
    """Counting sort for strings by character at position pos"""
    n = len(arr)
    output = [''] * n
    count = [0] * 256  # ASCII characters
    
    # Count occurrences
    for string in arr:
        char_val = ord(string[pos]) if pos < len(string) else 0
        count[char_val] += 1
    
    # Calculate cumulative count
    for i in range(1, 256):
        count[i] += count[i - 1]
    
    # Build output array
    for i in range(n - 1, -1, -1):
        char_val = ord(arr[i][pos]) if pos < len(arr[i]) else 0
        output[count[char_val] - 1] = arr[i]
        count[char_val] -= 1
    
    # Copy back to original array
    for i in range(n):
        arr[i] = output[i]

# Example usage
if __name__ == "__main__":
    # Integer sorting
    test_array = [170, 45, 75, 90, 2, 802, 24, 66]
    print("Original array:", test_array)
    
    sorted_array = radix_sort(test_array.copy())
    print("Sorted array:", sorted_array)
    
    # String sorting
    string_array = ["abc", "def", "ghi", "aaa", "zzz"]
    print("\nOriginal strings:", string_array)
    
    sorted_strings = radix_sort_strings(string_array.copy())
    print("Sorted strings:", sorted_strings)
```

## ☕ Java Implementation

```java
import java.util.Arrays;

public class RadixSort {
    
    public static void radixSort(int[] arr) {
        if (arr.length == 0) return;
        
        // Find maximum number to know number of digits
        int max = Arrays.stream(arr).max().getAsInt();
        
        // Do counting sort for every digit
        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortByDigit(arr, exp);
        }
    }
    
    private static void countingSortByDigit(int[] arr, int exp) {
        int n = arr.length;
        int[] output = new int[n];
        int[] count = new int[10];
        
        // Count occurrences of each digit
        for (int i = 0; i < n; i++) {
            count[(arr[i] / exp) % 10]++;
        }
        
        // Calculate cumulative count
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }
        
        // Build output array
        for (int i = n - 1; i >= 0; i--) {
            output[count[(arr[i] / exp) % 10] - 1] = arr[i];
            count[(arr[i] / exp) % 10]--;
        }
        
        // Copy output array to arr
        System.arraycopy(output, 0, arr, 0, n);
    }
    
    public static void printArray(int[] arr) {
        for (int value : arr) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        int[] arr = {170, 45, 75, 90, 2, 802, 24, 66};
        
        System.out.println("Original array:");
        printArray(arr);
        
        radixSort(arr);
        
        System.out.println("Sorted array:");
        printArray(arr);
    }
}
```

## 🎯 When to Use Radix Sort

✅ **Use Radix Sort when:**
- Sorting integers with small number of digits
- Range of values is not significantly larger than number of elements
- Stable sorting is required
- Linear time complexity is desired

❌ **Don't use when:**
- Floating-point numbers (without preprocessing)
- Very large integers (many digits)
- Memory is limited
- Variable-length data without preprocessing

## 🆚 Radix Sort vs Other Algorithms

| Algorithm | Time | Space | Stable | Input Type |
|-----------|------|-------|--------|------------|
| **Radix Sort** | O(d×n) | O(n+k) | Yes | Integers/Fixed keys |
| **Counting Sort** | O(n+k) | O(k) | Yes | Small range integers |
| **Quick Sort** | O(n log n) | O(log n) | No | Any comparable |
| **Merge Sort** | O(n log n) | O(n) | Yes | Any comparable |

## 💡 Applications

1. **Large Integer Arrays**: Sorting large datasets of integers
2. **String Sorting**: Fixed-length strings (like IDs)
3. **Date/Time Sorting**: Numerical date representations
4. **IP Address Sorting**: 32-bit integer representations

## 🔧 Variations

1. **MSD Radix Sort**: Most significant digit first
2. **Base-k Radix Sort**: Use different bases (not just 10)
3. **String Radix Sort**: For variable-length strings
4. **Parallel Radix Sort**: Distributed sorting

## 🔗 Related Topics

- [[Counting Sort]] - Used as subroutine in radix sort
- [[Bucket Sort]] - Another distribution-based sort
- [[String Algorithms]] - String sorting applications
- [[Hash Tables]] - Alternative for some use cases

---

*See also: [[Counting Sort]], [[Bucket Sort]], [[algorithms_and_ds]]*