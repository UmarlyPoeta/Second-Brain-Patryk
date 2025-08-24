# Fibonacci Sequence

> Classic dynamic programming example that demonstrates the power of memoization to transform an exponential algorithm into a linear one.

## 📖 Definition

The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones: F(n) = F(n-1) + F(n-2), with F(0) = 0 and F(1) = 1.

## ⚡ Complexity Analysis

| Approach | Time | Space | Description |
|----------|------|-------|-------------|
| **Naive Recursive** | O(2ⁿ) | O(n) | Exponential - very slow |
| **Memoization** | O(n) | O(n) | Top-down DP |
| **Tabulation** | O(n) | O(n) | Bottom-up DP |
| **Space Optimized** | O(n) | O(1) | Only store last 2 values |
| **Matrix Exponentiation** | O(log n) | O(1) | Advanced technique |

## 🐍 Python Implementation

```python
# 1. Naive Recursive (Exponential Time)
def fibonacci_naive(n):
    """Naive recursive - O(2^n) time"""
    if n <= 1:
        return n
    return fibonacci_naive(n-1) + fibonacci_naive(n-2)

# 2. Memoization (Top-Down DP)
def fibonacci_memo(n, memo={}):
    """Memoization approach - O(n) time"""
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]

# 3. Tabulation (Bottom-Up DP)
def fibonacci_tab(n):
    """Tabulation approach - O(n) time, O(n) space"""
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

# 4. Space Optimized
def fibonacci_optimized(n):
    """Space optimized - O(n) time, O(1) space"""
    if n <= 1:
        return n
    
    prev2, prev1 = 0, 1
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2, prev1 = prev1, current
    
    return prev1

# 5. Matrix Exponentiation (Advanced)
def fibonacci_matrix(n):
    """Matrix exponentiation - O(log n) time"""
    if n <= 1:
        return n
    
    def matrix_multiply(A, B):
        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
    
    def matrix_power(matrix, n):
        if n == 1:
            return matrix
        if n % 2 == 0:
            half = matrix_power(matrix, n // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, matrix_power(matrix, n - 1))
    
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    return result_matrix[0][1]

# Generator for Fibonacci sequence
def fibonacci_generator():
    """Generate Fibonacci numbers indefinitely"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Example usage
if __name__ == "__main__":
    n = 10
    
    print(f"Fibonacci({n}):")
    print(f"Tabulation: {fibonacci_tab(n)}")
    print(f"Memoization: {fibonacci_memo(n)}")
    print(f"Optimized: {fibonacci_optimized(n)}")
    print(f"Matrix: {fibonacci_matrix(n)}")
    
    # First 10 Fibonacci numbers
    fib_gen = fibonacci_generator()
    first_10 = [next(fib_gen) for _ in range(10)]
    print(f"First 10: {first_10}")
```

## ☕ Java Implementation

```java
import java.util.HashMap;
import java.util.Map;

public class FibonacciSequence {
    
    // Memoization approach
    private static Map<Integer, Long> memo = new HashMap<>();
    
    public static long fibonacciMemo(int n) {
        if (memo.containsKey(n)) {
            return memo.get(n);
        }
        
        if (n <= 1) {
            return n;
        }
        
        long result = fibonacciMemo(n - 1) + fibonacciMemo(n - 2);
        memo.put(n, result);
        return result;
    }
    
    // Tabulation approach
    public static long fibonacciTab(int n) {
        if (n <= 1) return n;
        
        long[] dp = new long[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
    
    // Space optimized
    public static long fibonacciOptimized(int n) {
        if (n <= 1) return n;
        
        long prev2 = 0, prev1 = 1;
        
        for (int i = 2; i <= n; i++) {
            long current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
    
    // Matrix exponentiation
    public static long fibonacciMatrix(int n) {
        if (n <= 1) return n;
        
        long[][] base = {{1, 1}, {1, 0}};
        long[][] result = matrixPower(base, n);
        return result[0][1];
    }
    
    private static long[][] matrixMultiply(long[][] A, long[][] B) {
        return new long[][]{{A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]},
                           {A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]}};
    }
    
    private static long[][] matrixPower(long[][] matrix, int n) {
        if (n == 1) return matrix;
        
        if (n % 2 == 0) {
            long[][] half = matrixPower(matrix, n / 2);
            return matrixMultiply(half, half);
        } else {
            return matrixMultiply(matrix, matrixPower(matrix, n - 1));
        }
    }
    
    public static void main(String[] args) {
        int n = 10;
        
        System.out.println("Fibonacci(" + n + "):");
        System.out.println("Memoization: " + fibonacciMemo(n));
        System.out.println("Tabulation: " + fibonacciTab(n));
        System.out.println("Optimized: " + fibonacciOptimized(n));
        System.out.println("Matrix: " + fibonacciMatrix(n));
    }
}
```

## 🎯 Fibonacci Applications

1. **Nature Patterns**: Flower petals, pinecones, shells
2. **Art and Architecture**: Golden ratio proportions
3. **Computer Science**: Algorithm analysis, recursion examples
4. **Financial Markets**: Technical analysis patterns
5. **Mathematical Modeling**: Population growth models

## 💡 Key Insights

1. **Exponential to Linear**: DP transforms O(2ⁿ) to O(n)
2. **Space Trade-off**: Can optimize space from O(n) to O(1)
3. **Pattern Recognition**: Foundation for many DP problems
4. **Mathematical Properties**: Golden ratio relationship

## 🔧 Variations and Extensions

1. **Tribonacci**: Sum of three previous numbers
2. **k-Fibonacci**: Sum of k previous numbers
3. **Matrix Form**: Using matrix multiplication for fast computation
4. **Modular Fibonacci**: Computing Fibonacci mod m

## 🔗 Related Topics

- [[Dynamic Programming]] - General DP concepts
- [[Dynamic Programming Basics]] - DP fundamentals
- [[Time Complexity]] - Complexity analysis
- [[Recursion]] - Recursive problem-solving

---

*See also: [[Dynamic Programming]], [[Dynamic Programming Basics]], [[algorithms_and_ds]]*