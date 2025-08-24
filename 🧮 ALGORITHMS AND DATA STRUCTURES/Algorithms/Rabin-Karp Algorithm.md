# Rabin-Karp Algorithm

> Rolling hash-based string matching algorithm that uses hash functions to efficiently find pattern occurrences in text.

## 📖 Definition

The Rabin-Karp algorithm searches for a pattern in a text using hashing. It computes hash values for the pattern and for each possible substring of the text, comparing hash values first before doing character-by-character comparison.

## ⚡ Time & Space Complexity

- **Average Case**: O(n + m) where n = text length, m = pattern length
- **Worst Case**: O(nm) when many hash collisions occur
- **Space Complexity**: O(1) - constant extra space
- **Preprocessing**: O(m) to compute pattern hash

## 🔑 Key Insight

Use rolling hash to compute substring hashes in O(1) time, making the average case linear.

## 🐍 Python Implementation

```python
def rabin_karp(text, pattern, prime=101):
    """Rabin-Karp algorithm for pattern matching"""
    n, m = len(text), len(pattern)
    
    if m > n:
        return []
    
    # Calculate hash values
    pattern_hash = 0
    text_hash = 0
    h = 1  # Hash multiplier for removing leading digit
    
    # Calculate h = pow(256, m-1) % prime
    for _ in range(m - 1):
        h = (h * 256) % prime
    
    # Calculate initial hash values
    for i in range(m):
        pattern_hash = (256 * pattern_hash + ord(pattern[i])) % prime
        text_hash = (256 * text_hash + ord(text[i])) % prime
    
    matches = []
    
    # Slide pattern over text
    for i in range(n - m + 1):
        # Check if hash values match
        if pattern_hash == text_hash:
            # Hash values match, verify character by character
            if text[i:i + m] == pattern:
                matches.append(i)
        
        # Calculate hash for next window
        if i < n - m:
            text_hash = (256 * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            # Handle negative values
            if text_hash < 0:
                text_hash += prime
    
    return matches

def rabin_karp_multiple(text, patterns, prime=101):
    """Search for multiple patterns simultaneously"""
    n = len(text)
    results = {pattern: [] for pattern in patterns}
    
    for pattern in patterns:
        m = len(pattern)
        if m > n:
            continue
        
        # Calculate pattern hash
        pattern_hash = 0
        for char in pattern:
            pattern_hash = (256 * pattern_hash + ord(char)) % prime
        
        # Calculate h for this pattern length
        h = 1
        for _ in range(m - 1):
            h = (h * 256) % prime
        
        # Calculate initial window hash
        text_hash = 0
        for i in range(m):
            text_hash = (256 * text_hash + ord(text[i])) % prime
        
        # Search for pattern
        for i in range(n - m + 1):
            if pattern_hash == text_hash:
                if text[i:i + m] == pattern:
                    results[pattern].append(i)
            
            if i < n - m:
                text_hash = (256 * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
                if text_hash < 0:
                    text_hash += prime
    
    return results

class RollingHash:
    """Rolling hash class for reusable hash computations"""
    
    def __init__(self, s, window_size, base=256, prime=101):
        self.base = base
        self.prime = prime
        self.window_size = window_size
        
        # Calculate base^(window_size-1) % prime
        self.h = 1
        for _ in range(window_size - 1):
            self.h = (self.h * base) % prime
        
        # Calculate initial hash
        self.hash_value = 0
        for i in range(window_size):
            self.hash_value = (base * self.hash_value + ord(s[i])) % prime
    
    def roll(self, old_char, new_char):
        """Roll the hash window"""
        # Remove old character
        self.hash_value = (self.hash_value - ord(old_char) * self.h) % self.prime
        
        # Add new character
        self.hash_value = (self.base * self.hash_value + ord(new_char)) % self.prime
        
        if self.hash_value < 0:
            self.hash_value += self.prime
        
        return self.hash_value

def rabin_karp_2d(matrix, pattern):
    """2D Rabin-Karp for searching pattern in 2D matrix"""
    if not matrix or not pattern:
        return []
    
    rows, cols = len(matrix), len(matrix[0])
    p_rows, p_cols = len(pattern), len(pattern[0])
    
    if p_rows > rows or p_cols > cols:
        return []
    
    matches = []
    
    # Simple 2D implementation (can be optimized with rolling hash)
    for i in range(rows - p_rows + 1):
        for j in range(cols - p_cols + 1):
            match = True
            for pi in range(p_rows):
                for pj in range(p_cols):
                    if matrix[i + pi][j + pj] != pattern[pi][pj]:
                        match = False
                        break
                if not match:
                    break
            
            if match:
                matches.append((i, j))
    
    return matches

# Example usage
if __name__ == "__main__":
    text = "ABABDABACDABABCABCABCABC"
    pattern = "ABABC"
    
    print("Rabin-Karp Algorithm:")
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    
    matches = rabin_karp(text, pattern)
    print(f"Matches found at positions: {matches}")
    
    # Multiple patterns
    patterns = ["ABA", "ABC", "CAB"]
    multi_matches = rabin_karp_multiple(text, patterns)
    print(f"Multiple patterns: {multi_matches}")
    
    # Rolling hash demonstration
    rh = RollingHash("ABCDE", 3)
    print(f"Initial hash for 'ABC': {rh.hash_value}")
    new_hash = rh.roll('A', 'F')  # ABC -> BCF
    print(f"Hash after rolling to 'BCF': {new_hash}")
```

## 🎯 Applications

1. **Plagiarism Detection**: Finding copied text segments
2. **Bioinformatics**: DNA/protein sequence analysis
3. **Data Deduplication**: Identifying duplicate content
4. **Version Control**: Efficient diff algorithms
5. **Antivirus Software**: Malware signature detection

## 🆚 Rabin-Karp vs Other Algorithms

| Feature | Rabin-Karp | KMP | Boyer-Moore | Naive |
|---------|------------|-----|-------------|-------|
| **Average Time** | O(n) | O(n) | O(n/m) | O(nm) |
| **Worst Time** | O(nm) | O(n) | O(nm) | O(nm) |
| **Multiple Patterns** | ✅ Excellent | ❌ Sequential | ❌ Sequential | ❌ Sequential |
| **Memory** | O(1) | O(m) | O(m+σ) | O(1) |

## 💡 Key Advantages

1. **Multiple Patterns**: Can search for many patterns simultaneously
2. **Simple Implementation**: Easier than KMP or Boyer-Moore
3. **Rolling Hash**: Efficient window sliding
4. **Parallelizable**: Hash computations can be parallelized

## 🚫 Limitations

1. **Hash Collisions**: Can cause false positives
2. **Worst Case**: Degrades to O(nm) with many collisions
3. **Prime Selection**: Performance depends on good hash function
4. **Spurious Matches**: Need verification after hash match

## 🔧 Optimizations

1. **Good Hash Functions**: Minimize collisions
2. **Multiple Hashes**: Use multiple hash functions
3. **Prime Selection**: Choose large primes carefully
4. **Early Termination**: Stop on first match if needed

## 🔗 Related Topics

- [[String Matching]] - General pattern matching problem
- [[KMP Algorithm]] - Alternative linear-time algorithm
- [[Hash Functions]] - Core component of Rabin-Karp
- [[Rolling Hash]] - Efficient hash computation technique

---

*See also: [[String Matching]], [[KMP Algorithm]], [[algorithms_and_ds]]*