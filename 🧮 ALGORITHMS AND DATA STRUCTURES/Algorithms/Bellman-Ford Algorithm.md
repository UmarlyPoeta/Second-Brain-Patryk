# Bellman-Ford Algorithm

> Single-source shortest path algorithm that can handle graphs with negative edge weights and detect negative cycles.

## 📖 Definition

The Bellman-Ford algorithm computes shortest paths from a single source vertex to all other vertices in a weighted graph. Unlike Dijkstra's algorithm, it can handle graphs with negative edge weights and can detect negative cycles.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(V × E) where V = vertices, E = edges
- **Space Complexity**: O(V) for distance array
- **Handles**: Negative edge weights
- **Detects**: Negative cycles

## 🔑 Algorithm Steps

1. **Initialize**: Set distance to source as 0, all others as infinity
2. **Relax**: For V-1 iterations, relax all edges
3. **Check**: Run one more iteration to detect negative cycles

## 🐍 Python Implementation

```python
def bellman_ford(graph, start):
    """
    Bellman-Ford algorithm for shortest paths
    graph: dict of {vertex: [(neighbor, weight), ...]}
    Returns: (distances, has_negative_cycle)
    """
    # Get all vertices
    vertices = set(graph.keys())
    for vertex in graph:
        for neighbor, _ in graph[vertex]:
            vertices.add(neighbor)
    
    # Initialize distances
    distances = {vertex: float('infinity') for vertex in vertices}
    distances[start] = 0
    
    # Relax edges V-1 times
    for _ in range(len(vertices) - 1):
        for u in graph:
            if distances[u] != float('infinity'):
                for v, weight in graph[u]:
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
    
    # Check for negative cycles
    has_negative_cycle = False
    for u in graph:
        if distances[u] != float('infinity'):
            for v, weight in graph[u]:
                if distances[u] + weight < distances[v]:
                    has_negative_cycle = True
                    break
        if has_negative_cycle:
            break
    
    return distances, has_negative_cycle

def bellman_ford_with_path(graph, start, end):
    """Bellman-Ford with path reconstruction"""
    vertices = set(graph.keys())
    for vertex in graph:
        for neighbor, _ in graph[vertex]:
            vertices.add(neighbor)
    
    distances = {vertex: float('infinity') for vertex in vertices}
    previous = {vertex: None for vertex in vertices}
    distances[start] = 0
    
    # Relax edges V-1 times
    for _ in range(len(vertices) - 1):
        for u in graph:
            if distances[u] != float('infinity'):
                for v, weight in graph[u]:
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        previous[v] = u
    
    # Check for negative cycles
    for u in graph:
        if distances[u] != float('infinity'):
            for v, weight in graph[u]:
                if distances[u] + weight < distances[v]:
                    return None, []  # Negative cycle detected
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return distances[end], path if path[0] == start else []

def detect_negative_cycle(graph):
    """Detect if graph contains negative cycle"""
    # Pick any vertex as source
    vertices = list(graph.keys())
    if not vertices:
        return False
    
    _, has_cycle = bellman_ford(graph, vertices[0])
    return has_cycle

# Example usage
if __name__ == "__main__":
    # Graph with negative edges but no negative cycle
    graph1 = {
        'A': [('B', -1), ('C', 4)],
        'B': [('C', 3), ('D', 2), ('E', 2)],
        'C': [],
        'D': [('B', 1), ('C', 5)],
        'E': [('D', -3)]
    }
    
    distances, has_cycle = bellman_ford(graph1, 'A')
    print("Graph 1 - Distances:", distances)
    print("Has negative cycle:", has_cycle)
    
    # Graph with negative cycle
    graph2 = {
        'A': [('B', 1)],
        'B': [('C', -2)],
        'C': [('A', -1)]
    }
    
    distances2, has_cycle2 = bellman_ford(graph2, 'A')
    print("\nGraph 2 - Has negative cycle:", has_cycle2)
```

## ☕ Java Implementation

