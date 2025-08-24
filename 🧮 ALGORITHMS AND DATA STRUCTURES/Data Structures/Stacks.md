# Stacks

> Last-In-First-Out (LIFO) data structure where elements are added and removed from the same end, called the "top" of the stack.

## 📖 Definition

A stack is a linear data structure that follows the **LIFO (Last-In-First-Out)** principle. Think of it like a stack of plates - you can only add or remove plates from the top.

## 🔑 Key Operations

- **Push**: Add an element to the top - O(1)
- **Pop**: Remove and return the top element - O(1)  
- **Peek/Top**: View the top element without removing - O(1)
- **isEmpty**: Check if stack is empty - O(1)
- **Size**: Get number of elements - O(1)

## 🐍 Python Implementation

```python
# Using built-in list (simplest approach)
class StackList:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Add item to top - O(1)"""
        self.items.append(item)
    
    def pop(self):
        """Remove and return top item - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        """View top item without removing - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        """Check if stack is empty - O(1)"""
        return len(self.items) == 0
    
    def size(self):
        """Get number of elements - O(1)"""
        return len(self.items)
    
    def __str__(self):
        return f"Stack: {self.items} (top is right)"

# Using collections.deque (more efficient for large stacks)
from collections import deque

class StackDeque:
    def __init__(self):
        self.items = deque()
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.items:
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        if not self.items:
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

# Linked List implementation
class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class StackLinkedList:
    def __init__(self):
        self.head = None
        self._size = 0
    
    def push(self, data):
        """Add element to top - O(1)"""
        new_node = StackNode(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def pop(self):
        """Remove and return top element - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        
        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data
    
    def peek(self):
        """View top element - O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.head.data
    
    def is_empty(self):
        return self.head is None
    
    def size(self):
        return self._size
```

## ☕ Java Implementation

```java
import java.util.*;

// Array-based stack implementation
public class ArrayStack<T> {
    private T[] stack;
    private int top;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public ArrayStack(int capacity) {
        this.capacity = capacity;
        this.stack = (T[]) new Object[capacity];
        this.top = -1;
    }
    
    public void push(T item) {
        if (isFull()) {
            throw new StackOverflowError("Stack is full");
        }
        stack[++top] = item;
    }
    
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T item = stack[top];
        stack[top--] = null; // Help GC
        return item;
    }
    
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return stack[top];
    }
    
    public boolean isEmpty() {
        return top == -1;
    }
    
    public boolean isFull() {
        return top == capacity - 1;
    }
    
    public int size() {
        return top + 1;
    }
}

// LinkedList-based stack implementation
class StackNode<T> {
    T data;
    StackNode<T> next;
    
    StackNode(T data) {
        this.data = data;
    }
}

public class LinkedStack<T> {
    private StackNode<T> head;
    private int size;
    
    public LinkedStack() {
        this.head = null;
        this.size = 0;
    }
    
    public void push(T data) {
        StackNode<T> newNode = new StackNode<>(data);
        newNode.next = head;
        head = newNode;
        size++;
    }
    
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        T data = head.data;
        head = head.next;
        size--;
        return data;
    }
    
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return head.data;
    }
    
    public boolean isEmpty() {
        return head == null;
    }
    
    public int size() {
        return size;
    }
}

// Using built-in Stack class
public class StackExample {
    public static void main(String[] args) {
        Stack<Integer> stack = new Stack<>();
        
        stack.push(10);
        stack.push(20);
        stack.push(30);
        
        System.out.println(stack.peek()); // 30
        System.out.println(stack.pop());  // 30
        System.out.println(stack.size()); // 2
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <stack>
#include <vector>

// Array-based stack implementation
template<typename T>
class ArrayStack {
private:
    std::vector<T> data;
    
public:
    void push(const T& item) {
        data.push_back(item);
    }
    
    T pop() {
        if (empty()) {
            throw std::runtime_error("Stack is empty");
        }
        T item = data.back();
        data.pop_back();
        return item;
    }
    
    const T& top() const {
        if (empty()) {
            throw std::runtime_error("Stack is empty");
        }
        return data.back();
    }
    
    bool empty() const {
        return data.empty();
    }
    
    size_t size() const {
        return data.size();
    }
};

// Linked List implementation
template<typename T>
struct StackNode {
    T data;
    StackNode* next;
    
    StackNode(const T& val) : data(val), next(nullptr) {}
};

template<typename T>
class LinkedStack {
private:
    StackNode<T>* head;
    size_t stackSize;
    
public:
    LinkedStack() : head(nullptr), stackSize(0) {}
    
    ~LinkedStack() {
        while (!empty()) {
            pop();
        }
    }
    
    void push(const T& data) {
        StackNode<T>* newNode = new StackNode<T>(data);
        newNode->next = head;
        head = newNode;
        stackSize++;
    }
    
    T pop() {
        if (empty()) {
            throw std::runtime_error("Stack is empty");
        }
        T data = head->data;
        StackNode<T>* temp = head;
        head = head->next;
        delete temp;
        stackSize--;
        return data;
    }
    
    const T& top() const {
        if (empty()) {
            throw std::runtime_error("Stack is empty");
        }
        return head->data;
    }
    
    bool empty() const {
        return head == nullptr;
    }
    
    size_t size() const {
        return stackSize;
    }
};

// Using STL stack
int main() {
    std::stack<int> s;
    
    s.push(10);
    s.push(20);
    s.push(30);
    
    std::cout << s.top() << std::endl; // 30
    s.pop();
    std::cout << s.size() << std::endl; // 2
    
    return 0;
}
```

