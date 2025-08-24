# Topological Sort

> Linear ordering of vertices in a directed acyclic graph (DAG) such that for every directed edge (u,v), vertex u comes before vertex v in the ordering.

## 📖 Definition

Topological sorting is a linear ordering of vertices in a directed acyclic graph (DAG) such that for every directed edge (u, v), vertex u appears before vertex v in the ordering. It's only possible for DAGs.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(V + E) where V = vertices, E = edges
- **Space Complexity**: O(V) for auxiliary data structures
- **Prerequisite**: Graph must be acyclic (DAG)

## 🔑 Key Applications

1. **Task Scheduling**: Order tasks based on dependencies
2. **Course Prerequisites**: Academic course planning
3. **Build Systems**: Compile order for dependencies
4. **Project Management**: Task dependency resolution

## 🐍 Python Implementation

```python
from collections import defaultdict, deque

def topological_sort_dfs(graph):
    """Topological sort using DFS"""
    visited = set()
    stack = []
    
    def dfs(vertex):
        visited.add(vertex)
        
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                dfs(neighbor)
        
        stack.append(vertex)
    
    # Get all vertices
    vertices = set(graph.keys())
    for vertex in graph:
        vertices.update(graph[vertex])
    
    # DFS from all unvisited vertices
    for vertex in vertices:
        if vertex not in visited:
            dfs(vertex)
    
    return stack[::-1]  # Reverse to get topological order

def topological_sort_kahns(graph):
    """Kahn's algorithm using BFS approach"""
    # Calculate in-degrees
    in_degree = defaultdict(int)
    vertices = set(graph.keys())
    
    for vertex in graph:
        vertices.update(graph[vertex])
        for neighbor in graph[vertex]:
            in_degree[neighbor] += 1
    
    # Initialize in-degree for all vertices
    for vertex in vertices:
        if vertex not in in_degree:
            in_degree[vertex] = 0
    
    # Find vertices with 0 in-degree
    queue = deque([v for v in vertices if in_degree[v] == 0])
    result = []
    
    while queue:
        vertex = queue.popleft()
        result.append(vertex)
        
        # Reduce in-degree of neighbors
        for neighbor in graph.get(vertex, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if all vertices are included (cycle detection)
    if len(result) != len(vertices):
        return None  # Graph has cycle
    
    return result

def detect_cycle_dfs(graph):
    """Detect cycle in directed graph using DFS"""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(lambda: WHITE)
    
    def dfs(vertex):
        if color[vertex] == GRAY:
            return True  # Back edge found (cycle)
        
        if color[vertex] == BLACK:
            return False  # Already processed
        
        color[vertex] = GRAY
        
        for neighbor in graph.get(vertex, []):
            if dfs(neighbor):
                return True
        
        color[vertex] = BLACK
        return False
    
    # Check all vertices
    vertices = set(graph.keys())
    for vertex in graph:
        vertices.update(graph[vertex])
    
    for vertex in vertices:
        if color[vertex] == WHITE:
            if dfs(vertex):
                return True
    
    return False

def all_topological_sorts(graph):
    """Find all possible topological sorts"""
    vertices = set(graph.keys())
    for vertex in graph:
        vertices.update(graph[vertex])
    
    in_degree = defaultdict(int)
    for vertex in graph:
        for neighbor in graph[vertex]:
            in_degree[neighbor] += 1
    
    def backtrack(result, remaining):
        if not remaining:
            all_sorts.append(result[:])
            return
        
        # Try all vertices with in-degree 0
        for vertex in remaining:
            if in_degree[vertex] == 0:
                # Choose vertex
                result.append(vertex)
                remaining.remove(vertex)
                
                # Reduce in-degree of neighbors
                for neighbor in graph.get(vertex, []):
                    in_degree[neighbor] -= 1
                
                backtrack(result, remaining)
                
                # Backtrack
                result.pop()
                remaining.add(vertex)
                for neighbor in graph.get(vertex, []):
                    in_degree[neighbor] += 1
    
    all_sorts = []
    backtrack([], vertices)
    return all_sorts

class CourseScheduler:
    """Practical example: Course scheduling with prerequisites"""
    
    def __init__(self):
        self.courses = defaultdict(list)
        self.prerequisites = defaultdict(int)
    
    def add_course(self, course, prereq=None):
        if prereq:
            self.courses[prereq].append(course)
            self.prerequisites[course] += 1
        else:
            # Ensure course exists in graph
            if course not in self.courses:
                self.courses[course] = []
    
    def get_course_order(self):
        """Get valid course taking order"""
        # Kahn's algorithm
        queue = deque()
        in_degree = self.prerequisites.copy()
        
        # Find courses with no prerequisites
        all_courses = set(self.courses.keys())
        for course in self.courses:
            all_courses.update(self.courses[course])
        
        for course in all_courses:
            if in_degree[course] == 0:
                queue.append(course)
        
        order = []
        while queue:
            course = queue.popleft()
            order.append(course)
            
            for next_course in self.courses[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)
        
        return order if len(order) == len(all_courses) else None

# Example usage
if __name__ == "__main__":
    # Basic topological sort
    graph = {
        'A': ['C'],
        'B': ['C', 'D'],
        'C': ['E'],
        'D': ['F'],
        'E': ['F'],
        'F': []
    }
    
    print("Graph:", dict(graph))
    
    # DFS-based topological sort
    topo_dfs = topological_sort_dfs(graph)
    print("Topological sort (DFS):", topo_dfs)
    
    # Kahn's algorithm
    topo_kahns = topological_sort_kahns(graph)
    print("Topological sort (Kahn's):", topo_kahns)
    
    # Cycle detection
    has_cycle = detect_cycle_dfs(graph)
    print("Has cycle:", has_cycle)
    
    # Course scheduling example
    scheduler = CourseScheduler()
    scheduler.add_course("Math101")
    scheduler.add_course("Physics101", "Math101")
    scheduler.add_course("Chemistry101", "Math101")
    scheduler.add_course("Physics201", "Physics101")
    scheduler.add_course("Chemistry201", "Chemistry101")
    
    course_order = scheduler.get_course_order()
    print("Course order:", course_order)
    
    # All topological sorts (for small graphs)
    small_graph = {'A': ['B'], 'B': ['C'], 'C': []}
    all_sorts = all_topological_sorts(small_graph)
    print("All topological sorts:", all_sorts)
```

