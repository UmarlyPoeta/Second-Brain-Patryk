# Prim Algorithm

> Greedy algorithm for finding minimum spanning tree by growing the tree one vertex at a time, always adding the minimum weight edge that connects a tree vertex to a non-tree vertex.

## 📖 Definition

Prim's algorithm builds a minimum spanning tree by starting with an arbitrary vertex and repeatedly adding the minimum weight edge that connects a vertex in the current tree to a vertex outside the tree.

## ⚡ Time & Space Complexity

- **Time Complexity**: 
  - O(V²) with simple array implementation
  - O(E log V) with binary heap
  - O(E + V log V) with Fibonacci heap
- **Space Complexity**: O(V) for priority queue and arrays
- **Efficient for**: Dense graphs

## 🔑 Algorithm Steps

1. **Start**: Choose arbitrary starting vertex
2. **Initialize**: Add starting vertex to MST
3. **Grow**: Repeatedly add minimum weight edge connecting MST to non-MST vertex
4. **Continue**: Until all vertices are in MST

## 🐍 Python Implementation

```python
import heapq
from collections import defaultdict

def prim_mst_simple(graph, start):
    """Simple Prim's algorithm implementation"""
    # Get all vertices
    vertices = set([start])
    for u in graph:
        vertices.add(u)
        for v, _ in graph[u]:
            vertices.add(v)
    
    mst_edges = []
    total_weight = 0
    visited = {start}
    
    # Priority queue of (weight, u, v) for edges from visited vertices
    edge_queue = []
    
    # Add all edges from start vertex
    for neighbor, weight in graph.get(start, []):
        heapq.heappush(edge_queue, (weight, start, neighbor))
    
    while edge_queue and len(visited) < len(vertices):
        weight, u, v = heapq.heappop(edge_queue)
        
        # Skip if both vertices already in MST
        if v in visited:
            continue
        
        # Add edge to MST
        mst_edges.append((u, v, weight))
        total_weight += weight
        visited.add(v)
        
        # Add all edges from newly added vertex
        for neighbor, edge_weight in graph.get(v, []):
            if neighbor not in visited:
                heapq.heappush(edge_queue, (edge_weight, v, neighbor))
    
    return mst_edges, total_weight

def prim_mst_with_keys(graph):
    """Prim's algorithm using key array approach"""
    vertices = set()
    for u in graph:
        vertices.add(u)
        for v, _ in graph[u]:
            vertices.add(v)
    
    vertex_list = sorted(list(vertices))
    n = len(vertex_list)
    vertex_to_index = {v: i for i, v in enumerate(vertex_list)}
    
    # Initialize arrays
    key = [float('inf')] * n  # Minimum weight to connect vertex to MST
    parent = [-1] * n         # Parent in MST
    in_mst = [False] * n      # Whether vertex is in MST
    
    # Start from vertex 0
    key[0] = 0
    mst_edges = []
    total_weight = 0
    
    for _ in range(n):
        # Find minimum key vertex not in MST
        min_key = float('inf')
        min_vertex = -1
        
        for v in range(n):
            if not in_mst[v] and key[v] < min_key:
                min_key = key[v]
                min_vertex = v
        
        # Add vertex to MST
        in_mst[min_vertex] = True
        
        if parent[min_vertex] != -1:
            u_name = vertex_list[parent[min_vertex]]
            v_name = vertex_list[min_vertex]
            mst_edges.append((u_name, v_name, key[min_vertex]))
            total_weight += key[min_vertex]
        
        # Update keys of adjacent vertices
        current_vertex = vertex_list[min_vertex]
        for neighbor, weight in graph.get(current_vertex, []):
            neighbor_idx = vertex_to_index[neighbor]
            
            if not in_mst[neighbor_idx] and weight < key[neighbor_idx]:
                key[neighbor_idx] = weight
                parent[neighbor_idx] = min_vertex
    
    return mst_edges, total_weight

class PrimMST:
    """Graph class with Prim's MST implementation"""
    
    def __init__(self):
        self.graph = defaultdict(list)
        self.vertices = set()
    
    def add_edge(self, u, v, weight):
        """Add undirected edge"""
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))
        self.vertices.update([u, v])
    
    def find_mst(self, start=None):
        """Find MST using Prim's algorithm"""
        if not self.vertices:
            return [], 0
        
        if start is None:
            start = next(iter(self.vertices))
        
        return prim_mst_simple(self.graph, start)
    
    def print_mst(self, start=None):
        mst_edges, total_weight = self.find_mst(start)
        
        print("Minimum Spanning Tree (Prim's Algorithm):")
        print("Edges in MST:")
        for u, v, weight in mst_edges:
            print(f"  {u} -- {v}: {weight}")
        print(f"Total weight: {total_weight}")

def prim_step_by_step(graph, start):
    """Visualize Prim's algorithm step by step"""
    vertices = set([start])
    for u in graph:
        vertices.add(u)
        for v, _ in graph[u]:
            vertices.add(v)
    
    mst_edges = []
    visited = {start}
    edge_queue = []
    
    print(f"Prim's Algorithm Starting from {start}:")
    print(f"Step 0: Start with vertex {start}")
    
    # Add initial edges
    for neighbor, weight in graph.get(start, []):
        heapq.heappush(edge_queue, (weight, start, neighbor))
    
    step = 1
    while edge_queue and len(visited) < len(vertices):
        weight, u, v = heapq.heappop(edge_queue)
        
        if v in visited:
            print(f"Step {step}: Skip edge ({u}, {v}, {weight}) - {v} already in MST")
            continue
        
        # Add edge to MST
        mst_edges.append((u, v, weight))
        visited.add(v)
        
        print(f"Step {step}: Add edge ({u}, {v}, {weight}) to MST")
        print(f"         Vertices in MST: {sorted(visited)}")
        
        # Add new edges from v
        new_edges = []
        for neighbor, edge_weight in graph.get(v, []):
            if neighbor not in visited:
                heapq.heappush(edge_queue, (edge_weight, v, neighbor))
                new_edges.append((v, neighbor, edge_weight))
        
        if new_edges:
            print(f"         New candidate edges: {new_edges}")
        
        step += 1
        print()
    
    total_weight = sum(weight for _, _, weight in mst_edges)
    print(f"Final MST edges: {mst_edges}")
    print(f"Total weight: {total_weight}")
    
    return mst_edges, total_weight

# Example usage
if __name__ == "__main__":
    # Example graph
    graph = {
        'A': [('B', 2), ('C', 3)],
        'B': [('A', 2), ('C', 1), ('D', 1), ('E', 4)],
        'C': [('A', 3), ('B', 1), ('F', 5)],
        'D': [('B', 1), ('E', 1)],
        'E': [('B', 4), ('D', 1), ('F', 1)],
        'F': [('C', 5), ('E', 1)]
    }
    
    print("Original graph:", dict(graph))
    print()
    
    # Find MST
    mst_edges, total_weight = prim_mst_simple(graph, 'A')
    print("MST using Prim's algorithm:")
    for u, v, weight in mst_edges:
        print(f"  {u} -- {v}: {weight}")
    print(f"Total weight: {total_weight}")
    print()
    
    # Step-by-step visualization
    prim_step_by_step(graph, 'A')
    
    # Using class
    print("\nUsing PrimMST class:")
    g = PrimMST()
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'C', 1)
    g.add_edge('B', 'D', 1)
    g.add_edge('B', 'E', 4)
    g.add_edge('C', 'F', 5)
    g.add_edge('D', 'E', 1)
    g.add_edge('E', 'F', 1)
    
    g.print_mst()
```

