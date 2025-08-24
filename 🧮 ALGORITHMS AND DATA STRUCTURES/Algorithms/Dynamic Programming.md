# Dynamic Programming

> Algorithmic paradigm that solves complex problems by breaking them down into simpler subproblems, storing solutions to avoid redundant calculations.

## 📖 Definition

Dynamic Programming (DP) is an optimization technique that solves problems by combining solutions to subproblems. It's applicable when the problem has:

1. **Optimal Substructure**: Optimal solution contains optimal solutions of subproblems
2. **Overlapping Subproblems**: Same subproblems are solved multiple times

## 🎯 Key Concepts

### Memoization (Top-Down)
Store results of expensive function calls and return cached result when same inputs occur again.

### Tabulation (Bottom-Up)  
Build up solutions iteratively, starting from simplest subproblems.

## 🔄 DP Approaches

### 1. Memoization Approach
```python
def fibonacci_memo(n, memo=None):
    """Top-down DP with memoization"""
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]
```

### 2. Tabulation Approach
```python
def fibonacci_tab(n):
    """Bottom-up DP with tabulation"""
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
```

### 3. Space-Optimized
```python
def fibonacci_optimized(n):
    """Space-optimized DP"""
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1
```

## 🐍 Classic DP Problems

### 1. Longest Common Subsequence (LCS)
```python
def lcs_length(text1, text2):
    """Find length of longest common subsequence"""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

def lcs_string(text1, text2):
    """Return actual LCS string"""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Reconstruct LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i-1] == text2[j-1]:
            lcs.append(text1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))
```

### 2. 0/1 Knapsack Problem
```python
def knapsack_01(weights, values, capacity):
    """0/1 Knapsack problem using DP"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Don't include current item
            dp[i][w] = dp[i-1][w]
            
            # Include current item if it fits
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i-1][w-weights[i-1]] + values[i-1])
    
    return dp[n][capacity]

def knapsack_items(weights, values, capacity):
    """Return items included in optimal knapsack"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i-1][w-weights[i-1]] + values[i-1])
    
    # Reconstruct solution
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)  # Item index
            w -= weights[i-1]
    
    return selected[::-1]

def knapsack_space_optimized(weights, values, capacity):
    """Space-optimized O(capacity) solution"""
    dp = [0] * (capacity + 1)
    
    for i in range(len(weights)):
        # Traverse backwards to avoid using updated values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]
```

### 3. Longest Increasing Subsequence (LIS)
```python
def lis_length(arr):
    """Length of longest increasing subsequence - O(n²)"""
    if not arr:
        return 0
    
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

def lis_optimized(arr):
    """LIS using binary search - O(n log n)"""
    if not arr:
        return 0
    
    import bisect
    tails = []
    
    for num in arr:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)

def lis_sequence(arr):
    """Return actual LIS sequence"""
    if not arr:
        return []
    
    n = len(arr)
    dp = [1] * n
    parent = [-1] * n
    
    # Fill DP table and track parents
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j
    
    # Find index of LIS end
    max_length = max(dp)
    max_index = dp.index(max_length)
    
    # Reconstruct LIS
    lis = []
    current = max_index
    while current != -1:
        lis.append(arr[current])
        current = parent[current]
    
    return lis[::-1]
```

### 4. Edit Distance (Levenshtein Distance)
```python
def edit_distance(word1, word2):
    """Minimum edit distance between two strings"""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from word1
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters to get word2
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # Delete
                    dp[i][j-1],    # Insert
                    dp[i-1][j-1]   # Replace
                )
    
    return dp[m][n]

def edit_operations(word1, word2):
    """Return sequence of operations to transform word1 to word2"""
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table (same as above)
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    # Reconstruct operations
    operations = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i-1] == word2[j-1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            operations.append(f"Replace '{word1[i-1]}' with '{word2[j-1]}'")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            operations.append(f"Delete '{word1[i-1]}'")
            i -= 1
        else:
            operations.append(f"Insert '{word2[j-1]}'")
            j -= 1
    
    return operations[::-1]
```

### 5. Coin Change Problem
```python
def coin_change_min(coins, amount):
    """Minimum coins needed to make amount"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

def coin_change_ways(coins, amount):
    """Number of ways to make amount"""
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]

def coin_change_combination(coins, amount):
    """Return one valid combination of coins"""
    dp = [float('inf')] * (amount + 1)
    parent = [-1] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            if dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                parent[i] = coin
    
    if dp[amount] == float('inf'):
        return []
    
    # Reconstruct solution
    result = []
    current = amount
    while current > 0:
        coin = parent[current]
        result.append(coin)
        current -= coin
    
    return result
```

## ☕ Java Implementation Examples

```java
import java.util.*;

public class DynamicProgramming {
    
    // Fibonacci with memoization
    public static int fibonacciMemo(int n, Map<Integer, Integer> memo) {
        if (memo.containsKey(n)) {
            return memo.get(n);
        }
        
        if (n <= 1) {
            return n;
        }
        
        int result = fibonacciMemo(n - 1, memo) + fibonacciMemo(n - 2, memo);
        memo.put(n, result);
        return result;
    }
    
    // Fibonacci with tabulation
    public static int fibonacciTab(int n) {
        if (n <= 1) return n;
        
        int[] dp = new int[n + 1];
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
    
    // 0/1 Knapsack
    public static int knapsack01(int[] weights, int[] values, int capacity) {
        int n = weights.length;
        int[][] dp = new int[n + 1][capacity + 1];
        
        for (int i = 1; i <= n; i++) {
            for (int w = 1; w <= capacity; w++) {
                dp[i][w] = dp[i - 1][w]; // Don't include item
                
                if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(dp[i][w], 
                                       dp[i - 1][w - weights[i - 1]] + values[i - 1]);
                }
            }
        }
        
        return dp[n][capacity];
    }
    
    // Longest Common Subsequence
    public static int lcsLength(String text1, String text2) {
        int m = text1.length(), n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    // Edit Distance
    public static int editDistance(String word1, String word2) {
        int m = word1.length(), n = word2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Initialize base cases
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(Math.min(dp[i - 1][j], dp[i][j - 1]), 
                                           dp[i - 1][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    public static void main(String[] args) {
        // Test Fibonacci
        System.out.println("Fibonacci(10): " + fibonacciTab(10));
        
        // Test Knapsack
        int[] weights = {1, 3, 4, 5};
        int[] values = {1, 4, 5, 7};
        System.out.println("Knapsack: " + knapsack01(weights, values, 7));
        
        // Test LCS
        System.out.println("LCS Length: " + lcsLength("abcde", "ace"));
        
        // Test Edit Distance
        System.out.println("Edit Distance: " + editDistance("horse", "ros"));
    }
}
```

