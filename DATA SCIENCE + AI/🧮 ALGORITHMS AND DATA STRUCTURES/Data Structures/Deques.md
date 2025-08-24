# Deques

> Double-ended queue data structure that allows insertion and deletion at both ends, providing O(1) operations at front and back.

## 📖 Definition

A deque (double-ended queue) is a linear data structure that supports insertion and deletion operations at both ends. It combines features of both stacks and queues.

## 🔑 Key Operations

- **append()**: Add to back - O(1)
- **appendleft()**: Add to front - O(1)  
- **pop()**: Remove from back - O(1)
- **popleft()**: Remove from front - O(1)

## 🐍 Python Implementation

```python
from collections import deque

# Using built-in deque
dq = deque([1, 2, 3])

# Add elements
dq.append(4)        # [1, 2, 3, 4]
dq.appendleft(0)    # [0, 1, 2, 3, 4]

# Remove elements  
dq.pop()            # Remove 4: [0, 1, 2, 3]
dq.popleft()        # Remove 0: [1, 2, 3]

# Access elements
print(dq[0])        # First element
print(dq[-1])       # Last element
```

## 🎯 Applications

1. **Sliding Window Problems**: Maintain window efficiently
2. **Palindrome Checking**: Compare from both ends
3. **Undo/Redo Operations**: Recent actions at both ends
4. **BFS/DFS**: Graph traversal algorithms

## 🔗 Related Topics

- [[Stacks]] - LIFO structure (one end only)
- [[Queues]] - FIFO structure (two ends, different operations)
- [[Arrays and Lists]] - Linear data structures

---

*See also: [[Stacks]], [[Queues]], [[algorithms_and_ds]]*