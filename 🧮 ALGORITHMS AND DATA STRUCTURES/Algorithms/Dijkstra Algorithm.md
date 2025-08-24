# Dijkstra Algorithm

> Efficient algorithm for finding the shortest paths from a single source vertex to all other vertices in a weighted graph with non-negative edge weights.

## 📖 Definition

Dijkstra's algorithm finds the shortest path from a source vertex to all other vertices in a weighted graph. It uses a greedy approach, always selecting the unvisited vertex with the smallest known distance from the source.

## ⚡ Time & Space Complexity

- **Time Complexity**: 
  - O(V²) with simple array implementation
  - O((V + E) log V) with binary heap
  - O(V log V + E) with Fibonacci heap
- **Space Complexity**: O(V) for distance and visited arrays
- **Works with**: Non-negative edge weights only

## 🔑 Algorithm Steps

1. **Initialize**: Set distance to source as 0, all others as infinity
2. **Select**: Choose unvisited vertex with minimum distance
3. **Relax**: Update distances to all adjacent vertices
4. **Repeat**: Until all vertices are visited

## 🐍 Python Implementation

```python
import heapq
from collections import defaultdict

def dijkstra(graph, start):
    """Dijkstra's algorithm using priority queue"""
    # Initialize distances and visited set
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    
    # Priority queue: (distance, vertex)
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        
        # Skip if already visited
        if current_vertex in visited:
            continue
        
        visited.add(current_vertex)
        
        # Check neighbors
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            # If shorter path found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances

def dijkstra_with_path(graph, start, end):
    """Dijkstra with path reconstruction"""
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    previous = {vertex: None for vertex in graph}
    
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        
        if current_vertex in visited:
            continue
        
        visited.add(current_vertex)
        
        # Early termination if we reached the target
        if current_vertex == end:
            break
        
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return distances[end], path if path[0] == start else []

class Graph:
    def __init__(self):
        self.vertices = defaultdict(list)
    
    def add_edge(self, u, v, weight):
        self.vertices[u].append((v, weight))
    
    def dijkstra_shortest_path(self, start):
        return dijkstra(self.vertices, start)

# Example usage
if __name__ == "__main__":
    # Create graph
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('C', 1), ('D', 5)],
        'C': [('D', 8), ('E', 10)],
        'D': [('E', 2)],
        'E': []
    }
    
    distances = dijkstra(graph, 'A')
    print("Shortest distances from A:", distances)
    
    distance, path = dijkstra_with_path(graph, 'A', 'E')
    print(f"Shortest path from A to E: {path} (distance: {distance})")
```

## ☕ Java Implementation

