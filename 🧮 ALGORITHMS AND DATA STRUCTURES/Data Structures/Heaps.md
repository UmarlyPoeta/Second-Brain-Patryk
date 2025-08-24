# Heaps

> Complete binary tree data structure that satisfies the heap property, commonly used to implement priority queues and efficient sorting algorithms.

## 📖 Definition

A heap is a specialized tree-based data structure that satisfies the heap property:
- **Max Heap**: Parent node ≥ children nodes (largest element at root)
- **Min Heap**: Parent node ≤ children nodes (smallest element at root)

## 🔑 Key Properties

1. **Complete Binary Tree**: All levels filled except possibly the last, filled left to right
2. **Heap Property**: Maintained throughout all operations
3. **Array Representation**: Efficient storage using arrays
4. **Parent-Child Relationships**: For node at index i:
   - Left child: `2i + 1`
   - Right child: `2i + 2`
   - Parent: `(i - 1) // 2`

## ⚡ Time Complexity

| Operation | Time Complexity |
|-----------|-----------------|
| **Insert** | O(log n) |
| **Extract Min/Max** | O(log n) |
| **Peek Min/Max** | O(1) |
| **Build Heap** | O(n) |
| **Heapify** | O(log n) |

## 🐍 Python Implementation

```python
class MaxHeap:
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2
    
    def has_parent(self, i):
        return self.parent(i) >= 0
    
    def has_left_child(self, i):
        return self.left_child(i) < self.size
    
    def has_right_child(self, i):
        return self.right_child(i) < self.size
    
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def insert(self, value):
        """Insert value into heap - O(log n)"""
        self.heap.append(value)
        self.size += 1
        self.heapify_up()
    
    def heapify_up(self):
        """Maintain heap property upwards"""
        index = self.size - 1
        while (self.has_parent(index) and 
               self.heap[self.parent(index)] < self.heap[index]):
            self.swap(self.parent(index), index)
            index = self.parent(index)
    
    def extract_max(self):
        """Remove and return maximum element - O(log n)"""
        if self.size == 0:
            raise IndexError("Heap is empty")
        
        max_value = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        
        if self.size > 0:
            self.heapify_down()
        
        return max_value
    
    def heapify_down(self):
        """Maintain heap property downwards"""
        index = 0
        
        while self.has_left_child(index):
            larger_child_index = self.left_child(index)
            
            if (self.has_right_child(index) and 
                self.heap[self.right_child(index)] > self.heap[larger_child_index]):
                larger_child_index = self.right_child(index)
            
            if self.heap[index] < self.heap[larger_child_index]:
                self.swap(index, larger_child_index)
                index = larger_child_index
            else:
                break
    
    def peek(self):
        """Get maximum element without removing - O(1)"""
        if self.size == 0:
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def is_empty(self):
        return self.size == 0
    
    def get_size(self):
        return self.size
    
    def build_heap(self, arr):
        """Build heap from array - O(n)"""
        self.heap = arr.copy()
        self.size = len(arr)
        
        # Start from last non-leaf node and heapify down
        for i in range((self.size - 1) // 2, -1, -1):
            self._heapify_down_from(i)
    
    def _heapify_down_from(self, index):
        """Heapify down from specific index"""
        while self.has_left_child(index):
            larger_child_index = self.left_child(index)
            
            if (self.has_right_child(index) and 
                self.heap[self.right_child(index)] > self.heap[larger_child_index]):
                larger_child_index = self.right_child(index)
            
            if self.heap[index] < self.heap[larger_child_index]:
                self.swap(index, larger_child_index)
                index = larger_child_index
            else:
                break

class MinHeap:
    def __init__(self):
        self.heap = []
        self.size = 0
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2
    
    def has_parent(self, i):
        return self.parent(i) >= 0
    
    def has_left_child(self, i):
        return self.left_child(i) < self.size
    
    def has_right_child(self, i):
        return self.right_child(i) < self.size
    
    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def insert(self, value):
        """Insert value into min heap"""
        self.heap.append(value)
        self.size += 1
        self.heapify_up()
    
    def heapify_up(self):
        index = self.size - 1
        while (self.has_parent(index) and 
               self.heap[self.parent(index)] > self.heap[index]):
            self.swap(self.parent(index), index)
            index = self.parent(index)
    
    def extract_min(self):
        """Remove and return minimum element"""
        if self.size == 0:
            raise IndexError("Heap is empty")
        
        min_value = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        
        if self.size > 0:
            self.heapify_down()
        
        return min_value
    
    def heapify_down(self):
        index = 0
        
        while self.has_left_child(index):
            smaller_child_index = self.left_child(index)
            
            if (self.has_right_child(index) and 
                self.heap[self.right_child(index)] < self.heap[smaller_child_index]):
                smaller_child_index = self.right_child(index)
            
            if self.heap[index] > self.heap[smaller_child_index]:
                self.swap(index, smaller_child_index)
                index = smaller_child_index
            else:
                break
    
    def peek(self):
        if self.size == 0:
            raise IndexError("Heap is empty")
        return self.heap[0]

# Using Python's heapq module (min heap)
import heapq

def heap_operations_builtin():
    """Examples using Python's built-in heapq"""
    # Create min heap
    heap = []
    
    # Insert elements
    heapq.heappush(heap, 5)
    heapq.heappush(heap, 2)
    heapq.heappush(heap, 8)
    heapq.heappush(heap, 1)
    
    print(f"Heap: {heap}")  # [1, 2, 8, 5]
    
    # Extract minimum
    min_val = heapq.heappop(heap)
    print(f"Extracted min: {min_val}")  # 1
    
    # Peek minimum
    print(f"Current min: {heap[0]}")  # 2
    
    # Build heap from list
    data = [9, 4, 7, 1, 3, 6]
    heapq.heapify(data)  # O(n) operation
    print(f"Heapified: {data}")
    
    # Get n largest/smallest elements
    numbers = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
    largest_3 = heapq.nlargest(3, numbers)
    smallest_3 = heapq.nsmallest(3, numbers)
    print(f"3 largest: {largest_3}")
    print(f"3 smallest: {smallest_3}")

# Max heap using heapq (negate values)
class MaxHeapBuiltin:
    def __init__(self):
        self.heap = []
    
    def insert(self, val):
        heapq.heappush(self.heap, -val)
    
    def extract_max(self):
        return -heapq.heappop(self.heap)
    
    def peek_max(self):
        return -self.heap[0]
    
    def is_empty(self):
        return len(self.heap) == 0
```

