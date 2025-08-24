# Floyd-Warshall Algorithm

> Dynamic programming algorithm for finding shortest paths between all pairs of vertices in a weighted graph, handling negative weights but detecting negative cycles.

## 📖 Definition

The Floyd-Warshall algorithm finds the shortest paths between all pairs of vertices in a weighted graph. It works with both positive and negative edge weights but cannot handle negative cycles (it can detect them though).

## ⚡ Time & Space Complexity

- **Time Complexity**: O(V³) where V = number of vertices
- **Space Complexity**: O(V²) for distance matrix
- **All-Pairs**: Finds shortest paths between every pair of vertices
- **Handles**: Negative edge weights (but not negative cycles)

## 🔑 Key Insight

For each pair of vertices (i,j), consider all possible intermediate vertices k and check if path i→k→j is shorter than direct path i→j.

## 🐍 Python Implementation

```python
def floyd_warshall(graph):
    """Floyd-Warshall algorithm for all-pairs shortest paths"""
    # Get all vertices
    vertices = set()
    for u in graph:
        vertices.add(u)
        for v, _ in graph[u]:
            vertices.add(v)
    
    vertex_list = sorted(list(vertices))
    n = len(vertex_list)
    
    # Create vertex index mapping
    vertex_to_index = {v: i for i, v in enumerate(vertex_list)}
    
    # Initialize distance matrix
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    
    # Distance from vertex to itself is 0
    for i in range(n):
        dist[i][i] = 0
    
    # Fill initial distances from graph
    for u in graph:
        u_idx = vertex_to_index[u]
        for v, weight in graph[u]:
            v_idx = vertex_to_index[v]
            dist[u_idx][v_idx] = weight
    
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist, vertex_list

def floyd_warshall_with_path(graph):
    """Floyd-Warshall with path reconstruction"""
    vertices = set()
    for u in graph:
        vertices.add(u)
        for v, _ in graph[u]:
            vertices.add(v)
    
    vertex_list = sorted(list(vertices))
    n = len(vertex_list)
    vertex_to_index = {v: i for i, v in enumerate(vertex_list)}
    
    # Initialize matrices
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    next_vertex = [[None] * n for _ in range(n)]
    
    # Initialize diagonal and edges
    for i in range(n):
        dist[i][i] = 0
    
    for u in graph:
        u_idx = vertex_to_index[u]
        for v, weight in graph[u]:
            v_idx = vertex_to_index[v]
            dist[u_idx][v_idx] = weight
            next_vertex[u_idx][v_idx] = v_idx
    
    # Floyd-Warshall with path tracking
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_vertex[i][j] = next_vertex[i][k]
    
    return dist, next_vertex, vertex_list

def reconstruct_path(next_vertex, vertex_list, start, end):
    """Reconstruct shortest path between two vertices"""
    vertex_to_index = {v: i for i, v in enumerate(vertex_list)}
    
    if start not in vertex_to_index or end not in vertex_to_index:
        return []
    
    start_idx = vertex_to_index[start]
    end_idx = vertex_to_index[end]
    
    if next_vertex[start_idx][end_idx] is None:
        return []  # No path exists
    
    path = [start]
    current = start_idx
    
    while current != end_idx:
        current = next_vertex[current][end_idx]
        path.append(vertex_list[current])
    
    return path

def detect_negative_cycle(dist):
    """Check if negative cycle exists in result matrix"""
    n = len(dist)
    for i in range(n):
        if dist[i][i] < 0:
            return True
    return False

def print_distance_matrix(dist, vertex_list):
    """Pretty print distance matrix"""
    n = len(vertex_list)
    
    # Print header
    print("     ", end="")
    for v in vertex_list:
        print(f"{v:>6}", end="")
    print()
    
    # Print rows
    for i in range(n):
        print(f"{vertex_list[i]:>4} ", end="")
        for j in range(n):
            if dist[i][j] == float('inf'):
                print("   ∞  ", end="")
            else:
                print(f"{dist[i][j]:>6}", end="")
        print()

class GraphAPSP:
    """All-Pairs Shortest Path using Floyd-Warshall"""
    
    def __init__(self):
        self.graph = defaultdict(list)
    
    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
    
    def shortest_paths(self):
        return floyd_warshall(self.graph)
    
    def path_between(self, start, end):
        dist, next_vertex, vertex_list = floyd_warshall_with_path(self.graph)
        path = reconstruct_path(next_vertex, vertex_list, start, end)
        
        if not path:
            return None, float('inf')
        
        vertex_to_index = {v: i for i, v in enumerate(vertex_list)}
        start_idx = vertex_to_index[start]
        end_idx = vertex_to_index[end]
        
        return path, dist[start_idx][end_idx]

# Example usage
if __name__ == "__main__":
    # Create graph
    graph = {
        'A': [('B', 3), ('C', 8), ('E', -4)],
        'B': [('D', 1), ('E', 7)],
        'C': [('B', 4)],
        'D': [('A', 2), ('C', -5)],
        'E': [('D', 6)]
    }
    
    print("Graph:", dict(graph))
    
    # Find all shortest paths
    dist_matrix, vertices = floyd_warshall(graph)
    print("\nShortest distance matrix:")
    print_distance_matrix(dist_matrix, vertices)
    
    # Check for negative cycles
    has_negative_cycle = detect_negative_cycle(dist_matrix)
    print(f"\nHas negative cycle: {has_negative_cycle}")
    
    # Path reconstruction example
    apsp = GraphAPSP()
    apsp.add_edge('A', 'B', 3)
    apsp.add_edge('A', 'C', 8)
    apsp.add_edge('B', 'D', 1)
    apsp.add_edge('C', 'D', 2)
    
    path, distance = apsp.path_between('A', 'D')
    print(f"\nShortest path from A to D: {path}")
    print(f"Distance: {distance}")
```

