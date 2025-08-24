# Breadth-First Search

> Graph traversal algorithm that explores all vertices at the current depth before moving to vertices at the next depth level, using a queue data structure.

## 📖 Definition

BFS systematically visits vertices level by level, exploring all neighbors of a vertex before moving to their neighbors. It guarantees the shortest path in unweighted graphs.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(V + E) where V = vertices, E = edges  
- **Space Complexity**: O(V) for queue and visited set

## 🎯 BFS Applications

1. **Shortest Path**: Find shortest path in unweighted graphs
2. **Level-order Traversal**: Traverse tree level by level
3. **Social Networks**: Find connections within k degrees
4. **Web Crawling**: Crawl web pages systematically  
5. **Puzzle Solving**: Find minimum moves to solve

## 🐍 Python Implementation

```python
from collections import deque

def bfs(graph, start):
    """Basic BFS traversal"""
    visited = set()
    queue = deque([start])
    result = []
    
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

def bfs_shortest_path(graph, start, goal):
    """Find shortest path using BFS"""
    if start == goal:
        return [start]
    
    visited = set()
    queue = deque([(start, [start])])
    visited.add(start)
    
    while queue:
        vertex, path = queue.popleft()
        
        for neighbor in graph[vertex]:
            if neighbor == goal:
                return path + [neighbor]
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None  # No path found

def bfs_level_order(graph, start):
    """BFS with level information"""
    if not graph or start not in graph:
        return []
    
    visited = set()
    queue = deque([(start, 0)])  # (vertex, level)
    levels = {}
    
    visited.add(start)
    
    while queue:
        vertex, level = queue.popleft()
        
        if level not in levels:
            levels[level] = []
        levels[level].append(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))
    
    return levels

def bfs_connected_components(graph):
    """Find all connected components using BFS"""
    visited = set()
    components = []
    
    for vertex in graph:
        if vertex not in visited:
            component = []
            queue = deque([vertex])
            visited.add(vertex)
            
            while queue:
                current = queue.popleft()
                component.append(current)
                
                for neighbor in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
    
    return components

# Tree BFS (Level-order traversal)
def bfs_tree_level_order(root):
    """Level-order traversal of binary tree"""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        result.append(node.val)
        
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return result

def bfs_tree_by_levels(root):
    """Return tree nodes grouped by levels"""
    if not root:
        return []
    
    levels = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level_nodes = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level_nodes.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        levels.append(level_nodes)
    
    return levels

# Example usage
def example_bfs():
    # Create sample graph
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    print("BFS from A:")
    result = bfs(graph, 'A')
    print(' -> '.join(result))
    
    print("Shortest path from A to F:")
    path = bfs_shortest_path(graph, 'A', 'F')
    print(' -> '.join(path) if path else "No path found")
    
    print("BFS with levels from A:")
    levels = bfs_level_order(graph, 'A')
    for level, vertices in levels.items():
        print(f"Level {level}: {vertices}")

if __name__ == "__main__":
    example_bfs()
```

## ☕ Java Implementation

```java
import java.util.*;

public class BFS {
    
    public static List<Integer> bfs(Map<Integer, List<Integer>> graph, int start) {
        List<Integer> result = new ArrayList<>();
        Set<Integer> visited = new HashSet<>();
        Queue<Integer> queue = new LinkedList<>();
        
        queue.offer(start);
        visited.add(start);
        
        while (!queue.isEmpty()) {
            int vertex = queue.poll();
            result.add(vertex);
            
            if (graph.containsKey(vertex)) {
                for (int neighbor : graph.get(vertex)) {
                    if (!visited.contains(neighbor)) {
                        visited.add(neighbor);
                        queue.offer(neighbor);
                    }
                }
            }
        }
        
        return result;
    }
    
    public static List<Integer> shortestPath(Map<Integer, List<Integer>> graph, 
                                           int start, int goal) {
        if (start == goal) {
            return Arrays.asList(start);
        }
        
        Set<Integer> visited = new HashSet<>();
        Queue<List<Integer>> queue = new LinkedList<>();
        
        queue.offer(Arrays.asList(start));
        visited.add(start);
        
        while (!queue.isEmpty()) {
            List<Integer> path = queue.poll();
            int vertex = path.get(path.size() - 1);
            
            if (graph.containsKey(vertex)) {
                for (int neighbor : graph.get(vertex)) {
                    if (neighbor == goal) {
                        List<Integer> newPath = new ArrayList<>(path);
                        newPath.add(neighbor);
                        return newPath;
                    }
                    
                    if (!visited.contains(neighbor)) {
                        visited.add(neighbor);
                        List<Integer> newPath = new ArrayList<>(path);
                        newPath.add(neighbor);
                        queue.offer(newPath);
                    }
                }
            }
        }
        
        return null; // No path found
    }
    
    public static void main(String[] args) {
        Map<Integer, List<Integer>> graph = new HashMap<>();
        graph.put(0, Arrays.asList(1, 2));
        graph.put(1, Arrays.asList(0, 3, 4));
        graph.put(2, Arrays.asList(0, 5));
        graph.put(3, Arrays.asList(1));
        graph.put(4, Arrays.asList(1, 5));
        graph.put(5, Arrays.asList(2, 4));
        
        System.out.println("BFS from 0:");
        List<Integer> result = bfs(graph, 0);
        System.out.println(result);
        
        System.out.println("Shortest path from 0 to 5:");
        List<Integer> path = shortestPath(graph, 0, 5);
        System.out.println(path);
    }
}
```

## 🆚 BFS vs DFS

| Aspect | BFS | DFS |
|--------|-----|-----|
| **Data Structure** | Queue | Stack |
| **Memory Usage** | Higher (stores all neighbors) | Lower (recursion stack) |
| **Shortest Path** | Guarantees shortest path | No guarantee |
| **Complete** | Yes (finds solution if exists) | Yes |
| **Optimal** | Yes (for unweighted graphs) | No |
| **Space Complexity** | O(b^d) | O(bd) |

*b = branching factor, d = depth*

## 🎯 When to Use BFS

✅ **Use BFS when:**
- Finding shortest path in unweighted graph
- Level-order tree traversal needed
- Finding all nodes within k distance
- Minimum steps/moves problems

❌ **Don't use BFS when:**
- Memory is limited (DFS uses less memory)
- You only need to find any solution (not optimal)
- Working with very wide graphs

## 🔗 Related Topics

- [[Depth-First Search]] - Alternative graph traversal
- [[Dijkstra Algorithm]] - Shortest path with weights
- [[Binary Trees]] - Level-order traversal
- [[Graphs]] - Data structure for BFS

---

*See also: [[Depth-First Search]], [[Graphs]], [[Dijkstra Algorithm]], [[algorithms_and_ds]]*