## ☕ Java Implementation

```java
import java.util.*;

public class MaxHeap {
    private List<Integer> heap;
    
    public MaxHeap() {
        this.heap = new ArrayList<>();
    }
    
    private int parent(int i) {
        return (i - 1) / 2;
    }
    
    private int leftChild(int i) {
        return 2 * i + 1;
    }
    
    private int rightChild(int i) {
        return 2 * i + 2;
    }
    
    private boolean hasParent(int i) {
        return parent(i) >= 0;
    }
    
    private boolean hasLeftChild(int i) {
        return leftChild(i) < heap.size();
    }
    
    private boolean hasRightChild(int i) {
        return rightChild(i) < heap.size();
    }
    
    private void swap(int i, int j) {
        Collections.swap(heap, i, j);
    }
    
    public void insert(int value) {
        heap.add(value);
        heapifyUp();
    }
    
    private void heapifyUp() {
        int index = heap.size() - 1;
        while (hasParent(index) && heap.get(parent(index)) < heap.get(index)) {
            swap(parent(index), index);
            index = parent(index);
        }
    }
    
    public int extractMax() {
        if (heap.isEmpty()) {
            throw new IllegalStateException("Heap is empty");
        }
        
        int max = heap.get(0);
        heap.set(0, heap.get(heap.size() - 1));
        heap.remove(heap.size() - 1);
        
        if (!heap.isEmpty()) {
            heapifyDown();
        }
        
        return max;
    }
    
    private void heapifyDown() {
        int index = 0;
        
        while (hasLeftChild(index)) {
            int largerChildIndex = leftChild(index);
            
            if (hasRightChild(index) && 
                heap.get(rightChild(index)) > heap.get(largerChildIndex)) {
                largerChildIndex = rightChild(index);
            }
            
            if (heap.get(index) < heap.get(largerChildIndex)) {
                swap(index, largerChildIndex);
                index = largerChildIndex;
            } else {
                break;
            }
        }
    }
    
    public int peek() {
        if (heap.isEmpty()) {
            throw new IllegalStateException("Heap is empty");
        }
        return heap.get(0);
    }
    
    public boolean isEmpty() {
        return heap.isEmpty();
    }
    
    public int size() {
        return heap.size();
    }
    
    // Using Java's PriorityQueue (min heap by default)
    public static void demonstrateBuiltinHeap() {
        // Min heap
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.offer(5);
        minHeap.offer(2);
        minHeap.offer(8);
        minHeap.offer(1);
        
        System.out.println("Min heap peek: " + minHeap.peek()); // 1
        System.out.println("Extracted: " + minHeap.poll()); // 1
        
        // Max heap using custom comparator
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        maxHeap.offer(5);
        maxHeap.offer(2);
        maxHeap.offer(8);
        maxHeap.offer(1);
        
        System.out.println("Max heap peek: " + maxHeap.peek()); // 8
        System.out.println("Extracted: " + maxHeap.poll()); // 8
    }
    
    public static void main(String[] args) {
        MaxHeap heap = new MaxHeap();
        
        heap.insert(10);
        heap.insert(5);
        heap.insert(15);
        heap.insert(20);
        heap.insert(8);
        
        System.out.println("Max: " + heap.peek()); // 20
        System.out.println("Extracted: " + heap.extractMax()); // 20
        System.out.println("New max: " + heap.peek()); // 15
        
        demonstrateBuiltinHeap();
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

class MaxHeap {
private:
    std::vector<int> heap;
    
    int parent(int i) { return (i - 1) / 2; }
    int leftChild(int i) { return 2 * i + 1; }
    int rightChild(int i) { return 2 * i + 2; }
    
    bool hasParent(int i) { return parent(i) >= 0; }
    bool hasLeftChild(int i) { return leftChild(i) < heap.size(); }
    bool hasRightChild(int i) { return rightChild(i) < heap.size(); }
    
    void heapifyUp() {
        int index = heap.size() - 1;
        while (hasParent(index) && heap[parent(index)] < heap[index]) {
            std::swap(heap[parent(index)], heap[index]);
            index = parent(index);
        }
    }
    
    void heapifyDown() {
        int index = 0;
        
        while (hasLeftChild(index)) {
            int largerChildIndex = leftChild(index);
            
            if (hasRightChild(index) && 
                heap[rightChild(index)] > heap[largerChildIndex]) {
                largerChildIndex = rightChild(index);
            }
            
            if (heap[index] < heap[largerChildIndex]) {
                std::swap(heap[index], heap[largerChildIndex]);
                index = largerChildIndex;
            } else {
                break;
            }
        }
    }
    
public:
    void insert(int value) {
        heap.push_back(value);
        heapifyUp();
    }
    
    int extractMax() {
        if (heap.empty()) {
            throw std::runtime_error("Heap is empty");
        }
        
        int maxValue = heap[0];
        heap[0] = heap.back();
        heap.pop_back();
        
        if (!heap.empty()) {
            heapifyDown();
        }
        
        return maxValue;
    }
    
    int peek() const {
        if (heap.empty()) {
            throw std::runtime_error("Heap is empty");
        }
        return heap[0];
    }
    
    bool empty() const {
        return heap.empty();
    }
    
    size_t size() const {
        return heap.size();
    }
    
    void display() const {
        for (int val : heap) {
            std::cout << val << " ";
        }
        std::cout << std::endl;
    }
};

// Using STL priority_queue
void demonstrateSTLHeap() {
    // Max heap (default)
    std::priority_queue<int> maxHeap;
    maxHeap.push(5);
    maxHeap.push(2);
    maxHeap.push(8);
    maxHeap.push(1);
    
    std::cout << "Max heap top: " << maxHeap.top() << std::endl; // 8
    maxHeap.pop();
    std::cout << "After pop: " << maxHeap.top() << std::endl; // 5
    
    // Min heap
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap;
    minHeap.push(5);
    minHeap.push(2);
    minHeap.push(8);
    minHeap.push(1);
    
    std::cout << "Min heap top: " << minHeap.top() << std::endl; // 1
    minHeap.pop();
    std::cout << "After pop: " << minHeap.top() << std::endl; // 2
    
    // Build heap from vector
    std::vector<int> data = {9, 4, 7, 1, 3, 6};
    std::make_heap(data.begin(), data.end()); // Max heap
    
    std::cout << "Heap root: " << data.front() << std::endl; // 9
    
    // Add element to heap
    data.push_back(15);
    std::push_heap(data.begin(), data.end());
    std::cout << "New heap root: " << data.front() << std::endl; // 15
    
    // Remove root from heap
    std::pop_heap(data.begin(), data.end());
    data.pop_back();
    std::cout << "After removing root: " << data.front() << std::endl; // 9
}

int main() {
    MaxHeap heap;
    
    heap.insert(10);
    heap.insert(5);
    heap.insert(15);
    heap.insert(20);
    heap.insert(8);
    
    std::cout << "Heap: ";
    heap.display();
    
    std::cout << "Max: " << heap.peek() << std::endl; // 20
    std::cout << "Extracted: " << heap.extractMax() << std::endl; // 20
    std::cout << "New max: " << heap.peek() << std::endl; // 15
    
    std::cout << "\nSTL heap demonstration:" << std::endl;
    demonstrateSTLHeap();
    
    return 0;
}
```