## 🏗️ Implementation Comparison

| Implementation | Push | Pop | Peek | Space | Notes |
|----------------|------|-----|------|-------|--------|
| Array/Vector | O(1)* | O(1) | O(1) | O(n) | May need resizing |
| Linked List | O(1) | O(1) | O(1) | O(n) | Extra pointer overhead |
| Built-in | O(1)* | O(1) | O(1) | O(n) | Optimized, recommended |

*Amortized time for dynamic arrays

## 🎯 Applications

### 1. Function Call Management
```python
# Call stack in recursion
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # Each call pushed onto stack
```

### 2. Expression Evaluation
```python
def evaluate_postfix(expression):
    """Evaluate postfix expression using stack"""
    stack = []
    operators = {'+', '-', '*', '/'}
    
    for token in expression.split():
        if token not in operators:
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a // b)
    
    return stack[0]

# Example: "3 4 + 2 *" = (3 + 4) * 2 = 14
```

### 3. Balanced Parentheses
```python
def is_balanced(expression):
    """Check if parentheses are balanced"""
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in expression:
        if char in pairs:  # Opening bracket
            stack.append(char)
        elif char in pairs.values():  # Closing bracket
            if not stack or pairs[stack.pop()] != char:
                return False
    
    return len(stack) == 0
```

### 4. Undo Operations
```python
class TextEditor:
    def __init__(self):
        self.text = ""
        self.undo_stack = []
    
    def type(self, text):
        self.undo_stack.append(('type', self.text))
        self.text += text
    
    def delete(self, count):
        self.undo_stack.append(('delete', self.text))
        self.text = self.text[:-count]
    
    def undo(self):
        if self.undo_stack:
            operation, previous_state = self.undo_stack.pop()
            self.text = previous_state
```

## 🔗 Related Topics

- [[Queues]] - FIFO counterpart to LIFO stacks
- [[Binary Trees]] - Tree traversal uses stack (DFS)
- [[Recursion]] - Function calls use system stack
- [[Dynamic Programming]] - Some DP problems use stacks

## 💡 Tips and Best Practices

1. **Choose the right implementation**:
   - Use built-in stack classes when available
   - Array-based for simple use cases
   - Linked list for memory-constrained environments

2. **Always check for empty stack** before pop/peek operations

3. **Consider stack overflow** in recursive algorithms

4. **Memory management** in manual implementations (C++)

## 📝 Practice Problems

1. **Valid Parentheses**: Check if string has valid parentheses
2. **Min Stack**: Design stack that supports getMin() in O(1)
3. **Evaluate Expression**: Implement calculator using stacks
4. **Next Greater Element**: Find next greater element for each array element
5. **Largest Rectangle in Histogram**: Find largest rectangle area
6. **Daily Temperatures**: Find warmer temperature for each day

## 🔍 Related Algorithms

- **Depth-First Search (DFS)**: Uses stack for traversal
- **Backtracking**: Uses stack to store decision points
- **Parsing**: Expression parsing and syntax analysis

---

*See also: [[Queues]], [[Linked Lists]], [[Binary Trees]], [[algorithms_and_ds]]*