## 🎯 Real-World Applications

### 1. Project Management
- **Task Dependencies**: Order tasks based on prerequisites
- **Critical Path**: Find longest path in project network
- **Resource Allocation**: Schedule resources efficiently

### 2. Software Development
- **Build Systems**: Compile files in dependency order
- **Package Management**: Install dependencies first
- **Module Loading**: Load modules in correct order

### 3. Academic Planning
- **Course Scheduling**: Take prerequisites before advanced courses
- **Curriculum Design**: Structure learning progression
- **Degree Planning**: Optimize course sequence

### 4. Manufacturing
- **Assembly Lines**: Order production steps
- **Supply Chain**: Organize supplier dependencies
- **Quality Control**: Sequence testing procedures

## 🔍 Algorithm Variants

### DFS-Based Approach
- Uses depth-first search with finishing times
- Natural recursive implementation
- Post-order traversal gives reverse topological order

### Kahn's Algorithm (BFS-Based)
- Removes vertices with no incoming edges iteratively
- Uses queue for level-by-level processing
- Naturally detects cycles

## 💡 Cycle Detection

If topological sort cannot include all vertices, the graph contains a cycle:
- **DFS**: Gray vertices indicate back edges (cycles)
- **Kahn's**: Remaining vertices after algorithm indicate cycles

## 🔗 Related Topics

- [[Depth-First Search]] - DFS-based implementation
- [[Breadth-First Search]] - Kahn's algorithm approach
- [[Graphs]] - Underlying data structure
- [[Cycle Detection]] - Related graph analysis

---

*See also: [[Depth-First Search]], [[Graphs]], [[algorithms_and_ds]]*