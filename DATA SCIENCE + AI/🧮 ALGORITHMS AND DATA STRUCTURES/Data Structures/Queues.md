# Queues

> First-In-First-Out (FIFO) data structure where elements are added at the rear and removed from the front, similar to a line of people waiting.

## 📖 Definition

A queue is a linear data structure that follows the **FIFO (First-In-First-Out)** principle. The first element added is the first one to be removed. Think of it as a line at a store checkout.

## 🔑 Key Operations

- **Enqueue**: Add element to the rear/back - O(1)
- **Dequeue**: Remove and return front element - O(1)
- **Front/Peek**: View front element without removing - O(1)
- **isEmpty**: Check if queue is empty - O(1)
- **Size**: Get number of elements - O(1)

## 🎭 Types of Queues

### 1. Simple Queue
Basic FIFO queue with enqueue at rear, dequeue at front.

### 2. Circular Queue  
Fixed-size queue where rear connects back to front when full.

### 3. Priority Queue
Elements have priorities; highest priority dequeued first.

### 4. Deque (Double-ended Queue)
Allows insertion and deletion at both ends.

## 🐍 Python Implementation

```python
# Using collections.deque (most efficient)
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        """Add item to rear - O(1)"""
        self.items.append(item)
    
    def dequeue(self):
        """Remove and return front item - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.popleft()
    
    def front(self):
        """View front item - O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def is_empty(self):
        """Check if queue is empty - O(1)"""
        return len(self.items) == 0
    
    def size(self):
        """Get number of elements - O(1)"""
        return len(self.items)
    
    def __str__(self):
        return f"Queue: {list(self.items)} (front is left)"

# Using list (less efficient for large queues)
class QueueList:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)  # O(1)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.pop(0)  # O(n) - inefficient!
    
    def front(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

# Circular Queue implementation
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.front_idx = 0
        self.rear_idx = -1
        self.count = 0
    
    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("Queue is full")
        
        self.rear_idx = (self.rear_idx + 1) % self.capacity
        self.items[self.rear_idx] = item
        self.count += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        item = self.items[self.front_idx]
        self.items[self.front_idx] = None
        self.front_idx = (self.front_idx + 1) % self.capacity
        self.count -= 1
        return item
    
    def front(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[self.front_idx]
    
    def is_empty(self):
        return self.count == 0
    
    def is_full(self):
        return self.count == self.capacity
    
    def size(self):
        return self.count

# Priority Queue using heapq
import heapq

class PriorityQueue:
    def __init__(self):
        self.items = []
        self.counter = 0  # For tie-breaking
    
    def enqueue(self, item, priority):
        """Add item with priority (lower number = higher priority)"""
        heapq.heappush(self.items, (priority, self.counter, item))
        self.counter += 1
    
    def dequeue(self):
        """Remove and return highest priority item"""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        priority, _, item = heapq.heappop(self.items)
        return item
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
```

## ☕ Java Implementation

