# Dynamic Programming Basics

> Problem-solving technique that breaks down complex problems into simpler subproblems, storing results to avoid redundant calculations.

## 📖 Definition

Dynamic Programming (DP) is an algorithmic paradigm that solves complex problems by breaking them down into simpler subproblems. It stores the results of subproblems to avoid computing the same results again, following the principle of optimality.

## 🔑 Key Principles

### 1. Overlapping Subproblems
The problem can be broken down into subproblems which are reused several times.

### 2. Optimal Substructure
An optimal solution can be constructed from optimal solutions of its subproblems.

## 🎯 DP Approaches

### 1. Memoization (Top-Down)
- Start with the original problem
- Break it down recursively
- Store results in a memo table

### 2. Tabulation (Bottom-Up)
- Start with smallest subproblems
- Build up to the original problem
- Fill up a table systematically

## ⚡ Time & Space Complexity

- **Time Complexity**: Usually reduces exponential to polynomial
- **Space Complexity**: O(number of unique subproblems)
- **Trade-off**: Space for time optimization

## 🐍 Python Implementation Examples

```python
# Example 1: Fibonacci (Classic DP)
def fibonacci_memo(n, memo={}):
    """Memoization approach"""
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]

def fibonacci_tab(n):
    """Tabulation approach"""
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

def fibonacci_optimized(n):
    """Space-optimized tabulation"""
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1

# Example 2: Climbing Stairs
def climb_stairs(n):
    """Number of ways to climb n stairs (1 or 2 steps at a time)"""
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

# Example 3: House Robber
def rob_houses(houses):
    """Maximum money that can be robbed without robbing adjacent houses"""
    if not houses:
        return 0
    if len(houses) == 1:
        return houses[0]
    
    dp = [0] * len(houses)
    dp[0] = houses[0]
    dp[1] = max(houses[0], houses[1])
    
    for i in range(2, len(houses)):
        dp[i] = max(dp[i-1], dp[i-2] + houses[i])
    
    return dp[-1]

# Example usage
if __name__ == "__main__":
    print("Fibonacci(10):", fibonacci_tab(10))
    print("Climb stairs(5):", climb_stairs(5))
    print("Rob houses [2,7,9,3,1]:", rob_houses([2, 7, 9, 3, 1]))
```

## 🔍 DP Problem Patterns

### 1. Linear DP
Problems where state depends on previous states in sequence.
- **Examples**: Fibonacci, House Robber, Climbing Stairs
- **Pattern**: `dp[i] = f(dp[i-1], dp[i-2], ...)`

### 2. 2D Grid DP
Problems involving 2D grids or two sequences.
- **Examples**: Longest Common Subsequence, Edit Distance, Unique Paths
- **Pattern**: `dp[i][j] = f(dp[i-1][j], dp[i][j-1], ...)`

### 3. Interval DP
Problems involving intervals or subarrays.
- **Examples**: Matrix Chain Multiplication, Palindromic Substrings
- **Pattern**: `dp[i][j] = f(dp[i][k], dp[k+1][j]) for k in range(i, j)`

### 4. Tree DP
DP on tree structures.
- **Examples**: Diameter of Tree, Maximum Path Sum
- **Pattern**: Combine results from children nodes

### 5. State Machine DP
Problems with discrete states.
- **Examples**: Best Time to Buy/Sell Stock
- **Pattern**: `dp[i][state] = f(dp[i-1][other_states])`

## 🎯 How to Identify DP Problems

1. **Optimal Substructure**: Can problem be broken into subproblems?
2. **Overlapping Subproblems**: Are subproblems computed multiple times?
3. **Choices**: At each step, do we make a choice that affects future?
4. **Optimization**: Are we finding minimum/maximum/count?

## 💡 DP Design Process

1. **Define State**: What information needed for subproblem?
2. **State Transition**: How to compute state from previous states?
3. **Base Cases**: What are the simplest cases?
4. **Order**: In what order to compute states?
5. **Answer**: Where is the final answer located?

## 🔧 Common DP Optimizations

1. **Space Optimization**: Use rolling arrays when only previous states needed
2. **Memoization**: Cache results in recursive solutions
3. **State Compression**: Reduce dimensions when possible
4. **Lazy Evaluation**: Compute only needed states

## 🎯 Applications

1. **Algorithm Design**: Optimal solutions to complex problems
2. **Competitive Programming**: Common problem-solving technique
3. **Economics**: Resource allocation and optimization
4. **Bioinformatics**: Sequence alignment algorithms
5. **Computer Graphics**: Image processing algorithms

## 🔗 Related Topics

- [[Fibonacci Sequence]] - Classic DP example
- [[Longest Common Subsequence]] - String DP problem
- [[Knapsack Problem]] - Optimization DP problem
- [[Edit Distance]] - String transformation problem

---

*See also: [[Dynamic Programming]], [[Fibonacci Sequence]], [[algorithms_and_ds]]*