# Hash Tables

> Data structure that implements an associative array abstract data type, mapping keys to values using a hash function for fast access, insertion, and deletion operations.

## 📖 Definition

A hash table (hash map) is a data structure that stores key-value pairs and uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found.

## 🔑 Key Components

1. **Hash Function**: Maps keys to array indices
2. **Buckets/Slots**: Array positions to store values
3. **Collision Resolution**: Handle multiple keys mapping to same index
4. **Load Factor**: Ratio of filled slots to total slots

## 🎯 Hash Functions

### Good Hash Function Properties:
- **Uniform Distribution**: Spreads keys evenly across table
- **Deterministic**: Same key always produces same hash
- **Fast Computation**: O(1) time complexity
- **Avalanche Effect**: Small key changes cause large hash changes

### Common Hash Functions:

```python
# Simple modular hash
def simple_hash(key, table_size):
    return hash(key) % table_size

# Division method
def division_hash(key, table_size):
    return key % table_size

# Multiplication method
def multiplication_hash(key, table_size):
    A = 0.6180339887  # (√5 - 1) / 2
    return int(table_size * ((key * A) % 1))

# String hashing
def string_hash(s, table_size):
    hash_val = 0
    for char in s:
        hash_val = (hash_val * 31 + ord(char)) % table_size
    return hash_val
```

## ⚔️ Collision Resolution

### 1. Chaining (Separate Chaining)
Store colliding elements in linked lists at each bucket.

### 2. Open Addressing
Find another empty slot using probing:
- **Linear Probing**: Check next slot sequentially
- **Quadratic Probing**: Check slots at quadratic intervals
- **Double Hashing**: Use second hash function for step size

## 🐍 Python Implementation

```python
class HashTable:
    def __init__(self, initial_capacity=11):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]  # Chaining
    
    def _hash(self, key):
        """Simple hash function"""
        if isinstance(key, str):
            return sum(ord(char) for char in key) % self.capacity
        return hash(key) % self.capacity
    
    def put(self, key, value):
        """Insert or update key-value pair - O(1) average"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Update existing key
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self.size += 1
        
        # Resize if load factor too high
        if self.size >= self.capacity * 0.7:
            self._resize()
    
    def get(self, key):
        """Retrieve value by key - O(1) average"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        raise KeyError(f"Key '{key}' not found")
    
    def delete(self, key):
        """Remove key-value pair - O(1) average"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return v
        
        raise KeyError(f"Key '{key}' not found")
    
    def _resize(self):
        """Resize hash table when load factor is high"""
        old_buckets = self.buckets
        self.capacity = self._next_prime(self.capacity * 2)
        self.buckets = [[] for _ in range(self.capacity)]
        old_size = self.size
        self.size = 0
        
        # Rehash all elements
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def _next_prime(self, n):
        """Find next prime number >= n"""
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    return False
            return True
        
        while not is_prime(n):
            n += 1
        return n
    
    def load_factor(self):
        """Calculate load factor"""
        return self.size / self.capacity
    
    def __contains__(self, key):
        """Check if key exists"""
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def keys(self):
        """Get all keys"""
        result = []
        for bucket in self.buckets:
            for key, _ in bucket:
                result.append(key)
        return result
    
    def values(self):
        """Get all values"""
        result = []
        for bucket in self.buckets:
            for _, value in bucket:
                result.append(value)
        return result
    
    def items(self):
        """Get all key-value pairs"""
        result = []
        for bucket in self.buckets:
            for item in bucket:
                result.append(item)
        return result
    
    def __str__(self):
        return str(dict(self.items()))

# Open Addressing Implementation (Linear Probing)
class HashTableOpenAddressing:
    def __init__(self, initial_capacity=11):
        self.capacity = initial_capacity
        self.size = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.deleted = [False] * self.capacity  # Tombstone for deleted items
    
    def _hash(self, key):
        if isinstance(key, str):
            return sum(ord(char) for char in key) % self.capacity
        return hash(key) % self.capacity
    
    def _probe(self, key):
        """Find slot for key using linear probing"""
        index = self._hash(key)
        
        while self.keys[index] is not None:
            if self.keys[index] == key and not self.deleted[index]:
                return index
            index = (index + 1) % self.capacity
        
        return index
    
    def put(self, key, value):
        """Insert or update key-value pair"""
        if self.size >= self.capacity * 0.7:
            self._resize()
        
        index = self._probe(key)
        
        if self.keys[index] is None or self.deleted[index]:
            self.size += 1
        
        self.keys[index] = key
        self.values[index] = value
        self.deleted[index] = False
    
    def get(self, key):
        """Retrieve value by key"""
        index = self._hash(key)
        
        while self.keys[index] is not None:
            if self.keys[index] == key and not self.deleted[index]:
                return self.values[index]
            index = (index + 1) % self.capacity
        
        raise KeyError(f"Key '{key}' not found")
    
    def delete(self, key):
        """Remove key-value pair using tombstone"""
        index = self._hash(key)
        
        while self.keys[index] is not None:
            if self.keys[index] == key and not self.deleted[index]:
                self.deleted[index] = True
                self.size -= 1
                return self.values[index]
            index = (index + 1) % self.capacity
        
        raise KeyError(f"Key '{key}' not found")
    
    def _resize(self):
        """Resize and rehash all elements"""
        old_keys, old_values, old_deleted = self.keys, self.values, self.deleted
        old_capacity = self.capacity
        
        self.capacity *= 2
        self.size = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.deleted = [False] * self.capacity
        
        for i in range(old_capacity):
            if old_keys[i] is not None and not old_deleted[i]:
                self.put(old_keys[i], old_values[i])
```

