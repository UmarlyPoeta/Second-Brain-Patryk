# String Matching

> Fundamental problem of finding occurrences of a pattern string within a text string, with various algorithms offering different trade-offs.

## 📖 Definition

String matching (pattern searching) is the problem of finding all occurrences of a pattern P of length m in a text T of length n. It's one of the most fundamental problems in computer science with applications in text processing, bioinformatics, and data analysis.

## 🔍 Basic Algorithms

### 1. Naive String Matching
Simple brute-force approach checking every position.

### 2. Advanced Algorithms
- [[KMP Algorithm]] - Uses failure function for efficiency
- [[Rabin-Karp Algorithm]] - Uses rolling hash for speed
- **Boyer-Moore Algorithm** - Skips characters for performance
- **Z Algorithm** - Linear preprocessing for multiple searches

## ⚡ Complexity Comparison

| Algorithm | Preprocessing | Matching | Space | Best For |
|-----------|---------------|----------|-------|----------|
| **Naive** | O(1) | O(nm) | O(1) | Small patterns |
| **KMP** | O(m) | O(n) | O(m) | Long texts |
| **Rabin-Karp** | O(m) | O(n) avg | O(1) | Multiple patterns |
| **Boyer-Moore** | O(m+σ) | O(n/m) avg | O(m) | Large alphabets |

Where n = text length, m = pattern length, σ = alphabet size

## 🐍 Python Implementation

```python
def naive_string_match(text, pattern):
    """Naive string matching - O(nm) time"""
    matches = []
    n, m = len(text), len(pattern)
    
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            matches.append(i)
    
    return matches

def naive_string_match_detailed(text, pattern):
    """Naive matching with character-by-character comparison"""
    matches = []
    n, m = len(text), len(pattern)
    
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        
        if j == m:  # Found complete match
            matches.append(i)
    
    return matches

def find_all_patterns(text, patterns):
    """Find all occurrences of multiple patterns"""
    result = {}
    
    for pattern in patterns:
        result[pattern] = naive_string_match(text, pattern)
    
    return result

def substring_search_python(text, pattern):
    """Using Python's built-in string methods"""
    matches = []
    start = 0
    
    while True:
        pos = text.find(pattern, start)
        if pos == -1:
            break
        matches.append(pos)
        start = pos + 1
    
    return matches

def pattern_with_wildcards(text, pattern):
    """Simple wildcard matching with ? (single char) and * (any chars)"""
    import re
    
    # Convert pattern to regex
    regex_pattern = pattern.replace('?', '.').replace('*', '.*')
    regex_pattern = f"^{regex_pattern}$"
    
    matches = []
    for i in range(len(text) - len(pattern) + 1):
        substring = text[i:i + len(pattern)]
        if re.match(regex_pattern, substring):
            matches.append(i)
    
    return matches

# Performance comparison
def compare_algorithms(text, pattern):
    """Compare different string matching approaches"""
    import time
    
    # Naive approach
    start = time.time()
    naive_matches = naive_string_match(text, pattern)
    naive_time = time.time() - start
    
    # Python built-in
    start = time.time()
    builtin_matches = substring_search_python(text, pattern)
    builtin_time = time.time() - start
    
    print(f"Naive: {len(naive_matches)} matches in {naive_time:.6f}s")
    print(f"Built-in: {len(builtin_matches)} matches in {builtin_time:.6f}s")
    
    return naive_matches, builtin_matches

# Example usage
if __name__ == "__main__":
    text = "ABABDABACDABABCABCABCABC"
    pattern = "ABABC"
    
    matches = naive_string_match(text, pattern)
    print(f"Pattern '{pattern}' found at positions: {matches}")
    
    # Multiple patterns
    patterns = ["ABA", "ABC", "CAB"]
    all_matches = find_all_patterns(text, patterns)
    print(f"Multiple patterns: {all_matches}")
    
    # Wildcard example
    wildcard_pattern = "A?A"
    wildcard_matches = pattern_with_wildcards(text, wildcard_pattern)
    print(f"Wildcard pattern '{wildcard_pattern}' found at: {wildcard_matches}")
```