## 🎯 Applications

1. **Network Design**: Minimum cost network connections
2. **Circuit Design**: Minimize wire length in circuits
3. **Approximation Algorithms**: TSP 2-approximation
4. **Cluster Analysis**: Hierarchical clustering
5. **Image Segmentation**: Computer vision applications

## 🆚 Prim vs Kruskal

| Aspect | Prim | Kruskal |
|--------|------|---------|
| **Approach** | Vertex-based (grow tree) | Edge-based (sort edges) |
| **Data Structure** | Priority Queue | Union-Find |
| **Time (dense)** | O(V²) | O(E log E) |
| **Time (sparse)** | O(E log V) | O(E log E) |
| **Memory** | O(V) | O(V) |
| **Parallelization** | Easier | More difficult |
| **Online** | Can handle dynamic edge weights | Requires all edges upfront |

## 💡 Key Insights

1. **Cut Property**: MST must include minimum weight edge crossing any cut
2. **Greedy Choice**: Locally optimal choice leads to global optimum
3. **Vertex Growth**: Tree grows by one vertex at each step
4. **Priority Queue**: Efficiently finds minimum weight edge

## 🔧 Implementation Variants

1. **Array-based**: Simple O(V²) implementation
2. **Binary Heap**: O(E log V) using priority queue
3. **Fibonacci Heap**: O(E + V log V) theoretical optimum
4. **Dense Graph**: Prefer array-based approach

## 🎯 When to Use Prim

✅ **Use Prim when:**
- Graph is dense (E ≈ V²)
- Need to start from specific vertex
- Working with dynamic edge weights
- Memory for Union-Find is limited

❌ **Use Kruskal when:**
- Graph is sparse
- All edges known upfront
- Edge sorting is acceptable

## 🔗 Related Topics

- [[Kruskal Algorithm]] - Alternative MST algorithm
- [[Dijkstra Algorithm]] - Similar priority queue approach
- [[Greedy Algorithms]] - Algorithm design paradigm
- [[Union-Find]] - Used in Kruskal's algorithm

---

*See also: [[Kruskal Algorithm]], [[Dijkstra Algorithm]], [[algorithms_and_ds]]*