## 🎯 Applications

1. **Network Routing**: Find optimal routes between all node pairs
2. **Social Networks**: Analyze connectivity and influence
3. **Game Theory**: Analyze strategies in multi-player games
4. **Urban Planning**: Traffic flow optimization
5. **Bioinformatics**: Protein interaction networks

## 🆚 Floyd-Warshall vs Other Algorithms

| Algorithm | Single/All Pairs | Negative Weights | Time Complexity |
|-----------|------------------|------------------|-----------------|
| **Floyd-Warshall** | All Pairs | ✅ Yes | O(V³) |
| **Dijkstra** | Single Source | ❌ No | O(V log V + E) |
| **Bellman-Ford** | Single Source | ✅ Yes | O(VE) |
| **Johnson's** | All Pairs | ✅ Yes | O(V² log V + VE) |

## 💡 Key Advantages

1. **All Pairs**: Computes shortest paths between all vertex pairs
2. **Negative Weights**: Handles negative edge weights
3. **Simple Implementation**: Easy to understand and code
4. **Dense Graphs**: Efficient for dense graphs (E ≈ V²)

## 🚫 Limitations

1. **Cubic Time**: O(V³) can be slow for large graphs
2. **Negative Cycles**: Cannot handle negative cycles
3. **Memory Usage**: O(V²) space requirement
4. **Sparse Graphs**: Inefficient for sparse graphs

## 🔧 Optimizations

1. **Early Termination**: Stop if no improvements in iteration
2. **Path Compression**: Store only necessary path information
3. **Parallel Implementation**: Parallelize the triple loop
4. **Bit Manipulation**: Use bit operations for boolean matrices

## 🔗 Related Topics

- [[Dijkstra Algorithm]] - Single-source shortest paths
- [[Bellman-Ford Algorithm]] - Single-source with negative weights
- [[Dynamic Programming]] - Core technique used
- [[Graph Algorithms]] - Related graph processing

---

*See also: [[Dijkstra Algorithm]], [[Bellman-Ford Algorithm]], [[algorithms_and_ds]]*