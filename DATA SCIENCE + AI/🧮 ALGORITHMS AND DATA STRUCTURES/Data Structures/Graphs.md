# Graphs

> Non-linear data structure consisting of vertices (nodes) connected by edges, used to represent relationships and networks in computer science and real-world applications.

## 📖 Definition

A graph G = (V, E) is a collection of vertices (V) and edges (E) where each edge connects two vertices. Graphs are fundamental structures for modeling relationships, networks, and many real-world problems.

## 🔗 Graph Terminology

- **Vertex/Node**: Individual element in the graph
- **Edge**: Connection between two vertices
- **Adjacent**: Two vertices connected by an edge
- **Degree**: Number of edges connected to a vertex
- **Path**: Sequence of vertices connected by edges
- **Cycle**: Path that starts and ends at the same vertex
- **Connected**: Path exists between any two vertices

## 🎯 Types of Graphs

### 1. Directed vs Undirected
- **Directed (Digraph)**: Edges have direction (A → B)
- **Undirected**: Edges are bidirectional (A ↔ B)

### 2. Weighted vs Unweighted
- **Weighted**: Edges have associated weights/costs
- **Unweighted**: All edges have equal weight

### 3. Connected vs Disconnected
- **Connected**: Path exists between every pair of vertices
- **Disconnected**: Some vertices are not reachable from others

### 4. Cyclic vs Acyclic
- **Cyclic**: Contains at least one cycle
- **Acyclic**: No cycles (trees are acyclic connected graphs)

## 💾 Graph Representations

### 1. Adjacency Matrix
2D array where matrix[i][j] = 1 if edge exists from vertex i to j.

### 2. Adjacency List
Array/list of lists where each index contains neighbors of that vertex.

### 3. Edge List
List of all edges as pairs/tuples of vertices.

## 🐍 Python Implementation