## ☕ Java Implementation

```java
import java.util.*;

public class StringMatching {
    
    // Naive string matching
    public static List<Integer> naiveStringMatch(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        int n = text.length();
        int m = pattern.length();
        
        for (int i = 0; i <= n - m; i++) {
            int j = 0;
            while (j < m && text.charAt(i + j) == pattern.charAt(j)) {
                j++;
            }
            
            if (j == m) {
                matches.add(i);
            }
        }
        
        return matches;
    }
    
    // Find all occurrences using substring
    public static List<Integer> findAllOccurrences(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        int index = text.indexOf(pattern);
        
        while (index != -1) {
            matches.add(index);
            index = text.indexOf(pattern, index + 1);
        }
        
        return matches;
    }
    
    // Count occurrences
    public static int countOccurrences(String text, String pattern) {
        int count = 0;
        int index = text.indexOf(pattern);
        
        while (index != -1) {
            count++;
            index = text.indexOf(pattern, index + 1);
        }
        
        return count;
    }
    
    // Check if string contains pattern
    public static boolean containsPattern(String text, String pattern) {
        return text.contains(pattern);
    }
    
    public static void printMatches(String text, String pattern) {
        List<Integer> matches = naiveStringMatch(text, pattern);
        System.out.println("Pattern '" + pattern + "' found at positions: " + matches);
        
        for (int pos : matches) {
            System.out.println("  Position " + pos + ": " + 
                text.substring(Math.max(0, pos-3), Math.min(text.length(), pos+pattern.length()+3)));
        }
    }
    
    public static void main(String[] args) {
        String text = "ABABDABACDABABCABCABCABC";
        String pattern = "ABABC";
        
        printMatches(text, pattern);
        
        System.out.println("Total occurrences: " + countOccurrences(text, pattern));
        System.out.println("Contains pattern: " + containsPattern(text, pattern));
    }
}
```

## 🎯 String Matching Applications

### 1. Text Processing
- **Text Editors**: Find/replace functionality
- **Word Processors**: Spell check and autocorrect
- **Search Engines**: Query matching in documents

### 2. Bioinformatics
- **DNA Analysis**: Finding gene sequences
- **Protein Matching**: Amino acid sequence alignment
- **Phylogenetic Analysis**: Species relationship studies

### 3. Data Mining
- **Log Analysis**: Finding patterns in system logs
- **Data Validation**: Format checking and parsing
- **Information Extraction**: Structured data from text

### 4. Security
- **Intrusion Detection**: Malicious pattern detection
- **Virus Scanning**: Signature-based detection
- **Content Filtering**: Inappropriate content identification

## 🆚 Algorithm Selection Guide

### Choose Naive When:
- Pattern and text are small
- Simple implementation needed
- Memory is extremely limited

### Choose KMP When:
- Pattern has repeated prefixes
- Multiple searches with same pattern
- Linear time guarantee needed

### Choose Rabin-Karp When:
- Multiple patterns to search
- Average case performance sufficient
- Hash functions are efficient

### Choose Boyer-Moore When:
- Large alphabet size
- Long patterns
- Best average performance needed

## 💡 Optimization Techniques

1. **Preprocessing**: Build auxiliary data structures
2. **Skip Mechanisms**: Avoid unnecessary comparisons
3. **Hash Functions**: Quick string comparison
4. **Suffix Structures**: Reuse computation across searches

## 🔧 Advanced Topics

1. **Multiple Pattern Matching**: Aho-Corasick algorithm
2. **Approximate Matching**: Edit distance and fuzzy search
3. **Compressed Pattern Matching**: Search in compressed text
4. **Online Algorithms**: Process streaming text

## 🔗 Related Topics

- [[KMP Algorithm]] - Efficient exact pattern matching
- [[Rabin-Karp Algorithm]] - Hash-based pattern search
- [[Edit Distance]] - String similarity measurement
- [[Tries]] - Prefix tree for string operations

---

*See also: [[KMP Algorithm]], [[Rabin-Karp Algorithm]], [[algorithms_and_ds]]*