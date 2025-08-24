# Edit Distance

> Minimum number of single-character edits (insertions, deletions, or substitutions) needed to transform one string into another, also known as Levenshtein distance.

## 📖 Definition

Edit distance measures the similarity between two strings by counting the minimum number of operations required to transform one string into another. The allowed operations are insertion, deletion, and substitution of a single character.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(m × n) where m, n are string lengths
- **Space Complexity**: O(m × n) for DP table, can be optimized to O(min(m,n))
- **Dynamic Programming**: Classic 2D DP problem

## 🔑 Operations

1. **Insert**: Add a character
2. **Delete**: Remove a character  
3. **Substitute**: Replace a character with another

## 🐍 Python Implementation

```python
def edit_distance(str1, str2):
    """Calculate minimum edit distance between two strings"""
    m, n = len(str1), len(str2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    # Converting empty string to str2[0:j] requires j insertions
    for j in range(n + 1):
        dp[0][j] = j
    
    # Converting str1[0:i] to empty string requires i deletions
    for i in range(m + 1):
        dp[i][0] = i
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i-1][j-1]
            else:
                # Take minimum of three operations
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # Delete from str1
                    dp[i][j-1],    # Insert into str1
                    dp[i-1][j-1]   # Substitute in str1
                )
    
    return dp[m][n]

def edit_distance_with_operations(str1, str2):
    """Return edit distance and the actual operations"""
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(m + 1):
        dp[i][0] = i
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    # Backtrack to find operations
    operations = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and str1[i-1] == str2[j-1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + 1:
            operations.append(f"Substitute '{str1[i-1]}' with '{str2[j-1]}' at position {i-1}")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            operations.append(f"Delete '{str1[i-1]}' at position {i-1}")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + 1:
            operations.append(f"Insert '{str2[j-1]}' at position {i}")
            j -= 1
    
    operations.reverse()
    return dp[m][n], operations

def edit_distance_space_optimized(str1, str2):
    """Space optimized version - O(min(m,n)) space"""
    m, n = len(str1), len(str2)
    
    # Make str1 the shorter string for space optimization
    if m > n:
        str1, str2 = str2, str1
        m, n = n, m
    
    # Use only two rows
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        curr[0] = j
        
        for i in range(1, m + 1):
            if str1[i-1] == str2[j-1]:
                curr[i] = prev[i-1]
            else:
                curr[i] = 1 + min(prev[i], curr[i-1], prev[i-1])
        
        prev, curr = curr, prev
    
    return prev[m]

# Example usage
if __name__ == "__main__":
    str1 = "kitten"
    str2 = "sitting"
    
    distance = edit_distance(str1, str2)
    print(f"Edit distance between '{str1}' and '{str2}': {distance}")
    
    distance_ops, operations = edit_distance_with_operations(str1, str2)
    print(f"Operations needed:")
    for op in operations:
        print(f"  {op}")
    
    # Space optimized
    distance_opt = edit_distance_space_optimized(str1, str2)
    print(f"Space optimized result: {distance_opt}")
```

## ☕ Java Implementation

```java
public class EditDistance {
    
    public static int editDistance(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
        // Create DP table
        int[][] dp = new int[m + 1][n + 1];
        
        // Initialize base cases
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;
        }
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        
        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(Math.min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    public static int editDistanceSpaceOptimized(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
        // Use only two arrays
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];
        
        // Initialize first row
        for (int j = 0; j <= n; j++) {
            prev[j] = j;
        }
        
        for (int i = 1; i <= m; i++) {
            curr[0] = i;
            
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    curr[j] = prev[j - 1];
                } else {
                    curr[j] = 1 + Math.min(Math.min(prev[j], curr[j - 1]), prev[j - 1]);
                }
            }
            
            // Swap arrays
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }
        
        return prev[n];
    }
    
    public static void printDPTable(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Fill DP table (same logic as above)
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(Math.min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]);
                }
            }
        }
        
        // Print table
        System.out.println("DP Table:");
        System.out.print("    ");
        for (int j = 0; j <= n; j++) {
            if (j == 0) System.out.print("ε ");
            else System.out.print(str2.charAt(j-1) + " ");
        }
        System.out.println();
        
        for (int i = 0; i <= m; i++) {
            if (i == 0) System.out.print("ε ");
            else System.out.print(str1.charAt(i-1) + " ");
            
            for (int j = 0; j <= n; j++) {
                System.out.print(dp[i][j] + " ");
            }
            System.out.println();
        }
    }
    
    public static void main(String[] args) {
        String str1 = "kitten";
        String str2 = "sitting";
        
        int distance = editDistance(str1, str2);
        System.out.println("Edit distance between '" + str1 + "' and '" + str2 + "': " + distance);
        
        printDPTable(str1, str2);
        
        int distanceOpt = editDistanceSpaceOptimized(str1, str2);
        System.out.println("Space optimized result: " + distanceOpt);
    }
}
```

## 🎯 Applications

1. **Spell Checkers**: Find closest correct spellings
2. **DNA Analysis**: Compare genetic sequences
3. **Plagiarism Detection**: Measure text similarity
4. **Version Control**: Diff algorithms in Git
5. **Auto-correction**: Mobile keyboards and text input
6. **Database Record Matching**: Find similar records

## 🆚 Edit Distance Variants

| Variant | Operations | Use Case |
|---------|------------|----------|
| **Levenshtein** | Insert, Delete, Substitute | General string similarity |
| **Hamming** | Substitute only | Same-length strings |
| **Longest Common Subsequence** | Insert, Delete only | Sequence alignment |
| **Damerau-Levenshtein** | + Transposition | OCR error correction |

## 💡 Key Insights

1. **Recurrence Relation**: Breaks problem into smaller subproblems
2. **Optimal Substructure**: Optimal alignment contains optimal subalignments
3. **Bottom-up Construction**: Build solution from smaller problems
4. **Space-Time Trade-off**: Can optimize space at cost of losing operation trace

## 🔧 Optimizations

1. **Space Optimization**: Use O(min(m,n)) space instead of O(mn)
2. **Early Termination**: Stop if distance exceeds threshold
3. **Diagonal Optimization**: Process only relevant diagonal band
4. **Parallel Processing**: Compute diagonals in parallel

## 🔗 Related Topics

- [[Dynamic Programming]] - General DP technique
- [[Longest Common Subsequence]] - Related string DP problem
- [[String Algorithms]] - String processing techniques
- [[Hamming Distance]] - Simpler distance for equal-length strings

---

*See also: [[Dynamic Programming]], [[Longest Common Subsequence]], [[algorithms_and_ds]]*