```python
from collections import defaultdict, deque

class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)  # Adjacency list
        self.directed = directed
        self.vertices = set()
    
    def add_vertex(self, vertex):
        """Add a vertex to the graph"""
        self.vertices.add(vertex)
    
    def add_edge(self, u, v, weight=1):
        """Add an edge between vertices u and v"""
        self.graph[u].append((v, weight))
        self.vertices.add(u)
        self.vertices.add(v)
        
        # If undirected, add reverse edge
        if not self.directed:
            self.graph[v].append((u, weight))
    
    def remove_edge(self, u, v):
        """Remove edge between u and v"""
        self.graph[u] = [(vertex, weight) for vertex, weight in self.graph[u] 
                        if vertex != v]
        if not self.directed:
            self.graph[v] = [(vertex, weight) for vertex, weight in self.graph[v] 
                            if vertex != u]
    
    def get_neighbors(self, vertex):
        """Get all neighbors of a vertex"""
        return [neighbor for neighbor, _ in self.graph[vertex]]
    
    def get_vertices(self):
        """Get all vertices in the graph"""
        return list(self.vertices)
    
    def get_edges(self):
        """Get all edges in the graph"""
        edges = []
        for vertex in self.graph:
            for neighbor, weight in self.graph[vertex]:
                if self.directed or vertex < neighbor:  # Avoid duplicates for undirected
                    edges.append((vertex, neighbor, weight))
        return edges
    
    def has_edge(self, u, v):
        """Check if edge exists between u and v"""
        return any(neighbor == v for neighbor, _ in self.graph[u])
    
    def degree(self, vertex):
        """Get degree of a vertex"""
        if self.directed:
            # Return (in_degree, out_degree)
            in_degree = sum(1 for v in self.graph for neighbor, _ in self.graph[v] 
                           if neighbor == vertex)
            out_degree = len(self.graph[vertex])
            return (in_degree, out_degree)
        else:
            return len(self.graph[vertex])
    
    def dfs(self, start_vertex, visited=None):
        """Depth-First Search traversal"""
        if visited is None:
            visited = set()
        
        result = []
        
        def dfs_recursive(vertex):
            visited.add(vertex)
            result.append(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start_vertex)
        return result
    
    def dfs_iterative(self, start_vertex):
        """Iterative DFS using stack"""
        visited = set()
        stack = [start_vertex]
        result = []
        
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Add neighbors to stack (reverse order for consistent traversal)
                for neighbor, _ in reversed(self.graph[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def bfs(self, start_vertex):
        """Breadth-First Search traversal"""
        visited = set()
        queue = deque([start_vertex])
        result = []
        
        visited.add(start_vertex)
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def is_connected(self):
        """Check if graph is connected (for undirected graphs)"""
        if not self.vertices:
            return True
        
        start_vertex = next(iter(self.vertices))
        visited_count = len(self.dfs(start_vertex))
        
        return visited_count == len(self.vertices)
    
    def has_cycle(self):
        """Check if graph has a cycle"""
        if self.directed:
            return self._has_cycle_directed()
        else:
            return self._has_cycle_undirected()
    
    def _has_cycle_directed(self):
        """Check cycle in directed graph using DFS"""
        WHITE, GRAY, BLACK = 0, 1, 2
        colors = {vertex: WHITE for vertex in self.vertices}
        
        def dfs_cycle(vertex):
            colors[vertex] = GRAY
            
            for neighbor, _ in self.graph[vertex]:
                if colors[neighbor] == GRAY:  # Back edge found
                    return True
                if colors[neighbor] == WHITE and dfs_cycle(neighbor):
                    return True
            
            colors[vertex] = BLACK
            return False
        
        for vertex in self.vertices:
            if colors[vertex] == WHITE:
                if dfs_cycle(vertex):
                    return True
        
        return False
    
    def _has_cycle_undirected(self):
        """Check cycle in undirected graph using DFS"""
        visited = set()
        
        def dfs_cycle(vertex, parent):
            visited.add(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    if dfs_cycle(neighbor, vertex):
                        return True
                elif neighbor != parent:  # Back edge to non-parent
                    return True
            
            return False
        
        for vertex in self.vertices:
            if vertex not in visited:
                if dfs_cycle(vertex, None):
                    return True
        
        return False
    
    def topological_sort(self):
        """Topological sort for directed acyclic graph (DAG)"""
        if not self.directed:
            raise ValueError("Topological sort only applies to directed graphs")
        
        if self.has_cycle():
            raise ValueError("Graph has cycle - topological sort not possible")
        
        visited = set()
        stack = []
        
        def dfs_topo(vertex):
            visited.add(vertex)
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_topo(neighbor)
            
            stack.append(vertex)
        
        for vertex in self.vertices:
            if vertex not in visited:
                dfs_topo(vertex)
        
        return stack[::-1]  # Reverse to get correct order
    
    def shortest_path_bfs(self, start, end):
        """Find shortest path using BFS (unweighted graph)"""
        if start not in self.vertices or end not in self.vertices:
            return None
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            vertex, path = queue.popleft()
            
            if vertex == end:
                return path
            
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None  # No path found
    
    def display(self):
        """Display the graph"""
        for vertex in sorted(self.vertices):
            neighbors = [f"{neighbor}({weight})" for neighbor, weight in self.graph[vertex]]
            print(f"{vertex}: {' -> '.join(neighbors) if neighbors else 'No neighbors'}")

# Adjacency Matrix Implementation
class GraphMatrix:
    def __init__(self, num_vertices, directed=False):
        self.num_vertices = num_vertices
        self.directed = directed
        self.matrix = [[0] * num_vertices for _ in range(num_vertices)]
    
    def add_edge(self, u, v, weight=1):
        """Add edge between vertices u and v"""
        self.matrix[u][v] = weight
        if not self.directed:
            self.matrix[v][u] = weight
    
    def remove_edge(self, u, v):
        """Remove edge between u and v"""
        self.matrix[u][v] = 0
        if not self.directed:
            self.matrix[v][u] = 0
    
    def has_edge(self, u, v):
        """Check if edge exists between u and v"""
        return self.matrix[u][v] != 0
    
    def get_neighbors(self, vertex):
        """Get all neighbors of a vertex"""
        return [i for i in range(self.num_vertices) if self.matrix[vertex][i] != 0]
    
    def display(self):
        """Display adjacency matrix"""
        print("Adjacency Matrix:")
        for row in self.matrix:
            print(row)

# Example usage and testing
def example_usage():
    # Create undirected graph
    g = Graph(directed=False)
    
    # Add vertices and edges
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]
    for u, v in edges:
        g.add_edge(u, v)
    
    print("Graph representation:")
    g.display()
    
    print(f"\\nDFS from A: {g.dfs('A')}")
    print(f"BFS from A: {g.bfs('A')}")
    print(f"Is connected: {g.is_connected()}")
    print(f"Has cycle: {g.has_cycle()}")
    print(f"Shortest path A to E: {g.shortest_path_bfs('A', 'E')}")
    
    # Create directed graph for topological sort
    dag = Graph(directed=True)
    dag_edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
    for u, v in dag_edges:
        dag.add_edge(u, v)
    
    print(f"\\nTopological sort: {dag.topological_sort()}")

if __name__ == "__main__":
    example_usage()
```

