# Linear Search

> Simple search algorithm that checks every element in a collection sequentially until the target is found or all elements have been examined.

## 📖 Definition

Linear search (sequential search) is the simplest searching algorithm that traverses through each element one by one until the target element is found or the end of the collection is reached.

## ⚡ Time Complexity

- **Best Case**: O(1) - target is first element
- **Average Case**: O(n) - target is in middle on average  
- **Worst Case**: O(n) - target is last element or not present
- **Space Complexity**: O(1) - constant extra space

## 🐍 Python Implementation

```python
def linear_search(arr, target):
    """Basic linear search - returns index or -1"""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

def linear_search_pythonic(arr, target):
    """Pythonic linear search using enumerate"""
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1

def linear_search_all_occurrences(arr, target):
    """Find all occurrences of target"""
    indices = []
    for i, element in enumerate(arr):
        if element == target:
            indices.append(i)
    return indices

def linear_search_with_condition(arr, condition):
    """Search with custom condition function"""
    for i, element in enumerate(arr):
        if condition(element):
            return i
    return -1

# Example usage
def example_linear_search():
    arr = [64, 34, 25, 12, 22, 11, 90, 22]
    
    print(f"Array: {arr}")
    print(f"Search for 22: index {linear_search(arr, 22)}")
    print(f"Search for 99: index {linear_search(arr, 99)}")
    print(f"All occurrences of 22: {linear_search_all_occurrences(arr, 22)}")
    
    # Search for first even number
    even_index = linear_search_with_condition(arr, lambda x: x % 2 == 0)
    print(f"First even number at index: {even_index}")

if __name__ == "__main__":
    example_linear_search()
```

## ☕ Java Implementation

```java
public class LinearSearch {
    
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
    
    public static int[] findAllOccurrences(int[] arr, int target) {
        List<Integer> indices = new ArrayList<>();
        
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                indices.add(i);
            }
        }
        
        return indices.stream().mapToInt(Integer::intValue).toArray();
    }
    
    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90, 22};
        
        System.out.println("Array: " + Arrays.toString(arr));
        System.out.println("Search for 22: index " + linearSearch(arr, 22));
        System.out.println("All occurrences of 22: " + 
                          Arrays.toString(findAllOccurrences(arr, 22)));
    }
}
```

## 🎯 When to Use Linear Search

✅ **Use Linear Search when:**
- Small datasets (n < 100)
- Unsorted data
- Need to find all occurrences
- Simple implementation required
- Data structure doesn't support random access

❌ **Don't use when:**
- Large datasets (prefer binary search if sorted)
- Frequent searches on same data
- Data is already sorted

## 🆚 Linear vs Binary Search

| Aspect | Linear Search | Binary Search |
|--------|---------------|---------------|
| **Prerequisite** | None | Sorted array |
| **Time Complexity** | O(n) | O(log n) |
| **Space Complexity** | O(1) | O(1) |
| **Implementation** | Simple | More complex |
| **Best for** | Unsorted data | Large sorted data |

## 🔗 Related Topics

- [[Binary Search]] - Efficient search for sorted arrays
- [[Hash Tables]] - O(1) average search time
- [[Arrays and Lists]] - Data structures commonly searched

---

*See also: [[Binary Search]], [[Arrays and Lists]], [[algorithms_and_ds]]*