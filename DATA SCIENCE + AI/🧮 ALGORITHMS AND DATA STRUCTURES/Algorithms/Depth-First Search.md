# Depth-First Search

> Graph traversal algorithm that explores as far as possible along each branch before backtracking, using a stack (implicit via recursion or explicit).

## 📖 Definition

DFS systematically visits all vertices by going deep into the graph before exploring siblings. It uses a stack to keep track of the path and backtracks when it reaches a dead end.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(V + E) where V = vertices, E = edges
- **Space Complexity**: O(V) for recursion stack or explicit stack

## 🎯 DFS Applications

1. **Path Finding**: Find if path exists between two nodes
2. **Cycle Detection**: Detect cycles in graphs
3. **Topological Sorting**: Order vertices in DAG
4. **Connected Components**: Find all connected components
5. **Maze Solving**: Navigate through mazes

## 🐍 Python Implementation

```python
from collections import defaultdict

def dfs_recursive(graph, start, visited=None):
    """DFS using recursion"""
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start, end=' ')
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    
    return visited

def dfs_iterative(graph, start):
    """DFS using explicit stack"""
    visited = set()
    stack = [start]
    path = []
    
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            path.append(vertex)
            
            # Add neighbors to stack (reverse order for consistent traversal)
            for neighbor in reversed(graph[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return path

def dfs_path(graph, start, goal, path=None):
    """Find path from start to goal using DFS"""
    if path is None:
        path = []
    
    path = path + [start]
    
    if start == goal:
        return path
    
    for neighbor in graph[start]:
        if neighbor not in path:  # Avoid cycles
            new_path = dfs_path(graph, neighbor, goal, path)
            if new_path:
                return new_path
    
    return None

def dfs_all_paths(graph, start, goal, path=None, all_paths=None):
    """Find all paths from start to goal"""
    if path is None:
        path = []
    if all_paths is None:
        all_paths = []
    
    path = path + [start]
    
    if start == goal:
        all_paths.append(path)
        return all_paths
    
    for neighbor in graph[start]:
        if neighbor not in path:
            dfs_all_paths(graph, neighbor, goal, path, all_paths)
    
    return all_paths

# Example usage
def example_dfs():
    # Create sample graph
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    
    print("DFS Recursive from A:")
    dfs_recursive(graph, 'A')
    print()
    
    print("DFS Iterative from A:")
    path = dfs_iterative(graph, 'A')
    print(' -> '.join(path))
    
    print("Path from A to F:")
    path = dfs_path(graph, 'A', 'F')
    print(' -> '.join(path) if path else "No path found")
    
    print("All paths from A to F:")
    all_paths = dfs_all_paths(graph, 'A', 'F')
    for i, path in enumerate(all_paths, 1):
        print(f"Path {i}: {' -> '.join(path)}")

if __name__ == "__main__":
    example_dfs()
```

## ☕ Java Implementation

```java
import java.util.*;

public class DFS {
    
    // DFS recursive
    public static void dfsRecursive(Map<Integer, List<Integer>> graph, 
                                   int start, Set<Integer> visited) {
        visited.add(start);
        System.out.print(start + " ");
        
        if (graph.containsKey(start)) {
            for (int neighbor : graph.get(start)) {
                if (!visited.contains(neighbor)) {
                    dfsRecursive(graph, neighbor, visited);
                }
            }
        }
    }
    
    // DFS iterative
    public static List<Integer> dfsIterative(Map<Integer, List<Integer>> graph, int start) {
        List<Integer> result = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        Stack<Integer> stack = new Stack<>();
        
        stack.push(start);
        
        while (!stack.isEmpty()) {
            int vertex = stack.pop();
            if (!visited.contains(vertex)) {
                visited.add(vertex);
                result.add(vertex);
                
                if (graph.containsKey(vertex)) {
                    // Add neighbors in reverse order
                    List<Integer> neighbors = graph.get(vertex);
                    for (int i = neighbors.size() - 1; i >= 0; i--) {
                        int neighbor = neighbors.get(i);
                        if (!visited.contains(neighbor)) {
                            stack.push(neighbor);
                        }
                    }
                }
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        Map<Integer, List<Integer>> graph = new HashMap<>();
        graph.put(0, Arrays.asList(1, 2));
        graph.put(1, Arrays.asList(3, 4));
        graph.put(2, Arrays.asList(5));
        graph.put(3, new ArrayList<>());
        graph.put(4, Arrays.asList(5));
        graph.put(5, new ArrayList<>());
        
        System.out.println("DFS Recursive from 0:");
        dfsRecursive(graph, 0, new HashSet<>());
        System.out.println();
        
        System.out.println("DFS Iterative from 0:");
        List<Integer> path = dfsIterative(graph, 0);
        System.out.println(path);
    }
}
```

## 🔗 Related Topics

- [[Breadth-First Search]] - Alternative graph traversal
- [[Binary Trees]] - Tree traversal using DFS
- [[Graphs]] - Data structure for DFS
- [[Backtracking]] - Uses DFS approach

---

*See also: [[Breadth-First Search]], [[Graphs]], [[algorithms_and_ds]]*