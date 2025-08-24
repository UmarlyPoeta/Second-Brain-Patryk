# Linked Lists

> Dynamic linear data structure where elements (nodes) are stored in sequence, with each node containing data and a reference to the next node.

## 📖 Definition

A linked list is a collection of nodes where each node contains:
- **Data**: The actual value stored
- **Next**: Reference/pointer to the next node in sequence

Unlike arrays, linked lists don't require contiguous memory allocation.

## 🔗 Types of Linked Lists

### 1. Singly Linked List
Each node points to the next node, ending with null.

### 2. Doubly Linked List  
Each node has pointers to both next and previous nodes.

### 3. Circular Linked List
The last node points back to the first node.

## 🐍 Python Implementation

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, val):
        """Add element at end - O(n)"""
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def prepend(self, val):
        """Add element at beginning - O(1)"""
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def delete(self, val):
        """Delete first occurrence - O(n)"""
        if not self.head:
            return
        
        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return
        
        current = self.head
        while current.next and current.next.val != val:
            current = current.next
        
        if current.next:
            current.next = current.next.next
            self.size -= 1
    
    def find(self, val):
        """Search for value - O(n)"""
        current = self.head
        while current:
            if current.val == val:
                return True
            current = current.next
        return False
    
    def display(self):
        """Print all elements - O(n)"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.val))
            current = current.next
        return " -> ".join(elements) + " -> None"

# Doubly Linked List Node
class DoublyListNode:
    def __init__(self, val=0, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, val):
        """Add at end - O(1)"""
        new_node = DoublyListNode(val)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def prepend(self, val):
        """Add at beginning - O(1)"""
        new_node = DoublyListNode(val)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
```

## ☕ Java Implementation

```java
class ListNode {
    int val;
    ListNode next;
    
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

public class SinglyLinkedList {
    private ListNode head;
    private int size;
    
    public SinglyLinkedList() {
        this.head = null;
        this.size = 0;
    }
    
    public void append(int val) {
        ListNode newNode = new ListNode(val);
        if (head == null) {
            head = newNode;
        } else {
            ListNode current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        size++;
    }
    
    public void prepend(int val) {
        ListNode newNode = new ListNode(val);
        newNode.next = head;
        head = newNode;
        size++;
    }
    
    public boolean delete(int val) {
        if (head == null) return false;
        
        if (head.val == val) {
            head = head.next;
            size--;
            return true;
        }
        
        ListNode current = head;
        while (current.next != null && current.next.val != val) {
            current = current.next;
        }
        
        if (current.next != null) {
            current.next = current.next.next;
            size--;
            return true;
        }
        return false;
    }
    
    public boolean contains(int val) {
        ListNode current = head;
        while (current != null) {
            if (current.val == val) return true;
            current = current.next;
        }
        return false;
    }
    
    public void display() {
        ListNode current = head;
        while (current != null) {
            System.out.print(current.val + " -> ");
            current = current.next;
        }
        System.out.println("null");
    }
    
    public int size() { return size; }
    public boolean isEmpty() { return head == null; }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>

struct ListNode {
    int val;
    ListNode* next;
    
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* next) : val(x), next(next) {}
};

class SinglyLinkedList {
private:
    ListNode* head;
    int size;
    
public:
    SinglyLinkedList() : head(nullptr), size(0) {}
    
    ~SinglyLinkedList() {
        while (head) {
            ListNode* temp = head;
            head = head->next;
            delete temp;
        }
    }
    
    void append(int val) {
        ListNode* newNode = new ListNode(val);
        if (!head) {
            head = newNode;
        } else {
            ListNode* current = head;
            while (current->next) {
                current = current->next;
            }
            current->next = newNode;
        }
        size++;
    }
    
    void prepend(int val) {
        ListNode* newNode = new ListNode(val);
        newNode->next = head;
        head = newNode;
        size++;
    }
    
    bool remove(int val) {
        if (!head) return false;
        
        if (head->val == val) {
            ListNode* temp = head;
            head = head->next;
            delete temp;
            size--;
            return true;
        }
        
        ListNode* current = head;
        while (current->next && current->next->val != val) {
            current = current->next;
        }
        
        if (current->next) {
            ListNode* temp = current->next;
            current->next = current->next->next;
            delete temp;
            size--;
            return true;
        }
        return false;
    }
    
    bool contains(int val) const {
        ListNode* current = head;
        while (current) {
            if (current->val == val) return true;
            current = current->next;
        }
        return false;
    }
    
    void display() const {
        ListNode* current = head;
        while (current) {
            std::cout << current->val << " -> ";
            current = current->next;
        }
        std::cout << "nullptr\n";
    }
    
    int getSize() const { return size; }
    bool empty() const { return head == nullptr; }
};
```

## ⚡ Time Complexity

| Operation | Singly Linked | Doubly Linked |
|-----------|---------------|---------------|
| Access by index | O(n) | O(n) |
| Insert at beginning | O(1) | O(1) |
| Insert at end | O(n) | O(1)* |
| Insert in middle | O(n) | O(n) |
| Delete from beginning | O(1) | O(1) |
| Delete from end | O(n) | O(1)* |
| Delete by value | O(n) | O(n) |
| Search | O(n) | O(n) |

*With tail pointer

## 🆚 Arrays vs Linked Lists

| Aspect | Arrays | Linked Lists |
|--------|--------|--------------|
| **Memory** | Contiguous | Non-contiguous |
| **Access Time** | O(1) by index | O(n) sequential |
| **Insertion** | O(n) in middle | O(1) if node known |
| **Deletion** | O(n) in middle | O(1) if node known |
| **Memory Overhead** | None | Extra pointer storage |
| **Cache Performance** | Better | Worse |

## 🎯 Use Cases

### When to Use Linked Lists:
- Frequent insertions/deletions
- Unknown or varying size
- Don't need random access
- Implementing other data structures ([[Stacks]], [[Queues]])

### When NOT to Use:
- Need random access by index
- Memory is limited (pointer overhead)
- Cache performance is critical
- Frequent searching operations

## 🔗 Related Topics

- [[Stacks]] - Can be implemented using linked lists
- [[Queues]] - Can be implemented using linked lists  
- [[Trees]] - Extension of linked list concept
- [[Hash Tables]] - Handle collisions with linked lists

## 💡 Common Applications

1. **Undo functionality** in applications
2. **Music playlists** (next/previous songs)
3. **Browser history** navigation
4. **Implementation of other data structures**
5. **Memory management** in operating systems

## 📝 Practice Problems

1. **Reverse a Linked List**: Iterative and recursive approaches
2. **Merge Two Sorted Lists**: Combine two sorted linked lists
3. **Cycle Detection**: Detect if linked list has a cycle
4. **Find Middle Node**: Find middle element in one pass
5. **Remove Duplicates**: Remove duplicate nodes from sorted list
6. **Intersection of Two Lists**: Find where two lists intersect

---

*See also: [[Arrays and Lists]], [[Stacks]], [[Queues]], [[algorithms_and_ds]]*