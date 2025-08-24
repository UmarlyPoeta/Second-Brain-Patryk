# String Algorithms

> Collection of algorithms designed to solve problems involving strings, including pattern matching, text processing, and string transformations.

## 📖 Overview

String algorithms are fundamental in computer science, dealing with the manipulation and analysis of sequences of characters. They form the backbone of text editors, search engines, bioinformatics, and data processing systems.

## 🔍 Pattern Matching Algorithms

### Exact Matching
- [[String Matching]] - Basic pattern search methods
- [[KMP Algorithm]] - Knuth-Morris-Pratt efficient pattern matching
- [[Rabin-Karp Algorithm]] - Rolling hash-based pattern search
- **Boyer-Moore Algorithm** - Skip characters for faster search
- **Z Algorithm** - Linear time pattern matching

### Approximate Matching
- [[Edit Distance]] - Minimum operations to transform strings
- **Fuzzy String Matching** - Finding similar strings
- **Longest Common Subsequence** - [[Longest Common Subsequence]]

## 📊 String Processing Algorithms

### Text Analysis
- **Suffix Arrays** - Sorted array of all suffixes
- **Suffix Trees** - Tree of all suffixes
- **Longest Palindromic Substring** - Find longest palindrome
- **String Compression** - Reduce string size

### String Transformations
- **Anagram Detection** - Check if strings are anagrams
- **Palindrome Checking** - Verify if string reads same forwards/backwards
- **String Rotation** - Check if one string is rotation of another

## 🐍 Python Implementation Examples

```python
# Basic string operations
def is_palindrome(s):
    """Check if string is palindrome"""
    s = s.lower().replace(' ', '')
    return s == s[::-1]

def longest_common_prefix(strs):
    """Find longest common prefix among strings"""
    if not strs:
        return ""
    
    prefix = strs[0]
    for string in strs[1:]:
        while not string.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix

def reverse_words(s):
    """Reverse words in a string"""
    return ' '.join(s.split()[::-1])

def is_anagram(s1, s2):
    """Check if two strings are anagrams"""
    return sorted(s1.lower()) == sorted(s2.lower())

def remove_duplicates(s):
    """Remove duplicate characters from string"""
    seen = set()
    result = []
    
    for char in s:
        if char not in seen:
            seen.add(char)
            result.append(char)
    
    return ''.join(result)

def string_permutations(s):
    """Generate all permutations of string"""
    from itertools import permutations
    return [''.join(p) for p in permutations(s)]

def longest_palindromic_substring(s):
    """Find longest palindromic substring"""
    if not s:
        return ""
    
    start = 0
    max_len = 1
    
    for i in range(len(s)):
        # Odd length palindromes
        left, right = i, i
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > max_len:
                start = left
                max_len = right - left + 1
            left -= 1
            right += 1
        
        # Even length palindromes
        left, right = i, i + 1
        while left >= 0 and right < len(s) and s[left] == s[right]:
            if right - left + 1 > max_len:
                start = left
                max_len = right - left + 1
            left -= 1
            right += 1
    
    return s[start:start + max_len]

# Example usage
if __name__ == "__main__":
    print("Is 'racecar' palindrome?", is_palindrome("racecar"))
    print("LCP of ['flower', 'flow', 'flight']:", longest_common_prefix(['flower', 'flow', 'flight']))
    print("Reverse 'hello world':", reverse_words("hello world"))
    print("Are 'listen' and 'silent' anagrams?", is_anagram("listen", "silent"))
    print("Remove duplicates from 'hello':", remove_duplicates("hello"))
    print("Longest palindrome in 'babad':", longest_palindromic_substring("babad"))
```

## 🎯 String Algorithm Categories

### 1. Search and Match
- Find patterns or substrings within text
- Examples: String matching, regular expressions

### 2. Transform and Edit
- Modify strings according to rules
- Examples: Edit distance, string compression

### 3. Analyze and Compare
- Extract information from strings
- Examples: LCS, palindrome detection

### 4. Generate and Enumerate
- Create new strings from existing ones
- Examples: Permutations, combinations

## 💡 Common Techniques

1. **Two Pointers**: Compare characters from different positions
2. **Sliding Window**: Process substrings of varying sizes
3. **Dynamic Programming**: Build solutions from subproblems
4. **Hash Functions**: Quick string comparison and matching
5. **Trie Structures**: Efficient prefix operations

## 🔧 Optimization Strategies

1. **Preprocessing**: Build data structures for faster queries
2. **Early Termination**: Stop when answer is found
3. **Space-Time Trade-offs**: Use extra space for speed
4. **Parallel Processing**: Divide string operations

## 🎯 Real-World Applications

1. **Text Editors**: Find/replace, autocomplete, spell check
2. **Search Engines**: Web page indexing and retrieval
3. **Bioinformatics**: DNA sequence analysis
4. **Compilers**: Lexical analysis and parsing
5. **Data Validation**: Pattern matching for input validation

## 🔗 Related Topics

- [[String Matching]] - Pattern search algorithms
- [[KMP Algorithm]] - Efficient pattern matching
- [[Rabin-Karp Algorithm]] - Hash-based pattern search
- [[Edit Distance]] - String transformation metrics

---

*See also: [[String Matching]], [[KMP Algorithm]], [[algorithms_and_ds]]*