## ⚡ C++ Implementation Examples

```cpp
#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <string>

class DynamicProgramming {
public:
    // Fibonacci with memoization
    static int fibonacciMemo(int n, std::unordered_map<int, int>& memo) {
        if (memo.find(n) != memo.end()) {
            return memo[n];
        }
        
        if (n <= 1) {
            return n;
        }
        
        memo[n] = fibonacciMemo(n - 1, memo) + fibonacciMemo(n - 2, memo);
        return memo[n];
    }
    
    // Fibonacci with tabulation
    static int fibonacciTab(int n) {
        if (n <= 1) return n;
        
        std::vector<int> dp(n + 1);
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
    
    // 0/1 Knapsack
    static int knapsack01(const std::vector<int>& weights, 
                         const std::vector<int>& values, 
                         int capacity) {
        int n = weights.size();
        std::vector<std::vector<int>> dp(n + 1, std::vector<int>(capacity + 1, 0));
        
        for (int i = 1; i <= n; i++) {
            for (int w = 1; w <= capacity; w++) {
                dp[i][w] = dp[i - 1][w]; // Don't include item
                
                if (weights[i - 1] <= w) {
                    dp[i][w] = std::max(dp[i][w], 
                                       dp[i - 1][w - weights[i - 1]] + values[i - 1]);
                }
            }
        }
        
        return dp[n][capacity];
    }
    
    // Longest Common Subsequence
    static int lcsLength(const std::string& text1, const std::string& text2) {
        int m = text1.length(), n = text2.length();
        std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1, 0));
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1[i - 1] == text2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = std::max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    // Edit Distance
    static int editDistance(const std::string& word1, const std::string& word2) {
        int m = word1.length(), n = word2.length();
        std::vector<std::vector<int>> dp(m + 1, std::vector<int>(n + 1));
        
        // Initialize base cases
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i - 1] == word2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + std::min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
                }
            }
        }
        
        return dp[m][n];
    }
};

int main() {
    // Test Fibonacci
    std::cout << "Fibonacci(10): " << DynamicProgramming::fibonacciTab(10) << std::endl;
    
    // Test Knapsack
    std::vector<int> weights = {1, 3, 4, 5};
    std::vector<int> values = {1, 4, 5, 7};
    std::cout << "Knapsack: " << DynamicProgramming::knapsack01(weights, values, 7) << std::endl;
    
    // Test LCS
    std::cout << "LCS Length: " << DynamicProgramming::lcsLength("abcde", "ace") << std::endl;
    
    // Test Edit Distance
    std::cout << "Edit Distance: " << DynamicProgramming::editDistance("horse", "ros") << std::endl;
    
    return 0;
}
```

## 🔍 DP Problem Patterns

### 1. Linear DP
Problems where state depends on previous states in sequence.
- Fibonacci, House Robber, Climbing Stairs

### 2. 2D Grid DP
Problems involving 2D grids or two sequences.
- Longest Common Subsequence, Edit Distance, Unique Paths

### 3. Interval DP
Problems involving intervals or subarrays.
- Matrix Chain Multiplication, Palindromic Substrings

### 4. Tree DP
DP on tree structures.
- Diameter of Tree, Maximum Path Sum

### 5. Digit DP
Problems involving digits of numbers.
- Count numbers with specific properties

## 💡 DP Problem-Solving Strategy

1. **Identify if it's a DP problem**:
   - Optimal substructure
   - Overlapping subproblems

2. **Define the state**:
   - What parameters uniquely identify a subproblem?

3. **Find recurrence relation**:
   - How does current state relate to previous states?

4. **Identify base cases**:
   - What are the simplest subproblems?

5. **Decide implementation approach**:
   - Top-down (memoization) vs Bottom-up (tabulation)

6. **Optimize space if possible**:
   - Can we reduce space complexity?

## 📈 Time and Space Complexity

Most DP problems have:
- **Time Complexity**: O(number of states × time per state)
- **Space Complexity**: O(number of states)

Space can often be optimized by keeping only necessary previous states.

## 🔗 Related Topics

- [[Recursion]] - DP often optimizes recursive solutions
- [[Graphs]] - Some graph problems use DP
- [[Greedy Algorithms]] - Alternative optimization technique

## 📝 Practice Problems

1. **Climbing Stairs**: Count ways to reach top
2. **House Robber**: Maximum money without robbing adjacent houses
3. **Maximum Subarray**: Kadane's algorithm
4. **Unique Paths**: Count paths in grid
5. **Palindromic Substrings**: Count palindromic substrings
6. **Word Break**: Check if string can be segmented
7. **Longest Palindromic Subsequence**: Find LPS length
8. **Maximum Product Subarray**: Find maximum product

---

*See also: [[Recursion]], [[Greedy Algorithms]], [[algorithms_and_ds]]*