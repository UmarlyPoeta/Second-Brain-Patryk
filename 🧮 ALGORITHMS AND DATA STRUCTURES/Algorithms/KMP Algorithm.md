# KMP Algorithm

> Knuth-Morris-Pratt string matching algorithm that uses preprocessing to achieve linear time pattern matching by avoiding redundant character comparisons.

## 📖 Definition

The KMP algorithm efficiently finds all occurrences of a pattern in a text by preprocessing the pattern to create a failure function (partial match table) that determines how to shift the pattern when a mismatch occurs.

## ⚡ Time & Space Complexity

- **Preprocessing**: O(m) where m = pattern length
- **Matching**: O(n) where n = text length
- **Total**: O(n + m) - linear time complexity
- **Space**: O(m) for failure function

## 🔑 Key Insight

When a mismatch occurs, use the failure function to determine how many characters to skip, avoiding redundant comparisons of characters we've already matched.

## 🐍 Python Implementation

```python
def compute_failure_function(pattern):
    """Compute failure function (LPS - Longest Proper Prefix which is also Suffix)"""
    m = len(pattern)
    failure = [0] * m
    
    # Length of previous longest prefix suffix
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            failure[i] = length
            i += 1
        else:
            if length != 0:
                length = failure[length - 1]
            else:
                failure[i] = 0
                i += 1
    
    return failure

def kmp_search(text, pattern):
    """KMP string matching algorithm"""
    n, m = len(text), len(pattern)
    
    if m == 0:
        return []
    
    # Compute failure function
    failure = compute_failure_function(pattern)
    
    matches = []
    i = j = 0  # i for text, j for pattern
    
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        
        if j == m:
            # Found complete match
            matches.append(i - j)
            j = failure[j - 1]
        elif i < n and text[i] != pattern[j]:
            # Mismatch occurred
            if j != 0:
                j = failure[j - 1]
            else:
                i += 1
    
    return matches

def kmp_search_with_steps(text, pattern):
    """KMP with step-by-step visualization"""
    failure = compute_failure_function(pattern)
    print(f"Pattern: {pattern}")
    print(f"Failure function: {failure}")
    print()
    
    n, m = len(text), len(pattern)
    matches = []
    i = j = 0
    
    print(f"Text: {text}")
    
    while i < n:
        print(f"Comparing text[{i}]='{text[i]}' with pattern[{j}]='{pattern[j]}'")
        
        if text[i] == pattern[j]:
            i += 1
            j += 1
            print(f"Match! Moving both pointers: i={i}, j={j}")
        
        if j == m:
            print(f"Complete match found at position {i - j}")
            matches.append(i - j)
            j = failure[j - 1]
            print(f"Using failure function: j={j}")
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = failure[j - 1]
                print(f"Mismatch! Using failure function: j={j}")
            else:
                i += 1
                print(f"Mismatch at start of pattern: i={i}")
        print()
    
    return matches

def build_automaton(pattern):
    """Build finite automaton for pattern matching"""
    m = len(pattern)
    
    # Get all possible characters in pattern
    alphabet = sorted(set(pattern))
    
    # Compute failure function
    failure = compute_failure_function(pattern)
    
    # Build state transition table
    automaton = {}
    
    for state in range(m + 1):
        automaton[state] = {}
        
        for char in alphabet:
            if state < m and pattern[state] == char:
                automaton[state][char] = state + 1
            else:
                # Use failure function to find next state
                next_state = state
                while next_state > 0 and pattern[next_state] != char:
                    next_state = failure[next_state - 1]
                
                if next_state < m and pattern[next_state] == char:
                    automaton[state][char] = next_state + 1
                else:
                    automaton[state][char] = 0
    
    return automaton

def automaton_search(text, pattern):
    """Pattern matching using finite automaton"""
    automaton = build_automaton(pattern)
    matches = []
    
    state = 0
    for i, char in enumerate(text):
        if char in automaton[state]:
            state = automaton[state][char]
        else:
            state = 0
            if char in automaton[state]:
                state = automaton[state][char]
        
        if state == len(pattern):
            matches.append(i - len(pattern) + 1)
    
    return matches

# Example usage
if __name__ == "__main__":
    text = "ABABDABACDABABCABCABCABC"
    pattern = "ABABC"
    
    print("KMP Algorithm Demonstration:")
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    print()
    
    # Show failure function
    failure = compute_failure_function(pattern)
    print("Failure function (LPS array):")
    for i, val in enumerate(failure):
        print(f"  {pattern[i]} -> {val}")
    print()
    
    # Find matches
    matches = kmp_search(text, pattern)
    print(f"Pattern found at positions: {matches}")
    
    # Show matches in context
    for pos in matches:
        start = max(0, pos - 3)
        end = min(len(text), pos + len(pattern) + 3)
        context = text[start:end]
        marker = ' ' * (pos - start) + '^' * len(pattern)
        print(f"Position {pos}: {context}")
        print(f"             {marker}")
    
    print("\nDetailed step-by-step:")
    kmp_search_with_steps("ABABCAB", "ABABC")
```

