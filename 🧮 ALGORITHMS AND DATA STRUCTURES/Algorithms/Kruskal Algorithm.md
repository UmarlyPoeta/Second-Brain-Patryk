# Kruskal Algorithm

> Greedy algorithm for finding minimum spanning tree by selecting edges in order of increasing weight, using Union-Find to detect cycles.

## 📖 Definition

Kruskal's algorithm finds a minimum spanning tree for a connected weighted graph by selecting edges in order of increasing weight, adding an edge to the MST only if it doesn't create a cycle.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(E log E) where E = number of edges
- **Space Complexity**: O(V) for Union-Find data structure
- **Bottleneck**: Sorting edges by weight
- **Efficient for**: Sparse graphs

## 🔑 Algorithm Steps

1. **Sort**: Sort all edges by weight in ascending order
2. **Initialize**: Create Union-Find for cycle detection
3. **Iterate**: For each edge, add to MST if it doesn't create cycle
4. **Stop**: When MST has V-1 edges

## 🐍 Python Implementation

```python
class UnionFind:
    """Union-Find (Disjoint Set) data structure"""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n
    
    def find(self, x):
        """Find root with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same component
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.components -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)

def kruskal_mst(edges, num_vertices):
    """
    Kruskal's algorithm for MST
    edges: list of (weight, u, v) tuples
    Returns: list of MST edges and total weight
    """
    # Sort edges by weight
    sorted_edges = sorted(edges)
    
    # Initialize Union-Find
    uf = UnionFind(num_vertices)
    mst_edges = []
    total_weight = 0
    
    for weight, u, v in sorted_edges:
        # Add edge if it doesn't create cycle
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            # Stop when we have V-1 edges
            if len(mst_edges) == num_vertices - 1:
                break
    
    return mst_edges, total_weight

def kruskal_with_graph_dict(graph):
    """Kruskal's algorithm with graph as adjacency list"""
    # Extract edges from graph
    edges = []
    vertices = set()
    
    for u in graph:
        vertices.add(u)
        for v, weight in graph[u]:
            vertices.add(v)
            # Add edge only once (assuming undirected graph)
            if u < v:  # Avoid duplicate edges
                edges.append((weight, u, v))
    
    # Create vertex mapping
    vertex_list = sorted(list(vertices))
    vertex_to_index = {v: i for i, v in enumerate(vertex_list)}
    
    # Convert to indexed edges
    indexed_edges = [(weight, vertex_to_index[u], vertex_to_index[v]) 
                     for weight, u, v in edges]
    
    # Run Kruskal's algorithm
    mst_edges, total_weight = kruskal_mst(indexed_edges, len(vertices))
    
    # Convert back to vertex names
    named_mst_edges = [(vertex_list[u], vertex_list[v], weight) 
                       for u, v, weight in mst_edges]
    
    return named_mst_edges, total_weight

class Graph:
    """Graph class with Kruskal's MST implementation"""
    
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = []
    
    def add_edge(self, u, v, weight):
        self.edges.append((weight, u, v))
    
    def kruskal_mst(self):
        """Find MST using Kruskal's algorithm"""
        mst_edges, total_weight = kruskal_mst(self.edges, self.vertices)
        return mst_edges, total_weight
    
    def print_mst(self):
        mst_edges, total_weight = self.kruskal_mst()
        
        print("Minimum Spanning Tree (Kruskal's Algorithm):")
        print("Edges in MST:")
        for u, v, weight in mst_edges:
            print(f"  {u} -- {v}: {weight}")
        print(f"Total weight: {total_weight}")

# Visualization helper
def visualize_kruskal_steps(edges, num_vertices):
    """Show step-by-step MST construction"""
    sorted_edges = sorted(edges)
    uf = UnionFind(num_vertices)
    mst_edges = []
    
    print("Kruskal's Algorithm Steps:")
    print("Edges sorted by weight:", sorted_edges)
    print()
    
    for i, (weight, u, v) in enumerate(sorted_edges):
        print(f"Step {i + 1}: Consider edge ({u}, {v}) with weight {weight}")
        
        if uf.connected(u, v):
            print(f"  Rejected: Would create cycle (vertices {u} and {v} already connected)")
        else:
            uf.union(u, v)
            mst_edges.append((u, v, weight))
            print(f"  Accepted: Added to MST")
        
        print(f"  MST edges so far: {len(mst_edges)}")
        
        if len(mst_edges) == num_vertices - 1:
            print(f"  MST complete with {num_vertices - 1} edges")
            break
        print()
    
    return mst_edges

# Example usage
if __name__ == "__main__":
    # Example 1: Simple graph
    edges = [
        (10, 0, 1), (6, 0, 2), (5, 0, 3),
        (15, 1, 3), (4, 2, 3)
    ]
    
    print("Graph edges (weight, u, v):", edges)
    mst_edges, total_weight = kruskal_mst(edges, 4)
    print("MST edges:", mst_edges)
    print("Total weight:", total_weight)
    print()
    
    # Example 2: Step-by-step visualization
    print("Step-by-step MST construction:")
    visualize_kruskal_steps(edges, 4)
    
    # Example 3: Named vertices
    graph = {
        'A': [('B', 10), ('C', 6), ('D', 5)],
        'B': [('A', 10), ('D', 15)],
        'C': [('A', 6), ('D', 4)],
        'D': [('A', 5), ('B', 15), ('C', 4)]
    }
    
    named_mst, weight = kruskal_with_graph_dict(graph)
    print(f"\nNamed graph MST: {named_mst}")
    print(f"Total weight: {weight}")
```

## 🎯 Applications

1. **Network Design**: Minimum cost to connect all nodes
2. **Circuit Design**: Minimum wire length connections
3. **Cluster Analysis**: Hierarchical clustering
4. **Approximation Algorithms**: TSP approximation
5. **Image Segmentation**: Computer vision applications

## 🆚 Kruskal vs Prim

| Aspect | Kruskal | Prim |
|--------|---------|------|
| **Approach** | Edge-based | Vertex-based |
| **Data Structure** | Union-Find | Priority Queue |
| **Time** | O(E log E) | O(V² log V) |
| **Best For** | Sparse graphs | Dense graphs |
| **Memory** | O(V) | O(V) |
| **Parallelizable** | Difficult | Easier |

## 💡 Key Insights

1. **Greedy Choice**: Always select minimum weight edge that doesn't create cycle
2. **Union-Find**: Efficient cycle detection in O(α(V)) amortized time
3. **Edge-Centric**: Considers edges globally rather than growing from vertex
4. **Optimal**: Greedy choice leads to globally optimal solution

## 🔧 Optimizations

1. **Union-Find Optimizations**: Path compression and union by rank
2. **Edge Preprocessing**: Filter obviously non-MST edges
3. **Parallel Sorting**: Distribute edge sorting
4. **Early Termination**: Stop when MST is complete

## 🔗 Related Topics

- [[Prim Algorithm]] - Alternative MST algorithm
- [[Union-Find]] - Data structure for cycle detection
- [[Greedy Algorithms]] - Algorithm design paradigm
- [[Graph Algorithms]] - Related graph processing

---

*See also: [[Prim Algorithm]], [[Greedy Algorithms]], [[algorithms_and_ds]]*