## ☕ Java Implementation

```java
import java.util.*;

public class Graph {
    private Map<Integer, List<Edge>> adjacencyList;
    private boolean directed;
    
    static class Edge {
        int destination;
        int weight;
        
        Edge(int destination, int weight) {
            this.destination = destination;
            this.weight = weight;
        }
        
        Edge(int destination) {
            this(destination, 1);
        }
    }
    
    public Graph(boolean directed) {
        this.directed = directed;
        this.adjacencyList = new HashMap<>();
    }
    
    public void addVertex(int vertex) {
        adjacencyList.putIfAbsent(vertex, new ArrayList<>());
    }
    
    public void addEdge(int source, int destination, int weight) {
        addVertex(source);
        addVertex(destination);
        
        adjacencyList.get(source).add(new Edge(destination, weight));
        
        if (!directed) {
            adjacencyList.get(destination).add(new Edge(source, weight));
        }
    }
    
    public void addEdge(int source, int destination) {
        addEdge(source, destination, 1);
    }
    
    public List<Integer> getNeighbors(int vertex) {
        List<Integer> neighbors = new ArrayList<>();
        if (adjacencyList.containsKey(vertex)) {
            for (Edge edge : adjacencyList.get(vertex)) {
                neighbors.add(edge.destination);
            }
        }
        return neighbors;
    }
    
    public List<Integer> dfs(int startVertex) {
        List<Integer> result = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        dfsHelper(startVertex, visited, result);
        return result;
    }
    
    private void dfsHelper(int vertex, Set<Integer> visited, List<Integer> result) {
        visited.add(vertex);
        result.add(vertex);
        
        if (adjacencyList.containsKey(vertex)) {
            for (Edge edge : adjacencyList.get(vertex)) {
                if (!visited.contains(edge.destination)) {
                    dfsHelper(edge.destination, visited, result);
                }
            }
        }
    }
    
    public List<Integer> dfsIterative(int startVertex) {
        List<Integer> result = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        Stack<Integer> stack = new Stack<>();
        
        stack.push(startVertex);
        
        while (!stack.isEmpty()) {
            int vertex = stack.pop();
            if (!visited.contains(vertex)) {
                visited.add(vertex);
                result.add(vertex);
                
                if (adjacencyList.containsKey(vertex)) {
                    // Add neighbors in reverse order for consistent traversal
                    List<Edge> neighbors = adjacencyList.get(vertex);
                    for (int i = neighbors.size() - 1; i >= 0; i--) {
                        int neighbor = neighbors.get(i).destination;
                        if (!visited.contains(neighbor)) {
                            stack.push(neighbor);
                        }
                    }
                }
            }
        }
        
        return result;
    }
    
    public List<Integer> bfs(int startVertex) {
        List<Integer> result = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        Queue<Integer> queue = new LinkedList<>();
        
        queue.offer(startVertex);
        visited.add(startVertex);
        
        while (!queue.isEmpty()) {
            int vertex = queue.poll();
            result.add(vertex);
            
            if (adjacencyList.containsKey(vertex)) {
                for (Edge edge : adjacencyList.get(vertex)) {
                    if (!visited.contains(edge.destination)) {
                        visited.add(edge.destination);
                        queue.offer(edge.destination);
                    }
                }
            }
        }
        
        return result;
    }
    
    public boolean hasCycle() {
        if (directed) {
            return hasCycleDirected();
        } else {
            return hasCycleUndirected();
        }
    }
    
    private boolean hasCycleDirected() {
        Map<Integer, Integer> colors = new HashMap<>();
        final int WHITE = 0, GRAY = 1, BLACK = 2;
        
        for (int vertex : adjacencyList.keySet()) {
            colors.put(vertex, WHITE);
        }
        
        for (int vertex : adjacencyList.keySet()) {
            if (colors.get(vertex) == WHITE) {
                if (dfsCycleDirected(vertex, colors)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    private boolean dfsCycleDirected(int vertex, Map<Integer, Integer> colors) {
        final int GRAY = 1, BLACK = 2;
        colors.put(vertex, GRAY);
        
        if (adjacencyList.containsKey(vertex)) {
            for (Edge edge : adjacencyList.get(vertex)) {
                int neighbor = edge.destination;
                if (colors.get(neighbor) == GRAY) {
                    return true; // Back edge found
                }
                if (colors.get(neighbor) == 0 && dfsCycleDirected(neighbor, colors)) {
                    return true;
                }
            }
        }
        
        colors.put(vertex, BLACK);
        return false;
    }
    
    private boolean hasCycleUndirected() {
        Set<Integer> visited = new HashSet<>();
        
        for (int vertex : adjacencyList.keySet()) {
            if (!visited.contains(vertex)) {
                if (dfsCycleUndirected(vertex, -1, visited)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    private boolean dfsCycleUndirected(int vertex, int parent, Set<Integer> visited) {
        visited.add(vertex);
        
        if (adjacencyList.containsKey(vertex)) {
            for (Edge edge : adjacencyList.get(vertex)) {
                int neighbor = edge.destination;
                if (!visited.contains(neighbor)) {
                    if (dfsCycleUndirected(neighbor, vertex, visited)) {
                        return true;
                    }
                } else if (neighbor != parent) {
                    return true; // Back edge to non-parent
                }
            }
        }
        
        return false;
    }
    
    public List<Integer> topologicalSort() {
        if (!directed) {
            throw new IllegalArgumentException("Topological sort only applies to directed graphs");
        }
        
        if (hasCycle()) {
            throw new IllegalArgumentException("Graph has cycle - topological sort not possible");
        }
        
        Set<Integer> visited = new HashSet<>();
        Stack<Integer> stack = new Stack<>();
        
        for (int vertex : adjacencyList.keySet()) {
            if (!visited.contains(vertex)) {
                topologicalSortHelper(vertex, visited, stack);
            }
        }
        
        List<Integer> result = new ArrayList<>();
        while (!stack.isEmpty()) {
            result.add(stack.pop());
        }
        
        return result;
    }
    
    private void topologicalSortHelper(int vertex, Set<Integer> visited, Stack<Integer> stack) {
        visited.add(vertex);
        
        if (adjacencyList.containsKey(vertex)) {
            for (Edge edge : adjacencyList.get(vertex)) {
                if (!visited.contains(edge.destination)) {
                    topologicalSortHelper(edge.destination, visited, stack);
                }
            }
        }
        
        stack.push(vertex);
    }
    
    public void display() {
        for (int vertex : adjacencyList.keySet()) {
            System.out.print(vertex + ": ");
            for (Edge edge : adjacencyList.get(vertex)) {
                System.out.print(edge.destination + "(" + edge.weight + ") ");
            }
            System.out.println();
        }
    }
    
    public static void main(String[] args) {
        Graph graph = new Graph(false);
        
        // Add edges
        graph.addEdge(0, 1);
        graph.addEdge(0, 2);
        graph.addEdge(1, 3);
        graph.addEdge(2, 3);
        graph.addEdge(3, 4);
        
        System.out.println("Graph representation:");
        graph.display();
        
        System.out.println("\\nDFS from 0: " + graph.dfs(0));
        System.out.println("BFS from 0: " + graph.bfs(0));
        System.out.println("Has cycle: " + graph.hasCycle());
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <list>
#include <queue>
#include <stack>
#include <unordered_set>
#include <unordered_map>

class Graph {
private:
    std::unordered_map<int, std::list<std::pair<int, int>>> adjacencyList;
    bool directed;
    
public:
    Graph(bool directed = false) : directed(directed) {}
    
    void addVertex(int vertex) {
        if (adjacencyList.find(vertex) == adjacencyList.end()) {
            adjacencyList[vertex] = std::list<std::pair<int, int>>();
        }
    }
    
    void addEdge(int source, int destination, int weight = 1) {
        addVertex(source);
        addVertex(destination);
        
        adjacencyList[source].push_back({destination, weight});
        
        if (!directed) {
            adjacencyList[destination].push_back({source, weight});
        }
    }
    
    std::vector<int> getNeighbors(int vertex) {
        std::vector<int> neighbors;
        if (adjacencyList.find(vertex) != adjacencyList.end()) {
            for (const auto& edge : adjacencyList[vertex]) {
                neighbors.push_back(edge.first);
            }
        }
        return neighbors;
    }
    
    std::vector<int> dfs(int startVertex) {
        std::vector<int> result;
        std::unordered_set<int> visited;
        dfsHelper(startVertex, visited, result);
        return result;
    }
    
private:
    void dfsHelper(int vertex, std::unordered_set<int>& visited, std::vector<int>& result) {
        visited.insert(vertex);
        result.push_back(vertex);
        
        if (adjacencyList.find(vertex) != adjacencyList.end()) {
            for (const auto& edge : adjacencyList[vertex]) {
                if (visited.find(edge.first) == visited.end()) {
                    dfsHelper(edge.first, visited, result);
                }
            }
        }
    }
    
public:
    std::vector<int> dfsIterative(int startVertex) {
        std::vector<int> result;
        std::unordered_set<int> visited;
        std::stack<int> stack;
        
        stack.push(startVertex);
        
        while (!stack.empty()) {
            int vertex = stack.top();
            stack.pop();
            
            if (visited.find(vertex) == visited.end()) {
                visited.insert(vertex);
                result.push_back(vertex);
                
                if (adjacencyList.find(vertex) != adjacencyList.end()) {
                    // Add neighbors to stack in reverse order
                    std::vector<int> neighbors = getNeighbors(vertex);
                    for (auto it = neighbors.rbegin(); it != neighbors.rend(); ++it) {
                        if (visited.find(*it) == visited.end()) {
                            stack.push(*it);
                        }
                    }
                }
            }
        }
        
        return result;
    }
    
    std::vector<int> bfs(int startVertex) {
        std::vector<int> result;
        std::unordered_set<int> visited;
        std::queue<int> queue;
        
        queue.push(startVertex);
        visited.insert(startVertex);
        
        while (!queue.empty()) {
            int vertex = queue.front();
            queue.pop();
            result.push_back(vertex);
            
            if (adjacencyList.find(vertex) != adjacencyList.end()) {
                for (const auto& edge : adjacencyList[vertex]) {
                    if (visited.find(edge.first) == visited.end()) {
                        visited.insert(edge.first);
                        queue.push(edge.first);
                    }
                }
            }
        }
        
        return result;
    }
    
    bool hasCycle() {
        if (directed) {
            return hasCycleDirected();
        } else {
            return hasCycleUndirected();
        }
    }
    
private:
    bool hasCycleDirected() {
        enum Color { WHITE, GRAY, BLACK };
        std::unordered_map<int, Color> colors;
        
        for (const auto& pair : adjacencyList) {
            colors[pair.first] = WHITE;
        }
        
        for (const auto& pair : adjacencyList) {
            if (colors[pair.first] == WHITE) {
                if (dfsCycleDirected(pair.first, colors)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    bool dfsCycleDirected(int vertex, std::unordered_map<int, int>& colors) {
        colors[vertex] = 1; // GRAY
        
        if (adjacencyList.find(vertex) != adjacencyList.end()) {
            for (const auto& edge : adjacencyList[vertex]) {
                int neighbor = edge.first;
                if (colors[neighbor] == 1) { // GRAY - back edge
                    return true;
                }
                if (colors[neighbor] == 0 && dfsCycleDirected(neighbor, colors)) { // WHITE
                    return true;
                }
            }
        }
        
        colors[vertex] = 2; // BLACK
        return false;
    }
    
    bool hasCycleUndirected() {
        std::unordered_set<int> visited;
        
        for (const auto& pair : adjacencyList) {
            if (visited.find(pair.first) == visited.end()) {
                if (dfsCycleUndirected(pair.first, -1, visited)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    bool dfsCycleUndirected(int vertex, int parent, std::unordered_set<int>& visited) {
        visited.insert(vertex);
        
        if (adjacencyList.find(vertex) != adjacencyList.end()) {
            for (const auto& edge : adjacencyList[vertex]) {
                int neighbor = edge.first;
                if (visited.find(neighbor) == visited.end()) {
                    if (dfsCycleUndirected(neighbor, vertex, visited)) {
                        return true;
                    }
                } else if (neighbor != parent) {
                    return true; // Back edge to non-parent
                }
            }
        }
        
        return false;
    }
    
public:
    void display() {
        for (const auto& pair : adjacencyList) {
            std::cout << pair.first << ": ";
            for (const auto& edge : pair.second) {
                std::cout << edge.first << "(" << edge.second << ") ";
            }
            std::cout << std::endl;
        }
    }
};

int main() {
    Graph graph(false);
    
    // Add edges
    graph.addEdge(0, 1);
    graph.addEdge(0, 2);
    graph.addEdge(1, 3);
    graph.addEdge(2, 3);
    graph.addEdge(3, 4);
    
    std::cout << "Graph representation:" << std::endl;
    graph.display();
    
    auto dfsResult = graph.dfs(0);
    std::cout << "\\nDFS from 0: ";
    for (int vertex : dfsResult) {
        std::cout << vertex << " ";
    }
    std::cout << std::endl;
    
    auto bfsResult = graph.bfs(0);
    std::cout << "BFS from 0: ";
    for (int vertex : bfsResult) {
        std::cout << vertex << " ";
    }
    std::cout << std::endl;
    
    std::cout << "Has cycle: " << (graph.hasCycle() ? "Yes" : "No") << std::endl;
    
    return 0;
}
```