## ☕ Java Implementation

```java
public class KMPAlgorithm {
    
    public static int[] computeFailureFunction(String pattern) {
        int m = pattern.length();
        int[] failure = new int[m];
        
        int length = 0;
        int i = 1;
        
        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(length)) {
                length++;
                failure[i] = length;
                i++;
            } else {
                if (length != 0) {
                    length = failure[length - 1];
                } else {
                    failure[i] = 0;
                    i++;
                }
            }
        }
        
        return failure;
    }
    
    public static java.util.List<Integer> kmpSearch(String text, String pattern) {
        java.util.List<Integer> matches = new java.util.ArrayList<>();
        int n = text.length();
        int m = pattern.length();
        
        if (m == 0) return matches;
        
        int[] failure = computeFailureFunction(pattern);
        
        int i = 0; // text index
        int j = 0; // pattern index
        
        while (i < n) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }
            
            if (j == m) {
                matches.add(i - j);
                j = failure[j - 1];
            } else if (i < n && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) {
                    j = failure[j - 1];
                } else {
                    i++;
                }
            }
        }
        
        return matches;
    }
    
    public static void printFailureFunction(String pattern) {
        int[] failure = computeFailureFunction(pattern);
        System.out.println("Pattern: " + pattern);
        System.out.print("Index:   ");
        for (int i = 0; i < pattern.length(); i++) {
            System.out.print(i + " ");
        }
        System.out.println();
        System.out.print("Failure: ");
        for (int val : failure) {
            System.out.print(val + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        String text = "ABABDABACDABABCABCABCABC";
        String pattern = "ABABC";
        
        System.out.println("KMP Algorithm Example:");
        printFailureFunction(pattern);
        
        java.util.List<Integer> matches = kmpSearch(text, pattern);
        System.out.println("Pattern found at positions: " + matches);
    }
}
```

## 🎯 Applications

1. **Text Editors**: Find/replace functionality
2. **Bioinformatics**: DNA sequence searching
3. **Data Mining**: Pattern detection in logs
4. **Compilers**: Lexical analysis and tokenization
5. **Network Security**: Intrusion detection patterns

## 🆚 KMP vs Other String Matching

| Algorithm | Preprocessing | Matching | Space | Best For |
|-----------|---------------|----------|-------|----------|
| **KMP** | O(m) | O(n) | O(m) | Patterns with repetition |
| **Naive** | O(1) | O(nm) | O(1) | Simple cases |
| **Rabin-Karp** | O(m) | O(n) avg | O(1) | Multiple patterns |
| **Boyer-Moore** | O(m+σ) | O(n/m) avg | O(m) | Large alphabets |

## 💡 Key Insights

1. **Failure Function**: Encodes pattern's self-similarity
2. **No Backtracking**: Never moves backward in text
3. **Linear Time**: Optimal for exact string matching
4. **Preprocessing Pay-off**: Cost amortized over multiple searches

## 🔧 Variations

1. **KMP with Wildcards**: Handle ? and * characters
2. **Aho-Corasick**: Multiple pattern matching
3. **Z Algorithm**: Alternative linear-time approach
4. **Suffix Automaton**: More general pattern matching

## 🔗 Related Topics

- [[String Matching]] - General pattern matching problem
- [[Rabin-Karp Algorithm]] - Hash-based alternative
- [[String Algorithms]] - Comprehensive string processing
- [[Finite Automata]] - Theoretical foundation

---

*See also: [[String Matching]], [[Rabin-Karp Algorithm]], [[algorithms_and_ds]]*