## ☕ Java Implementation

```java
import java.util.*;

// Chaining implementation
public class HashTableChaining<K, V> {
    private static class Node<K, V> {
        K key;
        V value;
        Node<K, V> next;
        
        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }
    
    private Node<K, V>[] table;
    private int size;
    private int capacity;
    private static final double LOAD_FACTOR_THRESHOLD = 0.75;
    
    @SuppressWarnings("unchecked")
    public HashTableChaining(int initialCapacity) {
        this.capacity = initialCapacity;
        this.table = new Node[capacity];
        this.size = 0;
    }
    
    public HashTableChaining() {
        this(16);
    }
    
    private int hash(K key) {
        if (key == null) return 0;
        return Math.abs(key.hashCode()) % capacity;
    }
    
    public void put(K key, V value) {
        if ((double) size / capacity >= LOAD_FACTOR_THRESHOLD) {
            resize();
        }
        
        int index = hash(key);
        Node<K, V> head = table[index];
        
        // Update existing key
        Node<K, V> current = head;
        while (current != null) {
            if (current.key.equals(key)) {
                current.value = value;
                return;
            }
            current = current.next;
        }
        
        // Add new node
        Node<K, V> newNode = new Node<>(key, value);
        newNode.next = head;
        table[index] = newNode;
        size++;
    }
    
    public V get(K key) {
        int index = hash(key);
        Node<K, V> current = table[index];
        
        while (current != null) {
            if (current.key.equals(key)) {
                return current.value;
            }
            current = current.next;
        }
        
        return null; // Key not found
    }
    
    public V remove(K key) {
        int index = hash(key);
        Node<K, V> current = table[index];
        Node<K, V> prev = null;
        
        while (current != null) {
            if (current.key.equals(key)) {
                if (prev == null) {
                    table[index] = current.next;
                } else {
                    prev.next = current.next;
                }
                size--;
                return current.value;
            }
            prev = current;
            current = current.next;
        }
        
        return null; // Key not found
    }
    
    public boolean containsKey(K key) {
        return get(key) != null;
    }
    
    public int size() { return size; }
    
    public boolean isEmpty() { return size == 0; }
    
    @SuppressWarnings("unchecked")
    private void resize() {
        Node<K, V>[] oldTable = table;
        capacity *= 2;
        table = new Node[capacity];
        int oldSize = size;
        size = 0;
        
        for (Node<K, V> head : oldTable) {
            Node<K, V> current = head;
            while (current != null) {
                put(current.key, current.value);
                current = current.next;
            }
        }
    }
    
    public List<K> keys() {
        List<K> result = new ArrayList<>();
        for (Node<K, V> head : table) {
            Node<K, V> current = head;
            while (current != null) {
                result.add(current.key);
                current = current.next;
            }
        }
        return result;
    }
}

// Using Java's built-in HashMap
public class HashMapExample {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        
        map.put("apple", 1);
        map.put("banana", 2);
        map.put("orange", 3);
        
        System.out.println(map.get("apple")); // 1
        System.out.println(map.containsKey("grape")); // false
        
        // Iteration
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
}
```

## ⚡ C++ Implementation

