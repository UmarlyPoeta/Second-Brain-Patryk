# Tries

> Tree-like data structure used to store associative arrays where keys are strings, enabling efficient prefix-based operations and string searches.

## 📖 Definition

A Trie (prefix tree) is a tree data structure used to store a dynamic set of strings. Each path from root to leaf represents a word, with common prefixes sharing the same path.

## 🔑 Key Properties

- Root represents empty string
- Each node can have up to 26 children (for lowercase English)
- Path from root to node represents a prefix
- Leaf nodes (or marked nodes) represent complete words

## ⚡ Time Complexity

| Operation | Time Complexity |
|-----------|-----------------|
| **Insert** | O(m) where m = length of word |
| **Search** | O(m) where m = length of word |
| **Delete** | O(m) where m = length of word |
| **Prefix Search** | O(p) where p = length of prefix |

## 🐍 Python Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to store children
        self.is_end_of_word = False  # Mark end of valid word

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert word into trie - O(m)"""
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
    
    def search(self, word):
        """Search for exact word - O(m)"""
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end_of_word
    
    def starts_with(self, prefix):
        """Check if any word starts with prefix - O(p)"""
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def get_words_with_prefix(self, prefix):
        """Get all words with given prefix"""
        node = self.root
        
        # Navigate to prefix end
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all words from this point
        words = []
        self._collect_words(node, prefix, words)
        return words
    
    def _collect_words(self, node, current_word, words):
        """Helper to collect all words from current node"""
        if node.is_end_of_word:
            words.append(current_word)
        
        for char, child_node in node.children.items():
            self._collect_words(child_node, current_word + char, words)
    
    def delete(self, word):
        """Delete word from trie"""
        def _delete_helper(node, word, index):
            if index == len(word):
                # We're at the end of the word
                if not node.is_end_of_word:
                    return False  # Word doesn't exist
                
                node.is_end_of_word = False
                # Return True if node has no children (can be deleted)
                return len(node.children) == 0
            
            char = word[index]
            child_node = node.children.get(char)
            
            if not child_node:
                return False  # Word doesn't exist
            
            should_delete_child = _delete_helper(child_node, word, index + 1)
            
            if should_delete_child:
                del node.children[char]
                # Return True if current node can be deleted
                return not node.is_end_of_word and len(node.children) == 0
            
            return False
        
        _delete_helper(self.root, word, 0)

# Example usage
def example_trie():
    trie = Trie()
    
    # Insert words
    words = ["cat", "cats", "dog", "dogs", "car", "card", "care"]
    for word in words:
        trie.insert(word)
    
    # Search operations
    print("Search 'cat':", trie.search("cat"))        # True
    print("Search 'ca':", trie.search("ca"))          # False
    print("Starts with 'ca':", trie.starts_with("ca")) # True
    
    # Get all words with prefix
    print("Words with prefix 'ca':", trie.get_words_with_prefix("ca"))
    print("Words with prefix 'dog':", trie.get_words_with_prefix("dog"))

if __name__ == "__main__":
    example_trie()
```

## 🎯 Applications

1. **Auto-complete/Suggestions**: Predictive text input
2. **Spell Checkers**: Dictionary lookup and suggestions
3. **IP Routing**: Longest prefix matching
4. **Search Engines**: Keyword suggestions
5. **Phone Directories**: Name prefix search

## 🆚 Comparison with Hash Tables

| Aspect | Trie | Hash Table |
|--------|------|-------------|
| **Prefix Search** | O(p) | O(k×n) where k=avg key length |
| **Memory** | Higher (tree structure) | Lower |
| **Ordered Output** | Natural lexicographic | Requires sorting |
| **Collision Handling** | No collisions | Hash collision possible |

## 🔗 Related Topics

- [[Binary Trees]] - Tree data structure foundation
- [[Hash Tables]] - Alternative for string storage
- [[Binary Search]] - Search algorithms
- [[Strings]] - Primary data type for tries

---

*See also: [[Binary Trees]], [[Hash Tables]], [[algorithms_and_ds]]*