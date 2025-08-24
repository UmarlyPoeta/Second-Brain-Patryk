# Knapsack Problem

> Classic optimization problem in dynamic programming where items with given weights and values must be selected to maximize value while staying within weight capacity.

## 📖 Definition

The knapsack problem is a problem in combinatorial optimization: given a set of items, each with a weight and value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given capacity and the total value is as large as possible.

## 🎯 Problem Variants

### 1. 0/1 Knapsack (Bounded)
- Each item can be taken at most once
- Most common variant

### 2. Unbounded Knapsack
- Unlimited quantity of each item
- Can take same item multiple times

### 3. Bounded Knapsack
- Limited quantity for each item
- Generalization of 0/1 knapsack

## ⚡ Time & Space Complexity

- **0/1 Knapsack**: O(n × W) time, O(n × W) space
- **Space Optimized**: O(W) space using rolling array
- **Unbounded**: O(n × W) time, O(W) space

Where n = number of items, W = knapsack capacity

## 🐍 Python Implementation

```python
def knapsack_01(weights, values, capacity):
    """0/1 Knapsack using 2D DP"""
    n = len(weights)
    
    # Create DP table
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i-1][w]
            
            # Take item i-1 if it fits
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
    
    return dp[n][capacity]

def knapsack_01_optimized(weights, values, capacity):
    """Space optimized 0/1 Knapsack - O(W) space"""
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Process from right to left to avoid using updated values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]

def knapsack_01_with_items(weights, values, capacity):
    """0/1 Knapsack returning selected items"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
    
    # Backtrack to find selected items
    selected_items = []
    w = capacity
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i-1)  # Item index
            w -= weights[i-1]
    
    selected_items.reverse()
    return dp[n][capacity], selected_items

def knapsack_unbounded(weights, values, capacity):
    """Unbounded Knapsack - unlimited items"""
    dp = [0] * (capacity + 1)
    
    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]

def knapsack_bounded(weights, values, quantities, capacity):
    """Bounded Knapsack with limited quantities"""
    # Convert to 0/1 knapsack by expanding items
    expanded_weights = []
    expanded_values = []
    
    for i in range(len(weights)):
        for _ in range(quantities[i]):
            expanded_weights.append(weights[i])
            expanded_values.append(values[i])
    
    return knapsack_01(expanded_weights, expanded_values, capacity)

# Example usage
if __name__ == "__main__":
    # Example: weights, values, capacity
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    
    print("0/1 Knapsack:")
    print(f"Weights: {weights}")
    print(f"Values: {values}")
    print(f"Capacity: {capacity}")
    
    max_value = knapsack_01(weights, values, capacity)
    print(f"Maximum value: {max_value}")
    
    max_value_opt = knapsack_01_optimized(weights, values, capacity)
    print(f"Optimized result: {max_value_opt}")
    
    max_value_items, selected = knapsack_01_with_items(weights, values, capacity)
    print(f"Selected items (indices): {selected}")
    print(f"Selected weights: {[weights[i] for i in selected]}")
    print(f"Selected values: {[values[i] for i in selected]}")
    
    # Unbounded knapsack
    unbounded_value = knapsack_unbounded(weights, values, capacity)
    print(f"Unbounded knapsack value: {unbounded_value}")
```

## 🎯 Real-World Applications

1. **Resource Allocation**: Budget optimization, project selection
2. **Cargo Loading**: Maximizing value in limited space
3. **Investment Portfolio**: Selecting assets within budget constraints
4. **Memory Management**: Optimal cache usage
5. **Cutting Stock Problem**: Minimize waste in manufacturing

## 🔍 Problem Variations

### Fractional Knapsack
- Can take fractions of items
- Greedy algorithm works optimally
- O(n log n) time complexity

### Multiple Knapsacks
- Multiple containers with different capacities
- More complex optimization problem

### Knapsack with Dependencies
- Items have prerequisite relationships
- Additional constraints to consider

## 💡 Key Insights

1. **Optimal Substructure**: Optimal solution contains optimal sub-solutions
2. **Overlapping Subproblems**: Same subproblems appear multiple times
3. **Choice**: For each item, choose to include or exclude
4. **State Definition**: dp[i][w] = max value using first i items with capacity w

## 🔧 Advanced Techniques

1. **Branch and Bound**: For exact solutions with pruning
2. **Approximation Algorithms**: FPTAS for near-optimal solutions
3. **Genetic Algorithms**: Heuristic approaches for large instances
4. **Integer Linear Programming**: Mathematical optimization formulation

## 🔗 Related Topics

- [[Dynamic Programming]] - Core technique used
- [[Greedy Algorithms]] - For fractional knapsack variant
- [[Backtracking]] - Alternative exact solution method
- [[Optimization Problems]] - Related optimization concepts

---

*See also: [[Dynamic Programming]], [[Greedy Algorithms]], [[algorithms_and_ds]]*