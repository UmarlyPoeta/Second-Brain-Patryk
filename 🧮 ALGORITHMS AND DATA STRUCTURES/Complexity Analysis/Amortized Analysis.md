# Amortized Analysis

> Method of analyzing algorithms that considers the average cost of operations over a sequence, rather than the worst-case cost of individual operations.

## 📖 Definition

Amortized analysis provides a way to analyze the average performance of operations in a data structure over a sequence of operations, even when individual operations might be expensive. It gives a more realistic view of algorithm performance than worst-case analysis alone.

## 🎯 Analysis Methods

### 1. Aggregate Method
Calculate total cost of n operations and divide by n.

### 2. Accounting Method
Assign amortized costs to operations and maintain a credit system.

### 3. Potential Method
Use a potential function to measure the "stored energy" in the data structure.

## ⚡ Key Concepts

- **Amortized Cost**: Average cost per operation over worst-case sequence
- **Credit System**: Operations can "pay" for future expensive operations
- **Worst-Case Sequence**: Sequence that maximizes total cost

## 🐍 Python Implementation Examples

```python
# Example 1: Dynamic Array (Python List)
class DynamicArray:
    """Dynamic array with amortized O(1) append"""
    
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.array = [None] * self.capacity
    
    def append(self, item):
        """Amortized O(1) append operation"""
        if self.size == self.capacity:
            self._resize()
        
        self.array[self.size] = item
        self.size += 1
    
    def _resize(self):
        """Double capacity when full - expensive but infrequent"""
        old_array = self.array
        self.capacity *= 2
        self.array = [None] * self.capacity
        
        for i in range(self.size):
            self.array[i] = old_array[i]
    
    def __str__(self):
        return str([self.array[i] for i in range(self.size)])

# Example 2: Stack with Multi-Pop
class StackWithMultiPop:
    """Stack supporting multi-pop operation"""
    
    def __init__(self):
        self.stack = []
    
    def push(self, item):
        """O(1) push operation"""
        self.stack.append(item)
    
    def pop(self):
        """O(1) pop operation"""
        if self.stack:
            return self.stack.pop()
        return None
    
    def multi_pop(self, k):
        """Pop k elements - O(k) but amortized O(1) per element"""
        result = []
        for _ in range(min(k, len(self.stack))):
            if self.stack:
                result.append(self.stack.pop())
        return result

# Example 3: Binary Counter
class BinaryCounter:
    """Binary counter demonstrating amortized analysis"""
    
    def __init__(self, bits):
        self.bits = [0] * bits
        self.value = 0
    
    def increment(self):
        """Increment counter - amortized O(1)"""
        carry = 1
        for i in range(len(self.bits)):
            if carry == 0:
                break
            
            if self.bits[i] == 0:
                self.bits[i] = 1
                carry = 0
            else:
                self.bits[i] = 0
                carry = 1
        
        self.value += 1
    
    def __str__(self):
        return ''.join(map(str, reversed(self.bits)))

# Example 4: Splay Tree (Simplified)
class SplayNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class SimplifiedSplayTree:
    """Simplified splay tree for amortized analysis demonstration"""
    
    def __init__(self):
        self.root = None
    
    def splay(self, node):
        """Move node to root - amortized O(log n)"""
        # Simplified implementation
        # In practice, involves zig, zig-zig, zig-zag rotations
        # Each access is amortized O(log n) even though single operation might be O(n)
        pass
    
    def search(self, data):
        """Search and splay - amortized O(log n)"""
        # Find node and splay it to root
        # Individual search might be O(n) but amortized is O(log n)
        pass

# Amortized Analysis Demonstration
def demonstrate_amortized_analysis():
    """Show amortized vs worst-case analysis"""
    
    # Dynamic Array Analysis
    print("Dynamic Array Append Analysis:")
    print("Individual operations:")
    
    da = DynamicArray()
    total_cost = 0
    
    for i in range(16):
        cost = 1  # Basic append cost
        if da.size == da.capacity:
            cost += da.size  # Resize cost
        
        da.append(i)
        total_cost += cost
        
        print(f"Append {i}: cost = {cost}, capacity = {da.capacity}")
    
    avg_cost = total_cost / 16
    print(f"Average amortized cost: {avg_cost}")
    print(f"Worst-case single operation: O(n)")
    print(f"Amortized cost: O(1)")
    
    # Binary Counter Analysis
    print("\nBinary Counter Analysis:")
    counter = BinaryCounter(4)
    
    for i in range(16):
        bit_flips = 0
        old_bits = counter.bits[:]
        counter.increment()
        
        # Count bit flips
        for j in range(len(counter.bits)):
            if old_bits[j] != counter.bits[j]:
                bit_flips += 1
        
        print(f"Increment {i}: {counter} (flips: {bit_flips})")

# Example usage
if __name__ == "__main__":
    # Merge sort
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", arr)
    sorted_arr = merge_sort(arr)
    print("Sorted array:", sorted_arr)
    
    # Stack with multi-pop
    stack = StackWithMultiPop()
    for i in range(10):
        stack.push(i)
    
    print("Multi-pop 3 elements:", stack.multi_pop(3))
    print("Remaining stack:", stack.stack)
    
    # Amortized analysis demonstration
    demonstrate_amortized_analysis()
```

## 🎯 Common Examples

### Dynamic Array Resizing
- **Individual Operation**: O(n) for resize
- **Amortized Cost**: O(1) per append
- **Analysis**: Resize happens infrequently

### Binary Counter
- **Individual Operation**: O(k) bit flips
- **Amortized Cost**: O(1) per increment
- **Analysis**: Higher-order bits flip less frequently

### Splay Trees
- **Individual Operation**: O(n) for skewed tree
- **Amortized Cost**: O(log n) per access
- **Analysis**: Frequent items move closer to root

## 💡 When to Use Amortized Analysis

✅ **Use when:**
- Expensive operations are infrequent
- Operations naturally "pay" for future expensive operations
- Data structure maintains balance over time
- Interested in average performance over sequences

❌ **Not suitable when:**
- Need guaranteed per-operation bounds
- Single operation performance is critical
- Worst-case timing is important (real-time systems)

## 🔧 Analysis Techniques

### Aggregate Method
1. Find total cost of n operations
2. Divide by n to get amortized cost
3. Example: T(n) = cn, so amortized cost = c

### Accounting Method
1. Assign amortized cost to each operation
2. Ensure credit never goes negative
3. Expensive operations use accumulated credit

### Potential Method
1. Define potential function Φ(D)
2. Amortized cost = actual cost + ΔΦ
3. Φ increases when data structure becomes "expensive"

## 🎯 Applications

1. **Data Structures**: Dynamic arrays, hash tables, splay trees
2. **Memory Management**: Garbage collection analysis
3. **Network Algorithms**: Link-state routing updates
4. **Database Systems**: B-tree maintenance operations

## 🔗 Related Topics

- [[Big O Notation]] - Asymptotic analysis framework
- [[Time Complexity]] - Individual operation analysis
- [[Data Structures]] - Structures benefiting from amortized analysis
- [[Dynamic Arrays]] - Classic amortized analysis example

---

*See also: [[Big O Notation]], [[Time Complexity]], [[algorithms_and_ds]]*