## 📊 Complexity Analysis

| Operation | Adjacency List | Adjacency Matrix |
|-----------|----------------|------------------|
| **Add vertex** | O(1) | O(V²) |
| **Add edge** | O(1) | O(1) |
| **Remove edge** | O(V) | O(1) |
| **Check edge** | O(V) | O(1) |
| **Get neighbors** | O(V) | O(V) |
| **DFS/BFS** | O(V + E) | O(V²) |
| **Space** | O(V + E) | O(V²) |

## 🎯 Graph Algorithms

### 1. Shortest Path
- **Dijkstra's Algorithm**: Single-source shortest path (weighted)
- **Bellman-Ford**: Handles negative weights
- **Floyd-Warshall**: All-pairs shortest path

### 2. Minimum Spanning Tree
- **Kruskal's Algorithm**: Edge-based approach
- **Prim's Algorithm**: Vertex-based approach

### 3. Network Flow
- **Ford-Fulkerson**: Maximum flow
- **Edmonds-Karp**: Implementation using BFS

## 🌐 Real-world Applications

1. **Social Networks**: Friend connections, recommendations
2. **Maps/GPS**: Route finding, traffic optimization
3. **Internet**: Network routing, web crawling
4. **Dependency Resolution**: Build systems, package managers
5. **Game AI**: Pathfinding, decision trees
6. **Biology**: Phylogenetic trees, protein interactions
7. **Economics**: Supply chains, market analysis

## 🔗 Related Topics

- [[Binary Trees]] - Special case of graphs (acyclic, connected)
- [[Dijkstra Algorithm]] - Shortest path algorithm
- [[Depth-First Search]] - Graph traversal method
- [[Breadth-First Search]] - Graph traversal method

## 📝 Practice Problems

1. **Clone Graph**: Deep copy of graph
2. **Course Schedule**: Detect cycle in directed graph
3. **Number of Islands**: Connected components in 2D grid
4. **Word Ladder**: Shortest transformation path
5. **Minimum Spanning Tree**: Find MST using Kruskal/Prim
6. **Shortest Path in Binary Matrix**: BFS in grid
7. **Network Delay Time**: Single-source shortest path

---

*See also: [[Binary Trees]], [[Dijkstra Algorithm]], [[DFS]], [[BFS]], [[algorithms_and_ds]]*