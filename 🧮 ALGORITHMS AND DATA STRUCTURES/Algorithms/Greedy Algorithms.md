# Greedy Algorithms

> Problem-solving approach that makes locally optimal choices at each step, hoping to find a global optimum solution.

## 📖 Definition

Greedy algorithms build solutions piece by piece, always choosing the next piece that offers the most immediate benefit. They never reconsider previous choices.

## 🔑 Key Characteristics

1. **Greedy Choice Property**: Local optimum leads to global optimum
2. **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
3. **No Backtracking**: Once a choice is made, it's never reconsidered

## ⚡ Time Complexity

Generally efficient: O(n log n) due to sorting, or O(n) for simple greedy steps.

## 🎯 Classic Greedy Problems

### 1. Activity Selection Problem
```python
def activity_selection(activities):
    """
    Select maximum number of non-overlapping activities
    activities: list of (start, end) tuples
    """
    # Sort by end time (greedy choice)
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    last_end_time = activities[0][1]
    
    for start, end in activities[1:]:
        if start >= last_end_time:  # No overlap
            selected.append((start, end))
            last_end_time = end
    
    return selected

# Example usage
activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]
result = activity_selection(activities)
print(f"Selected activities: {result}")  # Maximum non-overlapping activities
```

### 2. Fractional Knapsack
```python
def fractional_knapsack(items, capacity):
    """
    items: list of (weight, value) tuples
    capacity: maximum weight capacity
    """
    # Calculate value-to-weight ratio and sort (greedy choice)
    items_with_ratio = [(value/weight, weight, value) for weight, value in items]
    items_with_ratio.sort(reverse=True)  # Sort by ratio descending
    
    total_value = 0
    remaining_capacity = capacity
    
    for ratio, weight, value in items_with_ratio:
        if weight <= remaining_capacity:
            # Take entire item
            total_value += value
            remaining_capacity -= weight
        else:
            # Take fraction of item
            fraction = remaining_capacity / weight
            total_value += value * fraction
            break
    
    return total_value

# Example usage
items = [(10, 60), (20, 100), (30, 120)]  # (weight, value)
capacity = 50
max_value = fractional_knapsack(items, capacity)
print(f"Maximum value: {max_value}")
```

### 3. Huffman Coding
```python
import heapq
from collections import defaultdict, Counter

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_encoding(text):
    """Create Huffman codes for characters"""
    if not text:
        return {}, None
    
    # Count frequency
    freq = Counter(text)
    
    # Create priority queue (min heap)
    heap = [HuffmanNode(char, f) for char, f in freq.items()]
    heapq.heapify(heap)
    
    # Build Huffman tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    root = heap[0]
    
    # Generate codes
    codes = {}
    
    def generate_codes(node, code=""):
        if node:
            if node.char:  # Leaf node
                codes[node.char] = code or "0"  # Handle single character case
            else:
                generate_codes(node.left, code + "0")
                generate_codes(node.right, code + "1")
    
    generate_codes(root)
    return codes, root

# Example usage
text = "hello world"
codes, root = huffman_encoding(text)
print("Huffman codes:", codes)

# Encode text
encoded = ''.join(codes[char] for char in text)
print(f"Original: {text}")
print(f"Encoded: {encoded}")
print(f"Compression ratio: {len(text)*8}/{len(encoded)} = {len(text)*8/len(encoded):.2f}")
```

### 4. Dijkstra's Algorithm (Shortest Path)
```python
import heapq

def dijkstra(graph, start):
    """
    Find shortest paths from start vertex using greedy approach
    graph: adjacency list with weights {vertex: [(neighbor, weight), ...]}
    """
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    
    # Priority queue: (distance, vertex)
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        
        if current_vertex in visited:
            continue
        
        visited.add(current_vertex)
        
        # Check neighbors (greedy choice: always pick minimum distance)
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances

# Example usage
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 1), ('D', 5)],
    'C': [('D', 8), ('E', 10)],
    'D': [('E', 2)],
    'E': []
}

distances = dijkstra(graph, 'A')
print("Shortest distances from A:", distances)
```

## 🎯 When Greedy Works

✅ **Greedy algorithm works when:**
- Problem has greedy choice property
- Problem exhibits optimal substructure
- Local optimum leads to global optimum

❌ **Greedy doesn't work for:**
- 0/1 Knapsack Problem (need Dynamic Programming)
- Traveling Salesman Problem
- Longest Common Subsequence

## 🆚 Greedy vs Other Approaches

| Approach | Time | Optimality | When to Use |
|----------|------|------------|-------------|
| **Greedy** | Fast | Sometimes | Clear greedy choice exists |
| **Dynamic Programming** | Slower | Always* | Overlapping subproblems |
| **Backtracking** | Slowest | Always* | Need all solutions |

*When applicable

## 💡 Greedy Strategy Design Steps

1. **Cast the optimization problem** as one where you make a choice and are left with one subproblem
2. **Prove that there's always an optimal solution** that makes the greedy choice
3. **Demonstrate optimal substructure** by showing that having made the greedy choice, what remains is a subproblem with the property that if you combine an optimal solution to the subproblem with the greedy choice you've made, you get an optimal solution to the original problem

## 🔗 Related Topics

- [[Dynamic Programming]] - Alternative optimization technique
- [[Dijkstra Algorithm]] - Greedy shortest path algorithm
- [[Binary Trees]] - Huffman coding uses trees
- [[Sorting Algorithms]] - Often need sorting for greedy choice

---

*See also: [[Dynamic Programming]], [[Dijkstra Algorithm]], [[algorithms_and_ds]]*