```java
import java.util.*;

// Array-based circular queue
public class CircularQueue<T> {
    private Object[] queue;
    private int front, rear, size, capacity;
    
    public CircularQueue(int capacity) {
        this.capacity = capacity;
        this.queue = new Object[capacity];
        this.front = 0;
        this.rear = -1;
        this.size = 0;
    }
    
    public void enqueue(T item) {
        if (isFull()) {
            throw new IllegalStateException("Queue is full");
        }
        rear = (rear + 1) % capacity;
        queue[rear] = item;
        size++;
    }
    
    @SuppressWarnings("unchecked")
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("Queue is empty");
        }
        T item = (T) queue[front];
        queue[front] = null;
        front = (front + 1) % capacity;
        size--;
        return item;
    }
    
    @SuppressWarnings("unchecked")
    public T front() {
        if (isEmpty()) {
            throw new NoSuchElementException("Queue is empty");
        }
        return (T) queue[front];
    }
    
    public boolean isEmpty() { return size == 0; }
    public boolean isFull() { return size == capacity; }
    public int size() { return size; }
}

// LinkedList-based queue
class QueueNode<T> {
    T data;
    QueueNode<T> next;
    
    QueueNode(T data) {
        this.data = data;
    }
}

public class LinkedQueue<T> {
    private QueueNode<T> front, rear;
    private int size;
    
    public LinkedQueue() {
        this.front = this.rear = null;
        this.size = 0;
    }
    
    public void enqueue(T data) {
        QueueNode<T> newNode = new QueueNode<>(data);
        
        if (rear == null) {
            front = rear = newNode;
        } else {
            rear.next = newNode;
            rear = newNode;
        }
        size++;
    }
    
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("Queue is empty");
        }
        
        T data = front.data;
        front = front.next;
        
        if (front == null) {
            rear = null;
        }
        size--;
        return data;
    }
    
    public T front() {
        if (isEmpty()) {
            throw new NoSuchElementException("Queue is empty");
        }
        return front.data;
    }
    
    public boolean isEmpty() { return front == null; }
    public int size() { return size; }
}

// Using built-in Queue classes
public class QueueExample {
    public static void main(String[] args) {
        // LinkedList as Queue
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(10);  // enqueue
        queue.offer(20);
        System.out.println(queue.poll()); // dequeue - returns 10
        
        // ArrayDeque (recommended)
        Queue<String> deque = new ArrayDeque<>();
        deque.offer("first");
        deque.offer("second");
        System.out.println(deque.peek()); // front - returns "first"
        
        // PriorityQueue
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.offer(30);
        pq.offer(10);
        pq.offer(20);
        System.out.println(pq.poll()); // returns 10 (smallest)
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <queue>
#include <deque>

// Array-based circular queue
template<typename T>
class CircularQueue {
private:
    T* data;
    int frontIdx, rearIdx, capacity, count;
    
public:
    CircularQueue(int cap) : capacity(cap), frontIdx(0), rearIdx(-1), count(0) {
        data = new T[capacity];
    }
    
    ~CircularQueue() {
        delete[] data;
    }
    
    void enqueue(const T& item) {
        if (isFull()) {
            throw std::overflow_error("Queue is full");
        }
        rearIdx = (rearIdx + 1) % capacity;
        data[rearIdx] = item;
        count++;
    }
    
    T dequeue() {
        if (isEmpty()) {
            throw std::underflow_error("Queue is empty");
        }
        T item = data[frontIdx];
        frontIdx = (frontIdx + 1) % capacity;
        count--;
        return item;
    }
    
    const T& front() const {
        if (isEmpty()) {
            throw std::underflow_error("Queue is empty");
        }
        return data[frontIdx];
    }
    
    bool isEmpty() const { return count == 0; }
    bool isFull() const { return count == capacity; }
    int size() const { return count; }
};

// Linked list implementation
template<typename T>
struct QueueNode {
    T data;
    QueueNode* next;
    
    QueueNode(const T& val) : data(val), next(nullptr) {}
};

template<typename T>
class LinkedQueue {
private:
    QueueNode<T>* frontPtr;
    QueueNode<T>* rearPtr;
    int queueSize;
    
public:
    LinkedQueue() : frontPtr(nullptr), rearPtr(nullptr), queueSize(0) {}
    
    ~LinkedQueue() {
        while (!isEmpty()) {
            dequeue();
        }
    }
    
    void enqueue(const T& data) {
        QueueNode<T>* newNode = new QueueNode<T>(data);
        
        if (isEmpty()) {
            frontPtr = rearPtr = newNode;
        } else {
            rearPtr->next = newNode;
            rearPtr = newNode;
        }
        queueSize++;
    }
    
    T dequeue() {
        if (isEmpty()) {
            throw std::underflow_error("Queue is empty");
        }
        
        T data = frontPtr->data;
        QueueNode<T>* temp = frontPtr;
        frontPtr = frontPtr->next;
        
        if (frontPtr == nullptr) {
            rearPtr = nullptr;
        }
        
        delete temp;
        queueSize--;
        return data;
    }
    
    const T& front() const {
        if (isEmpty()) {
            throw std::underflow_error("Queue is empty");
        }
        return frontPtr->data;
    }
    
    bool isEmpty() const { return frontPtr == nullptr; }
    int size() const { return queueSize; }
};

// Using STL queue
int main() {
    // Standard queue
    std::queue<int> q;
    q.push(10);
    q.push(20);
    q.push(30);
    
    std::cout << q.front() << std::endl; // 10
    q.pop();
    std::cout << q.size() << std::endl;  // 2
    
    // Priority queue (max-heap by default)
    std::priority_queue<int> pq;
    pq.push(30);
    pq.push(10);
    pq.push(20);
    std::cout << pq.top() << std::endl; // 30 (largest)
    
    // Deque (double-ended queue)
    std::deque<int> dq;
    dq.push_back(10);   // rear
    dq.push_front(5);   // front
    std::cout << dq.front() << " " << dq.back() << std::endl; // 5 10
    
    return 0;
}
```

## ⚡ Time Complexity Comparison

| Implementation | Enqueue | Dequeue | Front | Space |
|---------------|---------|---------|-------|--------|
| Array (circular) | O(1) | O(1) | O(1) | O(n) |
| Linked List | O(1) | O(1) | O(1) | O(n) |
| List (Python) | O(1) | O(n) | O(1) | O(n) |
| Deque | O(1) | O(1) | O(1) | O(n) |

## 🎯 Applications

### 1. Breadth-First Search (BFS)
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            print(vertex, end=' ')
            
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
```

### 2. Task Scheduling
```python
class TaskScheduler:
    def __init__(self):
        self.task_queue = deque()
    
    def add_task(self, task):
        self.task_queue.append(task)
    
    def process_next_task(self):
        if self.task_queue:
            return self.task_queue.popleft()
        return None
    
    def has_tasks(self):
        return len(self.task_queue) > 0
```

### 3. Cache Implementation (LRU)
```python
from collections import deque

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.order = deque()
    
    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            # Update existing
            self.cache[key] = value
            self.order.remove(key)
            self.order.append(key)
        else:
            # Add new
            if len(self.cache) >= self.capacity:
                # Remove least recently used
                lru_key = self.order.popleft()
                del self.cache[lru_key]
            
            self.cache[key] = value
            self.order.append(key)
```

## 🔗 Related Topics

- [[Stacks]] - LIFO counterpart to FIFO queues
- [[Binary Trees]] - BFS traversal uses queues
- [[Graphs]] - BFS and topological sort use queues
- [[Heaps]] - Priority queues often implemented with heaps

## 💡 Best Practices

1. **Choose appropriate implementation**:
   - `collections.deque` in Python
   - `ArrayDeque` in Java
   - `std::queue` in C++

2. **Consider circular queues** for fixed-size scenarios

3. **Use priority queues** when order matters beyond FIFO

4. **Handle empty queue exceptions** appropriately

## 📝 Practice Problems

1. **Implement Stack using Queues**: Use two queues to simulate stack
2. **Sliding Window Maximum**: Find maximum in each sliding window
3. **First Non-Repeating Character**: Find first unique char in stream
4. **Generate Binary Numbers**: Generate binary numbers from 1 to n
5. **Reverse First K Elements**: Reverse first k elements of queue
6. **Interleave Queue**: Interleave first and second half of queue

---

*See also: [[Stacks]], [[Binary Trees]], [[Graphs]], [[Heaps]], [[algorithms_and_ds]]*