## 🎯 Applications

### 1. Priority Queue
```python
class PriorityQueue:
    def __init__(self):
        self.heap = []
    
    def enqueue(self, item, priority):
        heapq.heappush(self.heap, (priority, item))
    
    def dequeue(self):
        return heapq.heappop(self.heap)[1]
    
    def is_empty(self):
        return len(self.heap) == 0
```

### 2. Heap Sort
```python
def heap_sort(arr):
    """Sort array using heap sort - O(n log n)"""
    # Build max heap
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Move max to end
        heapify(arr, i, 0)  # Heapify reduced heap
    
    return arr

def heapify(arr, n, i):
    """Heapify subtree rooted at index i"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
```

### 3. Finding K Largest/Smallest Elements
```python
def k_largest(arr, k):
    """Find k largest elements using heap"""
    return heapq.nlargest(k, arr)

def k_smallest(arr, k):
    """Find k smallest elements using heap"""
    return heapq.nsmallest(k, arr)

def k_largest_efficient(arr, k):
    """Find k largest using min heap of size k"""
    if k >= len(arr):
        return arr
    
    heap = arr[:k]
    heapq.heapify(heap)
    
    for num in arr[k:]:
        if num > heap[0]:
            heapq.heappop(heap)
            heapq.heappush(heap, num)
    
    return heap
```

## 🔗 Related Topics

- [[Binary Trees]] - Heaps are complete binary trees
- [[Priority Queues]] - Primary use case for heaps
- [[Sorting Algorithms]] - Heap sort algorithm
- [[Graphs]] - Dijkstra's algorithm uses heaps

## 📝 Practice Problems

1. **Kth Largest Element**: Find kth largest element in array
2. **Merge K Sorted Lists**: Use min heap to merge efficiently
3. **Top K Frequent Elements**: Find k most frequent elements
4. **Sliding Window Maximum**: Use heap or deque
5. **Find Median from Data Stream**: Use two heaps
6. **Task Scheduler**: Use heap for task scheduling
7. **Ugly Number II**: Generate ugly numbers using heaps

---

*See also: [[Binary Trees]], [[Priority Queues]], [[Sorting Algorithms]], [[algorithms_and_ds]]*