```java
import java.util.*;

public class BellmanFordAlgorithm {
    
    static class Edge {
        int source, destination, weight;
        
        Edge(int source, int destination, int weight) {
            this.source = source;
            this.destination = destination;
            this.weight = weight;
        }
    }
    
    static class Graph {
        int vertices;
        List<Edge> edges;
        
        Graph(int vertices) {
            this.vertices = vertices;
            this.edges = new ArrayList<>();
        }
        
        void addEdge(int source, int destination, int weight) {
            edges.add(new Edge(source, destination, weight));
        }
    }
    
    public static int[] bellmanFord(Graph graph, int source) {
        int V = graph.vertices;
        int[] distances = new int[V];
        
        // Initialize distances
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[source] = 0;
        
        // Relax all edges V-1 times
        for (int i = 1; i < V; i++) {
            for (Edge edge : graph.edges) {
                int u = edge.source;
                int v = edge.destination;
                int weight = edge.weight;
                
                if (distances[u] != Integer.MAX_VALUE && 
                    distances[u] + weight < distances[v]) {
                    distances[v] = distances[u] + weight;
                }
            }
        }
        
        // Check for negative cycles
        for (Edge edge : graph.edges) {
            int u = edge.source;
            int v = edge.destination;
            int weight = edge.weight;
            
            if (distances[u] != Integer.MAX_VALUE && 
                distances[u] + weight < distances[v]) {
                System.out.println("Graph contains negative cycle");
                return null;
            }
        }
        
        return distances;
    }
    
    public static void printDistances(int[] distances, int source) {
        System.out.println("Shortest distances from vertex " + source + ":");
        for (int i = 0; i < distances.length; i++) {
            System.out.println("Vertex " + i + ": " + 
                (distances[i] == Integer.MAX_VALUE ? "∞" : distances[i]));
        }
    }
    
    public static void main(String[] args) {
        Graph graph = new Graph(5);
        graph.addEdge(0, 1, -1);
        graph.addEdge(0, 2, 4);
        graph.addEdge(1, 2, 3);
        graph.addEdge(1, 3, 2);
        graph.addEdge(1, 4, 2);
        graph.addEdge(3, 2, 5);
        graph.addEdge(3, 1, 1);
        graph.addEdge(4, 3, -3);
        
        int[] distances = bellmanFord(graph, 0);
        if (distances != null) {
            printDistances(distances, 0);
        }
    }
}
```

## 🎯 When to Use Bellman-Ford

✅ **Use Bellman-Ford when:**
- Graph has negative edge weights
- Need to detect negative cycles
- Simple implementation preferred
- Distributed computing (easy to parallelize)

❌ **Don't use when:**
- All weights are non-negative (use Dijkstra instead)
- Need all-pairs shortest paths (use Floyd-Warshall)
- Performance is critical with large graphs

## 🆚 Bellman-Ford vs Other Algorithms

| Algorithm | Negative Weights | Negative Cycles | Time Complexity |
|-----------|------------------|-----------------|-----------------|
| **Bellman-Ford** | ✅ Yes | ✅ Detects | O(VE) |
| **Dijkstra** | ❌ No | ❌ No | O(V log V + E) |
| **Floyd-Warshall** | ✅ Yes | ✅ Detects | O(V³) |
| **SPFA** | ✅ Yes | ✅ Detects | O(VE) average |

## 💡 Key Insights

1. **Relaxation**: Core operation updating distances
2. **V-1 Iterations**: Sufficient for shortest paths without cycles
3. **Negative Cycle Detection**: Extra iteration reveals cycles
4. **Optimal Substructure**: Builds optimal solution incrementally

## 🔧 Optimizations

1. **Early Termination**: Stop if no updates in iteration
2. **SPFA (Shortest Path Faster Algorithm)**: Queue-based optimization
3. **Parallel Implementation**: Distribute edge relaxation

## 🎯 Applications

1. **Currency Arbitrage**: Detecting profitable exchange cycles
2. **Network Routing**: Internet routing with varying costs
3. **Game Theory**: Analyzing game strategies
4. **Economics**: Market analysis with negative costs

## 🔗 Related Topics

- [[Dijkstra Algorithm]] - Faster for non-negative weights
- [[Floyd-Warshall Algorithm]] - All-pairs shortest paths
- [[Graphs]] - Underlying data structure
- [[Topological Sort]] - Alternative for DAGs

---

*See also: [[Dijkstra Algorithm]], [[Floyd-Warshall Algorithm]], [[algorithms_and_ds]]*