```cpp
#include <iostream>
#include <vector>
#include <list>
#include <functional>

template<typename K, typename V>
class HashTable {
private:
    struct KeyValue {
        K key;
        V value;
        
        KeyValue(const K& k, const V& v) : key(k), value(v) {}
    };
    
    std::vector<std::list<KeyValue>> table;
    size_t tableSize;
    size_t numElements;
    static constexpr double LOAD_FACTOR_THRESHOLD = 0.75;
    
    size_t hash(const K& key) const {
        return std::hash<K>{}(key) % tableSize;
    }
    
    void resize() {
        auto oldTable = std::move(table);
        tableSize *= 2;
        table = std::vector<std::list<KeyValue>>(tableSize);
        numElements = 0;
        
        for (const auto& bucket : oldTable) {
            for (const auto& kv : bucket) {
                put(kv.key, kv.value);
            }
        }
    }
    
public:
    HashTable(size_t initialSize = 16) 
        : tableSize(initialSize), numElements(0) {
        table.resize(tableSize);
    }
    
    void put(const K& key, const V& value) {
        if (static_cast<double>(numElements) / tableSize >= LOAD_FACTOR_THRESHOLD) {
            resize();
        }
        
        size_t index = hash(key);
        auto& bucket = table[index];
        
        // Update existing key
        for (auto& kv : bucket) {
            if (kv.key == key) {
                kv.value = value;
                return;
            }
        }
        
        // Add new key-value pair
        bucket.emplace_back(key, value);
        numElements++;
    }
    
    bool get(const K& key, V& value) const {
        size_t index = hash(key);
        const auto& bucket = table[index];
        
        for (const auto& kv : bucket) {
            if (kv.key == key) {
                value = kv.value;
                return true;
            }
        }
        return false;
    }
    
    bool remove(const K& key) {
        size_t index = hash(key);
        auto& bucket = table[index];
        
        for (auto it = bucket.begin(); it != bucket.end(); ++it) {
            if (it->key == key) {
                bucket.erase(it);
                numElements--;
                return true;
            }
        }
        return false;
    }
    
    bool contains(const K& key) const {
        V dummy;
        return get(key, dummy);
    }
    
    size_t size() const { return numElements; }
    
    bool empty() const { return numElements == 0; }
    
    double loadFactor() const {
        return static_cast<double>(numElements) / tableSize;
    }
    
    void display() const {
        for (size_t i = 0; i < tableSize; ++i) {
            std::cout << "Bucket " << i << ": ";
            for (const auto& kv : table[i]) {
                std::cout << "[" << kv.key << ":" << kv.value << "] ";
            }
            std::cout << std::endl;
        }
    }
};

// Using STL unordered_map
#include <unordered_map>

int main() {
    std::unordered_map<std::string, int> map;
    
    map["apple"] = 1;
    map["banana"] = 2;
    map["orange"] = 3;
    
    std::cout << map["apple"] << std::endl; // 1
    
    // Check if key exists
    if (map.find("grape") != map.end()) {
        std::cout << "Found grape" << std::endl;
    }
    
    // Iteration
    for (const auto& pair : map) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    
    return 0;
}
```

## ⚡ Time Complexity

| Operation | Average | Worst Case |
|-----------|---------|------------|
| **Search** | O(1) | O(n) |
| **Insert** | O(1) | O(n) |
| **Delete** | O(1) | O(n) |
| **Space** | O(n) | O(n) |

*Worst case occurs when all keys hash to same bucket*

## 🆚 Collision Resolution Comparison

| Method | Pros | Cons |
|--------|------|------|
| **Chaining** | Simple, handles high load factors | Extra memory for pointers |
| **Linear Probing** | Good cache performance | Primary clustering |
| **Quadratic Probing** | Reduces clustering | May not find empty slot |
| **Double Hashing** | Best distribution | Two hash computations |

## 🎯 Applications

### 1. Database Indexing
```python
class DatabaseIndex:
    def __init__(self):
        self.index = {}
    
    def add_record(self, key, record_location):
        """Add index entry pointing to record location"""
        if key not in self.index:
            self.index[key] = []
        self.index[key].append(record_location)
    
    def find_records(self, key):
        """Find all records with given key"""
        return self.index.get(key, [])
```

### 2. Caching (Memoization)
```python
def fibonacci_memo():
    cache = {}
    
    def fib(n):
        if n in cache:
            return cache[n]
        
        if n <= 1:
            result = n
        else:
            result = fib(n-1) + fib(n-2)
        
        cache[n] = result
        return result
    
    return fib
```

### 3. Word Frequency Counter
```python
def count_words(text):
    """Count frequency of words in text"""
    word_count = {}
    words = text.lower().split()
    
    for word in words:
        word = word.strip('.,!?";')
        word_count[word] = word_count.get(word, 0) + 1
    
    return word_count
```

## 🔗 Related Topics

- [[Arrays and Lists]] - Underlying storage for hash table
- [[Binary Search Trees]] - Alternative for ordered keys
- [[Graphs]] - Adjacency lists use hash tables

## 💡 Best Practices

1. **Choose good hash function**: Minimize collisions
2. **Monitor load factor**: Resize when it gets too high
3. **Handle collisions properly**: Choose appropriate resolution method
4. **Use prime table sizes**: Better distribution
5. **Consider key types**: Immutable keys prevent issues

## 📝 Practice Problems

1. **Two Sum**: Find two numbers that add up to target using hash map
2. **Group Anagrams**: Group strings that are anagrams
3. **Valid Anagram**: Check if two strings are anagrams
4. **First Unique Character**: Find first non-repeating character
5. **Longest Substring Without Repeating Characters**: Use sliding window with hash set
6. **Design Twitter**: Design simplified Twitter using hash maps
7. **LRU Cache**: Implement Least Recently Used cache

---

*See also: [[Arrays and Lists]], [[Binary Search Trees]], [[algorithms_and_ds]]*