```java
import java.util.*;

public class DijkstraAlgorithm {
    
    static class Edge {
        int target, weight;
        
        Edge(int target, int weight) {
            this.target = target;
            this.weight = weight;
        }
    }
    
    static class Node implements Comparable<Node> {
        int vertex, distance;
        
        Node(int vertex, int distance) {
            this.vertex = vertex;
            this.distance = distance;
        }
        
        public int compareTo(Node other) {
            return Integer.compare(this.distance, other.distance);
        }
    }
    
    public static int[] dijkstra(List<List<Edge>> graph, int start) {
        int n = graph.size();
        int[] distances = new int[n];
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[start] = 0;
        
        PriorityQueue<Node> pq = new PriorityQueue<>();
        pq.offer(new Node(start, 0));
        boolean[] visited = new boolean[n];
        
        while (!pq.isEmpty()) {
            Node current = pq.poll();
            int u = current.vertex;
            
            if (visited[u]) continue;
            visited[u] = true;
            
            for (Edge edge : graph.get(u)) {
                int v = edge.target;
                int weight = edge.weight;
                
                if (distances[u] + weight < distances[v]) {
                    distances[v] = distances[u] + weight;
                    pq.offer(new Node(v, distances[v]));
                }
            }
        }
        
        return distances;
    }
    
    public static List<Integer> getPath(List<List<Edge>> graph, int start, int end) {
        int n = graph.size();
        int[] distances = new int[n];
        int[] previous = new int[n];
        Arrays.fill(distances, Integer.MAX_VALUE);
        Arrays.fill(previous, -1);
        distances[start] = 0;
        
        PriorityQueue<Node> pq = new PriorityQueue<>();
        pq.offer(new Node(start, 0));
        boolean[] visited = new boolean[n];
        
        while (!pq.isEmpty()) {
            Node current = pq.poll();
            int u = current.vertex;
            
            if (visited[u]) continue;
            visited[u] = true;
            
            if (u == end) break; // Early termination
            
            for (Edge edge : graph.get(u)) {
                int v = edge.target;
                int weight = edge.weight;
                
                if (distances[u] + weight < distances[v]) {
                    distances[v] = distances[u] + weight;
                    previous[v] = u;
                    pq.offer(new Node(v, distances[v]));
                }
            }
        }
        
        // Reconstruct path
        List<Integer> path = new ArrayList<>();
        int current = end;
        while (current != -1) {
            path.add(current);
            current = previous[current];
        }
        Collections.reverse(path);
        
        return path.get(0) == start ? path : new ArrayList<>();
    }
    
    public static void main(String[] args) {
        // Create graph: 0->1(4), 0->2(2), 1->2(1), 1->3(5), 2->3(8), 2->4(10), 3->4(2)
        int n = 5;
        List<List<Edge>> graph = new ArrayList<>();
        
        for (int i = 0; i < n; i++) {
            graph.add(new ArrayList<>());
        }
        
        graph.get(0).add(new Edge(1, 4));
        graph.get(0).add(new Edge(2, 2));
        graph.get(1).add(new Edge(2, 1));
        graph.get(1).add(new Edge(3, 5));
        graph.get(2).add(new Edge(3, 8));
        graph.get(2).add(new Edge(4, 10));
        graph.get(3).add(new Edge(4, 2));
        
        int[] distances = dijkstra(graph, 0);
        System.out.println("Shortest distances from vertex 0: " + Arrays.toString(distances));
        
        List<Integer> path = getPath(graph, 0, 4);
        System.out.println("Shortest path from 0 to 4: " + path);
    }
}
```

## 🎯 Applications

1. **GPS Navigation**: Finding shortest routes
2. **Network Routing**: Internet packet routing protocols
3. **Social Networks**: Finding degrees of separation
4. **Game AI**: Pathfinding in games
5. **Flight Connections**: Cheapest flight paths

## 🆚 Dijkstra vs Other Shortest Path Algorithms

| Algorithm | Negative Weights | All Pairs | Time Complexity |
|-----------|------------------|-----------|-----------------|
| **Dijkstra** | ❌ No | ❌ Single Source | O(V log V + E) |
| **Bellman-Ford** | ✅ Yes | ❌ Single Source | O(VE) |
| **Floyd-Warshall** | ✅ Yes | ✅ All Pairs | O(V³) |
| **A*** | ❌ No | ❌ Single Target | O(b^d) |

## 💡 Key Insights

1. **Greedy Choice**: Always picks globally optimal choice
2. **Relaxation**: Updates distances when shorter path found
3. **Priority Queue**: Efficiently gets minimum distance vertex
4. **Optimal Substructure**: Shortest path has shortest subpaths

## 🚫 Limitations

1. **Non-negative Weights**: Cannot handle negative edge weights
2. **Single Source**: Doesn't find all-pairs shortest paths efficiently
3. **Memory Usage**: Requires storing all distances

## 🔗 Related Topics

- [[Bellman-Ford Algorithm]] - Handles negative weights
- [[Floyd-Warshall Algorithm]] - All-pairs shortest paths
- [[Graphs]] - Underlying data structure
- [[Priority Queues]] - Essential for efficient implementation

---

*See also: [[Bellman-Ford Algorithm]], [[Floyd-Warshall Algorithm]], [[algorithms_and_ds]]*