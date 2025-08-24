# Longest Common Subsequence

> Dynamic programming problem to find the longest subsequence common to two sequences, widely used in bioinformatics, version control, and text comparison.

## 📖 Definition

The Longest Common Subsequence (LCS) problem is to find the longest subsequence common to two sequences. A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

## ⚡ Time & Space Complexity

- **Time Complexity**: O(m × n) where m, n are sequence lengths
- **Space Complexity**: O(m × n) for DP table, can be optimized to O(min(m,n))
- **Dynamic Programming**: Classic 2D DP problem

## 🔑 Key Insight

If characters match, extend LCS by 1. If they don't match, take maximum of excluding either character.

## 🐍 Python Implementation

```python
def lcs_length(str1, str2):
    """Find length of longest common subsequence"""
    m, n = len(str1), len(str2)
    
    # Create DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]

def lcs_string(str1, str2):
    """Find the actual LCS string"""
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Backtrack to find LCS
    lcs = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            lcs.append(str1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))

def lcs_space_optimized(str1, str2):
    """Space optimized LCS - O(min(m,n)) space"""
    m, n = len(str1), len(str2)
    
    # Make str1 the shorter string
    if m > n:
        str1, str2 = str2, str1
        m, n = n, m
    
    # Use only two rows
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if str1[i-1] == str2[j-1]:
                curr[i] = prev[i-1] + 1
            else:
                curr[i] = max(prev[i], curr[i-1])
        
        prev, curr = curr, [0] * (m + 1)
    
    return prev[m]

def lcs_multiple(sequences):
    """LCS of multiple sequences"""
    if len(sequences) == 0:
        return ""
    if len(sequences) == 1:
        return sequences[0]
    
    result = sequences[0]
    for i in range(1, len(sequences)):
        result = lcs_string(result, sequences[i])
    
    return result

def lcs_all_subsequences(str1, str2):
    """Find all longest common subsequences"""
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    # Find all LCS using backtracking
    def backtrack(i, j, current_lcs):
        if i == 0 or j == 0:
            all_lcs.add(current_lcs[::-1])
            return
        
        if str1[i-1] == str2[j-1]:
            backtrack(i-1, j-1, current_lcs + str1[i-1])
        else:
            if dp[i-1][j] == dp[i][j]:
                backtrack(i-1, j, current_lcs)
            if dp[i][j-1] == dp[i][j]:
                backtrack(i, j-1, current_lcs)
    
    all_lcs = set()
    backtrack(m, n, "")
    return list(all_lcs)

# Example usage
if __name__ == "__main__":
    str1 = "ABCDGH"
    str2 = "AEDFHR"
    
    length = lcs_length(str1, str2)
    print(f"LCS length of '{str1}' and '{str2}': {length}")
    
    lcs = lcs_string(str1, str2)
    print(f"LCS string: '{lcs}'")
    
    # Space optimized
    length_opt = lcs_space_optimized(str1, str2)
    print(f"Space optimized length: {length_opt}")
    
    # Multiple sequences
    sequences = ["ABCD", "ACBD", "ABDC"]
    multi_lcs = lcs_multiple(sequences)
    print(f"LCS of multiple sequences: '{multi_lcs}'")
    
    # All LCS
    all_lcs = lcs_all_subsequences("ABC", "AC")
    print(f"All LCS of 'ABC' and 'AC': {all_lcs}")
```

## ☕ Java Implementation

```java
import java.util.*;

public class LongestCommonSubsequence {
    
    public static int lcsLength(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    public static String lcsString(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        // Backtrack to construct LCS
        StringBuilder lcs = new StringBuilder();
        int i = m, j = n;
        
        while (i > 0 && j > 0) {
            if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                lcs.append(str1.charAt(i - 1));
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        
        return lcs.reverse().toString();
    }
    
    public static int lcsSpaceOptimized(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
        // Use only two arrays
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    curr[j] = prev[j - 1] + 1;
                } else {
                    curr[j] = Math.max(prev[j], curr[j - 1]);
                }
            }
            
            // Swap arrays
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }
        
        return prev[n];
    }
    
    public static void printLCSTable(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        // Print table
        System.out.println("LCS DP Table:");
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
        String str1 = "ABCDGH";
        String str2 = "AEDFHR";
        
        int length = lcsLength(str1, str2);
        System.out.println("LCS length: " + length);
        
        String lcs = lcsString(str1, str2);
        System.out.println("LCS string: " + lcs);
        
        printLCSTable(str1, str2);
    }
}
```

## 🎯 Applications

1. **Bioinformatics**: DNA/protein sequence alignment
2. **Version Control**: Diff algorithms (Git, SVN)
3. **Plagiarism Detection**: Document similarity analysis
4. **Data Compression**: Finding repeated patterns
5. **File Synchronization**: Rsync and similar tools

## 🆚 LCS vs Related Problems

| Problem | Focus | Applications |
|---------|-------|--------------|
| **LCS** | Common subsequence | Sequence alignment, diff |
| **[[Edit Distance]]** | Transformation cost | Spell checking, similarity |
| **Longest Increasing Subsequence** | Monotonic subsequence | Optimization problems |
| **String Matching** | Exact pattern | Text search, parsing |

## 💡 Key Insights

1. **Subsequence vs Substring**: LCS doesn't require contiguous characters
2. **Optimal Substructure**: LCS exhibits optimal substructure property
3. **Recurrence Relation**: Build solution from smaller subproblems
4. **Multiple Solutions**: There may be multiple LCS of same length

## 🔧 Variations

1. **Longest Common Substring**: Requires contiguous characters
2. **k-LCS**: LCS of k sequences
3. **Weighted LCS**: Characters have different weights
4. **Constrained LCS**: Additional constraints on subsequence

## 🔗 Related Topics

- [[Dynamic Programming]] - Core technique
- [[Edit Distance]] - Related string DP problem
- [[String Algorithms]] - String processing techniques
- [[Sequence Alignment]] - Bioinformatics applications

---

*See also: [[Dynamic Programming]], [[Edit Distance]], [[algorithms_and_ds]]*